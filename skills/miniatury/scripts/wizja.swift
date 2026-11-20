// wizja.swift — ocena twarzy, wycinanie postaci i zapis obrazów.
// Wszystko liczy Apple Vision na tym Macu: nic nie jest pobierane ani wysyłane.
// Kompiluje go mini.py (swiftc -O) do ~/.cache/miniatury/wizja.
//
//   wizja ocen  [--lista PLIK | pliki...]         -> JSONL, jedna linia na obraz
//   wizja wytnij WEJ WYJ.png [--tryb plan|plan-pelny|osoba] [--skurcz PX] [--wtop PX] [--wymaz x,y,r[,tol]]… [--maska M.png]
//   wizja jpg   WEJ WYJ.jpg [--szer N] [--max-bajty N]
//   wizja skaluj WEJ WYJ.png --szer N
//   wizja tekst  WEJ [--szer N]                   -> JSON z rozpoznanymi napisami (kontrola czytelności)

import Foundation
import Vision
import CoreImage
import CoreImage.CIFilterBuiltins
import ImageIO
import UniformTypeIdentifiers

setvbuf(stdout, nil, _IOLBF, 0)

func blad(_ msg: String) -> Never {
    FileHandle.standardError.write((msg + "\n").data(using: .utf8)!)
    exit(1)
}

func wczytaj(_ path: String) -> CGImage? {
    guard let src = CGImageSourceCreateWithURL(URL(fileURLWithPath: path) as CFURL, nil) else { return nil }
    return CGImageSourceCreateImageAtIndex(src, 0, [kCGImageSourceShouldCache: false] as CFDictionary)
}

let sRGB = CGColorSpace(name: CGColorSpace.sRGB)!
let ciCtx = CIContext(options: [.workingColorSpace: sRGB, .outputColorSpace: sRGB])

func r3(_ v: Double) -> NSDecimalNumber { NSDecimalNumber(string: String(format: "%.3f", v.isFinite ? v : 0)) }
func r1(_ v: Double) -> NSDecimalNumber { NSDecimalNumber(string: String(format: "%.1f", v.isFinite ? v : 0)) }

// ---------------------------------------------------------------- geometria

struct P { var x: Double; var y: Double }

func punkty(_ r: VNFaceLandmarkRegion2D?, _ W: Double, _ H: Double) -> [P] {
    guard let r = r else { return [] }
    // Vision liczy od lewego dolnego rogu; przechodzimy na lewy górny.
    return r.pointsInImage(imageSize: CGSize(width: W, height: H)).map { P(x: Double($0.x), y: H - Double($0.y)) }
}

func srodek(_ a: [P]) -> P {
    guard !a.isEmpty else { return P(x: 0, y: 0) }
    return P(x: a.map { $0.x }.reduce(0, +) / Double(a.count), y: a.map { $0.y }.reduce(0, +) / Double(a.count))
}

func obroc(_ a: [P], wokol c: P, kat: Double) -> [P] {
    let cs = cos(kat), sn = sin(kat)
    return a.map { p in
        let dx = p.x - c.x, dy = p.y - c.y
        return P(x: c.x + dx * cs - dy * sn, y: c.y + dx * sn + dy * cs)
    }
}

func zakres(_ a: [P]) -> (x0: Double, x1: Double, y0: Double, y1: Double) {
    guard let f = a.first else { return (0, 0, 0, 0) }
    var x0 = f.x, x1 = f.x, y0 = f.y, y1 = f.y
    for p in a { x0 = min(x0, p.x); x1 = max(x1, p.x); y0 = min(y0, p.y); y1 = max(y1, p.y) }
    return (x0, x1, y0, y1)
}

// Ostrość: wariancja laplasjanu na wycinku twarzy sprowadzonym do stałego rozmiaru,
// żeby dało się porównywać klatki z różnych kadrów.
func ostrosc(_ cg: CGImage, _ rect: CGRect) -> Double {
    let n = 256
    let pelny = CGRect(x: 0, y: 0, width: cg.width, height: cg.height)
    guard let wyc = cg.cropping(to: rect.integral.intersection(pelny)) else { return 0 }
    var px = [UInt8](repeating: 0, count: n * n)
    let ok: Bool = px.withUnsafeMutableBytes { buf in
        guard let ctx = CGContext(data: buf.baseAddress, width: n, height: n, bitsPerComponent: 8, bytesPerRow: n,
                                  space: CGColorSpaceCreateDeviceGray(), bitmapInfo: CGImageAlphaInfo.none.rawValue) else { return false }
        ctx.interpolationQuality = .high
        ctx.draw(wyc, in: CGRect(x: 0, y: 0, width: n, height: n))
        return true
    }
    if !ok { return 0 }
    var s = 0.0, s2 = 0.0
    var c = 0
    for y in 1..<(n - 1) {
        for x in 1..<(n - 1) {
            let i = y * n + x
            let l = Double(px[i - n]) + Double(px[i + n]) + Double(px[i - 1]) + Double(px[i + 1]) - 4 * Double(px[i])
            s += l; s2 += l * l; c += 1
        }
    }
    let m = s / Double(c)
    return s2 / Double(c) - m * m
}

// ---------------------------------------------------------------- ocen

func ocen(_ path: String) -> [String: Any] {
    guard let cg = wczytaj(path) else { return ["plik": path, "blad": "nie da się wczytać"] }
    let W = Double(cg.width), H = Double(cg.height)
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    let prost = VNDetectFaceRectanglesRequest()
    let lm = VNDetectFaceLandmarksRequest()
    let jak = VNDetectFaceCaptureQualityRequest()
    let rece = VNDetectHumanHandPoseRequest()
    rece.maximumHandCount = 2
    do {
        try handler.perform([prost, rece])
        // Punkty i jakość liczymy dla twarzy z nowszego detektora: daje on ciągłe kąty głowy.
        lm.inputFaceObservations = prost.results
        jak.inputFaceObservations = prost.results
        try handler.perform([lm, jak])
    } catch {
        return ["plik": path, "blad": "\(error.localizedDescription)"]
    }
    var out: [String: Any] = ["plik": path, "w": Int(W), "h": Int(H)]
    let twarze = lm.results ?? []
    out["twarze"] = twarze.count

    // Dłonie: prostokąt wokół stawów o sensownej pewności.
    var listaRak: [[String: Any]] = []
    for o in rece.results ?? [] {
        guard let pk = try? o.recognizedPoints(.all) else { continue }
        let dobre = pk.values.filter { $0.confidence > 0.3 }
        if dobre.count < 8 { continue }
        let xs = dobre.map { Double($0.location.x) }, ys = dobre.map { 1 - Double($0.location.y) }
        let pew = dobre.map { Double($0.confidence) }.reduce(0, +) / Double(dobre.count)
        listaRak.append(["x": r3(xs.min()!), "y": r3(ys.min()!), "w": r3(xs.max()! - xs.min()!),
                         "h": r3(ys.max()! - ys.min()!), "pewnosc": r3(pew)])
    }
    out["rece"] = listaRak

    guard let f = twarze.max(by: { $0.boundingBox.width * $0.boundingBox.height < $1.boundingBox.width * $1.boundingBox.height }) else {
        return out
    }
    let bb = f.boundingBox
    var t: [String: Any] = [
        "x": r1(Double(bb.minX) * W), "y": r1((1 - Double(bb.maxY)) * H),
        "w": r1(Double(bb.width) * W), "h": r1(Double(bb.height) * H),
    ]
    // Kąty bierzemy z detektora prostokątów (ta sama twarz, dopasowana po środku).
    let wzor = (prost.results ?? []).min(by: {
        hypot($0.boundingBox.midX - bb.midX, $0.boundingBox.midY - bb.midY) < hypot($1.boundingBox.midX - bb.midX, $1.boundingBox.midY - bb.midY)
    }) ?? f
    if let yaw = wzor.yaw { t["yaw"] = r1(yaw.doubleValue * 180 / .pi) }
    if let pitch = wzor.pitch { t["pitch"] = r1(pitch.doubleValue * 180 / .pi) }
    // Jakość ujęcia twarzy: dopasuj obserwację po środku prostokąta.
    if let q = (jak.results ?? []).min(by: {
        hypot($0.boundingBox.midX - bb.midX, $0.boundingBox.midY - bb.midY) < hypot($1.boundingBox.midX - bb.midX, $1.boundingBox.midY - bb.midY)
    }), let v = q.faceCaptureQuality {
        t["jakosc"] = r3(Double(v))
    }
    t["ostrosc"] = r1(ostrosc(cg, CGRect(x: Double(bb.minX) * W, y: (1 - Double(bb.maxY)) * H, width: Double(bb.width) * W, height: Double(bb.height) * H)))

    if let l = f.landmarks {
        let oko1 = punkty(l.leftEye, W, H), oko2 = punkty(l.rightEye, W, H)
        if !oko1.isEmpty && !oko2.isEmpty {
            // Lewe/prawe liczymy tak, jak widać na obrazie.
            let (oL, oP) = srodek(oko1).x < srodek(oko2).x ? (oko1, oko2) : (oko2, oko1)
            let cL = srodek(oL), cP = srodek(oP)
            let kat = atan2(cP.y - cL.y, cP.x - cL.x)
            let c0 = P(x: (cL.x + cP.x) / 2, y: (cL.y + cP.y) / 2)
            let io = max(1, hypot(cP.x - cL.x, cP.y - cL.y))
            func pr(_ a: [P]) -> [P] { obroc(a, wokol: c0, kat: -kat) }
            t["roll"] = r1(kat * 180 / .pi)
            t["rozstaw_oczu"] = r1(io)
            let eL = zakres(pr(oL)), eP = zakres(pr(oP))
            t["oko_l"] = r3((eL.y1 - eL.y0) / max(1, eL.x1 - eL.x0))
            t["oko_p"] = r3((eP.y1 - eP.y0) / max(1, eP.x1 - eP.x0))
            let zew = pr(punkty(l.outerLips, W, H)), wew = pr(punkty(l.innerLips, W, H))
            if !zew.isEmpty {
                let z = zakres(zew)
                t["usta_szer"] = r3((z.x1 - z.x0) / io)
                t["usta_wys"] = r3((z.y1 - z.y0) / io)
                if !wew.isEmpty {
                    let w = zakres(wew)
                    t["usta_otw"] = r3((w.y1 - w.y0) / io)
                    // Kąciki wyżej niż środek ust = uśmiech (oś y rośnie w dół).
                    let lewy = zew.min(by: { $0.x < $1.x })!, prawy = zew.max(by: { $0.x < $1.x })!
                    t["kaciki"] = r3((srodek(wew).y - (lewy.y + prawy.y) / 2) / io)
                }
            }
            let b1 = pr(punkty(l.leftEyebrow, W, H)), b2 = pr(punkty(l.rightEyebrow, W, H))
            if !b1.isEmpty && !b2.isEmpty {
                let oczyY = (srodek(pr(oL)).y + srodek(pr(oP)).y) / 2
                let brwiY = (srodek(b1).y + srodek(b2).y) / 2
                t["brwi"] = r3((oczyY - brwiY) / io)
            }
            let z1 = pr(punkty(l.leftPupil, W, H)), z2 = pr(punkty(l.rightPupil, W, H))
            if let a = z1.first, let b = z2.first {
                let (zL, zP) = a.x < b.x ? (a, b) : (b, a)
                let sL = srodek(pr(oL)), sP = srodek(pr(oP))
                t["wzrok_x"] = r3(((zL.x - sL.x) / max(1, eL.x1 - eL.x0) + (zP.x - sP.x) / max(1, eP.x1 - eP.x0)) / 2)
            }
        }
    }
    out["twarz"] = t
    return out
}

func komendaOcen(_ args: [String]) {
    var pliki: [String] = []
    var i = 0
    while i < args.count {
        if args[i] == "--lista", i + 1 < args.count {
            guard let txt = try? String(contentsOfFile: args[i + 1], encoding: .utf8) else { blad("Nie mogę czytać listy: \(args[i + 1])") }
            pliki += txt.split(separator: "\n").map(String.init).filter { !$0.isEmpty }
            i += 2
        } else { pliki.append(args[i]); i += 1 }
    }
    if pliki.isEmpty { blad("ocen: podaj pliki albo --lista PLIK") }
    var wyniki = [String?](repeating: nil, count: pliki.count)
    let lock = NSLock()
    DispatchQueue.concurrentPerform(iterations: pliki.count) { k in
        let d = autoreleasepool { ocen(pliki[k]) }
        let s = (try? JSONSerialization.data(withJSONObject: d, options: [.sortedKeys])).flatMap { String(data: $0, encoding: .utf8) }
        lock.lock(); wyniki[k] = s; lock.unlock()
    }
    for s in wyniki { if let s = s { print(s) } }
}

// ---------------------------------------------------------------- wytnij

func maskaJakoTablica(_ buf: CVPixelBuffer) -> (dane: [Float], w: Int, h: Int) {
    CVPixelBufferLockBaseAddress(buf, .readOnly)
    defer { CVPixelBufferUnlockBaseAddress(buf, .readOnly) }
    let w = CVPixelBufferGetWidth(buf), h = CVPixelBufferGetHeight(buf)
    let rb = CVPixelBufferGetBytesPerRow(buf)
    let base = CVPixelBufferGetBaseAddress(buf)!
    var out = [Float](repeating: 0, count: w * h)
    let fmt = CVPixelBufferGetPixelFormatType(buf)
    for y in 0..<h {
        let row = base.advanced(by: y * rb)
        if fmt == kCVPixelFormatType_OneComponent32Float {
            let p = row.assumingMemoryBound(to: Float.self)
            for x in 0..<w { out[y * w + x] = p[x] }
        } else {
            let p = row.assumingMemoryBound(to: UInt8.self)
            for x in 0..<w { out[y * w + x] = Float(p[x]) / 255 }
        }
    }
    return (out, w, h)
}

// Rozmycie pudełkowe (dwa przebiegi dają prawie gaussa), liczone sumą kroczącą.
func rozmyj(_ a: inout [Float], _ w: Int, _ h: Int, r: Int, przebiegi: Int = 2) {
    if r <= 0 { return }
    var tmp = [Float](repeating: 0, count: w * h)
    let norm = 1 / Float(2 * r + 1)
    for _ in 0..<przebiegi {
        a.withUnsafeMutableBufferPointer { A in
            tmp.withUnsafeMutableBufferPointer { T in
                for y in 0..<h {
                    let o = y * w
                    var s: Float = 0
                    for k in -r...r { s += A[o + min(max(k, 0), w - 1)] }
                    for x in 0..<w {
                        T[o + x] = s * norm
                        s += A[o + min(x + r + 1, w - 1)] - A[o + max(x - r, 0)]
                    }
                }
                for x in 0..<w {
                    var s: Float = 0
                    for k in -r...r { s += T[min(max(k, 0), h - 1) * w + x] }
                    for y in 0..<h {
                        A[y * w + x] = s * norm
                        s += T[min(y + r + 1, h - 1) * w + x] - T[max(y - r, 0) * w + x]
                    }
                }
            }
        }
    }
}

// Erozja (filtr minimum) w dwóch osiach: cofa krawędź maski o r pikseli.
func skurczMaske(_ a: inout [Float], _ w: Int, _ h: Int, r: Int) {
    if r <= 0 { return }
    var tmp = [Float](repeating: 0, count: w * h)
    a.withUnsafeMutableBufferPointer { A in
        tmp.withUnsafeMutableBufferPointer { T in
            for y in 0..<h {
                let o = y * w
                for x in 0..<w {
                    var m: Float = 1
                    for k in max(x - r, 0)...min(x + r, w - 1) { let v = A[o + k]; if v < m { m = v } }
                    T[o + x] = m
                }
            }
            for y in 0..<h {
                let y0 = max(y - r, 0), y1 = min(y + r, h - 1)
                for x in 0..<w {
                    var m: Float = 1
                    var k = y0
                    while k <= y1 { let v = T[k * w + x]; if v < m { m = v }; k += 1 }
                    A[y * w + x] = m
                }
            }
        }
    }
}

func prog(_ a: inout [Float], _ lo: Float, _ hi: Float) {
    let d = max(hi - lo, 1e-6)
    for i in 0..<a.count {
        let t = min(max((a[i] - lo) / d, 0), 1)
        a[i] = t * t * (3 - 2 * t)
    }
}

func komendaWytnij(_ args: [String]) {
    guard args.count >= 2 else { blad("wytnij: WEJ WYJ.png [--tryb plan|plan-pelny|osoba] [--skurcz PX] [--wtop PX] [--margines PX] [--wymaz x,y,r[,tol]]… [--maska M.png]") }
    let wej = args[0], wyj = args[1]
    var tryb = "plan", skurcz = 2, wtop = 1, maskaPlik: String? = nil, margines = 24
    var gumki: [(x: Double, y: Double, r: Double, tol: Double)] = []
    var i = 2
    while i + 1 < args.count {
        switch args[i] {
        case "--wymaz":
            // "x,y,r[,tol]" w pikselach klatki: ręczne usunięcie resztek tła, których maski nie odróżniają
            // od postaci. Znikają tylko piksele o kolorze podobnym do środka koła (tol = odległość RGB,
            // domyślnie 45; 0 wyłącza test koloru), więc koło może zachodzić na skórę bez szkody.
            let c = args[i + 1].split(separator: ",").compactMap { Double($0) }
            if c.count != 3 && c.count != 4 { blad("--wymaz oczekuje x,y,r[,tol] w pikselach klatki") }
            gumki.append((c[0], c[1], c[2], c.count == 4 ? c[3] : 45))
        case "--tryb": tryb = args[i + 1]
        case "--skurcz": skurcz = Int(args[i + 1]) ?? skurcz
        case "--wtop": wtop = Int(args[i + 1]) ?? wtop
        case "--maska": maskaPlik = args[i + 1]
        case "--margines": margines = Int(args[i + 1]) ?? margines
        default: blad("wytnij: nieznana opcja \(args[i])")
        }
        i += 2
    }
    guard let cg = wczytaj(wej) else { blad("Nie mogę wczytać \(wej)") }
    let W = cg.width, H = cg.height
    let handler = VNImageRequestHandler(cgImage: cg, options: [:])
    let osoba = VNGeneratePersonInstanceMaskRequest()
    let plan = VNGenerateForegroundInstanceMaskRequest()
    let lm = VNDetectFaceLandmarksRequest()
    do { try handler.perform([osoba, plan, lm]) } catch { blad("Vision: \(error.localizedDescription)") }

    var mOsoba: [Float]? = nil
    // Najpierw dokładna segmentacja osób (model od rozmów wideo): dobrze odróżnia człowieka od fotela.
    let segm = VNGeneratePersonSegmentationRequest()
    segm.qualityLevel = .accurate
    segm.outputPixelFormat = kCVPixelFormatType_OneComponent8
    if (try? handler.perform([segm])) != nil, let b = segm.results?.first?.pixelBuffer {
        let m = maskaJakoTablica(b)
        // Maska ma własną rozdzielczość (np. 2016×1512), więc próbkujemy ją dwuliniowo do rozmiaru klatki.
        var pelna = [Float](repeating: 0, count: W * H)
        let fx = Float(m.w) / Float(W), fy = Float(m.h) / Float(H)
        for y in 0..<H {
            let sy = min(Float(m.h - 1), max(0, (Float(y) + 0.5) * fy - 0.5))
            let y0 = Int(sy), y1 = min(m.h - 1, y0 + 1)
            let ty = sy - Float(y0)
            for x in 0..<W {
                let sx = min(Float(m.w - 1), max(0, (Float(x) + 0.5) * fx - 0.5))
                let x0 = Int(sx), x1 = min(m.w - 1, x0 + 1)
                let tx = sx - Float(x0)
                let g = m.dane[y0 * m.w + x0] * (1 - tx) + m.dane[y0 * m.w + x1] * tx
                let d = m.dane[y1 * m.w + x0] * (1 - tx) + m.dane[y1 * m.w + x1] * tx
                pelna[y * W + x] = g * (1 - ty) + d * ty
            }
        }
        var suma: Float = 0
        var k = 0
        while k < pelna.count { suma += pelna[k]; k += 16 }
        if suma > 50 { mOsoba = pelna }
    }
    // Zapas: maska instancji osoby (ma słabe resztki wokół fotela, stąd próg 0,8 → 0,5 po przeskalowaniu).
    if mOsoba == nil, let o = osoba.results?.first, !o.allInstances.isEmpty,
       let b = try? o.generateScaledMaskForImage(forInstances: o.allInstances, from: handler) {
        let m = maskaJakoTablica(b)
        if m.w == W && m.h == H {
            var t = m.dane
            for k in 0..<t.count { t[k] = t[k] > 0.8 ? 1 : 0 }
            mOsoba = t
        }
    }
    // Pierwszy plan: bierzemy obiekty, które pokrywają się z osobą. Zwykle to jedna
    // sylwetka razem z mikrofonem przed klatką piersiową; lampa czy roślina odpadają.
    var mPlan: [Float]? = nil
    var instancje = 0, wybranych = 0
    if let o = plan.results?.first, !o.allInstances.isEmpty {
        instancje = o.allInstances.count
        var wybrane = IndexSet()
        if let os = mOsoba {
            for inst in o.allInstances {
                guard let b = try? o.generateScaledMaskForImage(forInstances: IndexSet(integer: inst), from: handler) else { continue }
                let m = maskaJakoTablica(b)
                if m.w != W || m.h != H { continue }
                var pole = 0, wspolne = 0
                var k = 0
                while k < m.dane.count {
                    if m.dane[k] > 0.5 { pole += 1; if os[k] > 0.5 { wspolne += 1 } }
                    k += 4
                }
                if pole > 0 && Double(wspolne) / Double(pole) > 0.25 { wybrane.insert(inst) }
            }
        } else { wybrane = o.allInstances }
        wybranych = wybrane.count
        if !wybrane.isEmpty, let b = try? o.generateScaledMaskForImage(forInstances: wybrane, from: handler) {
            let m = maskaJakoTablica(b)
            if m.w == W && m.h == H { mPlan = m.dane }
        }
    }

    var uzyty = tryb
    var maska: [Float]
    if tryb == "plan" || tryb == "plan-pelny", let m = mPlan {
        maska = m
        if tryb == "plan", let os = mOsoba {
            // Pierwszy plan potrafi zabrać też kawałek fotela przy szyi. Zostawiamy z niego tylko to,
            // co leży w obrysie sylwetki: w wierszu między skrajnymi pikselami osoby i pod jakimś jej
            // pikselem w kolumnie. Mikrofon przed klatką piersiową się mieści, zagłówek obok szyi nie.
            var wMin = [Int](repeating: W, count: H), wMax = [Int](repeating: -1, count: H)
            var kMin = [Int](repeating: H, count: W), kMax = [Int](repeating: -1, count: W)
            for y in 0..<H {
                let off = y * W
                for x in 0..<W where os[off + x] > 0.5 {
                    if x < wMin[y] { wMin[y] = x }; if x > wMax[y] { wMax[y] = x }
                    if y < kMin[x] { kMin[x] = y }; if y > kMax[x] { kMax[x] = y }
                }
            }
            // Gdy sylwetkę ucina dolna krawędź kadru, ciało ciągnie się dalej w dół.
            let dotykaDolu = wMax[H - 1] >= 0 || wMax[max(0, H - 4)] >= 0
            var dozw = [Float](repeating: 1, count: W * H) // 1 = poza dozwolonym obszarem (odwrócone pod erozję)
            for y in 0..<H {
                let off = y * W
                if wMax[y] < 0 { continue }
                for x in wMin[y]...wMax[y] where kMin[x] <= y && (dotykaDolu || y <= kMax[x]) { dozw[off + x] = 0 }
            }
            for k in 0..<(W * H) where os[k] > 0.5 { dozw[k] = 0 }
            skurczMaske(&dozw, W, H, r: 4) // erozja odwróconej maski = poszerzenie dozwolonego obszaru o 4 px
            // Maska osoby ma niższą rozdzielczość, więc jej brzeg jest schodkowy. Rozmycie i próg
            // wygładzają granicę, żeby nie wycinała ząbków w ramionach.
            rozmyj(&dozw, W, H, r: 9)
            prog(&dozw, 0.35, 0.65)
            for k in 0..<(W * H) { maska[k] *= (1 - dozw[k]) }
        }
    }
    else if let m = mOsoba {
        maska = m; uzyty = "osoba"
    } else if let m = mPlan { maska = m; uzyty = "plan-pelny" }
    else { blad("Nie znaleziono postaci na obrazie") }

    // Prostokąt postaci z marginesem.
    var x0 = W, x1 = -1, y0 = H, y1 = -1
    for y in 0..<H {
        let off = y * W
        for x in 0..<W where maska[off + x] > 0.5 {
            if x < x0 { x0 = x }; if x > x1 { x1 = x }; if y < y0 { y0 = y }; if y > y1 { y1 = y }
        }
    }
    if x1 < 0 { blad("Maska jest pusta") }
    x0 = max(0, x0 - margines); y0 = max(0, y0 - margines)
    x1 = min(W - 1, x1 + margines); y1 = min(H - 1, y1 + margines)
    let w = x1 - x0 + 1, h = y1 - y0 + 1

    var a = [Float](repeating: 0, count: w * h)
    for y in 0..<h { for x in 0..<w { a[y * w + x] = maska[(y + y0) * W + x + x0] } }

    // Piksele źródła (RGBA, nieprzezroczyste).
    var px = [UInt8](repeating: 0, count: w * h * 4)
    px.withUnsafeMutableBytes { buf in
        let ctx = CGContext(data: buf.baseAddress, width: w, height: h, bitsPerComponent: 8, bytesPerRow: w * 4, space: sRGB,
                            bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
        // CGContext rysuje od dołu, więc przesuwamy tak, by wycinek trafił w (0,0).
        ctx.draw(cg, in: CGRect(x: -x0, y: -(H - 1 - y1), width: W, height: H))
    }

    // Gumki: w kole znikają piksele o kolorze zbliżonym do koloru w jego środku.
    for g in gumki {
        let cx = g.x - Double(x0), cy = g.y - Double(y0)
        var sr = 0.0, sg = 0.0, sb = 0.0, n = 0.0
        // Wzorzec koloru: okno 3×3 wokół środka, najpierw tylko piksele należące do maski.
        // Przy większym oknie cienka kreska fotela uśredniała się z tłem i gumka jej nie rozpoznawała.
        for tylkoMaska in [true, false] {
            if n > 0 { break }
            for yy in max(0, Int(cy) - 1)...min(h - 1, max(0, Int(cy) + 1)) {
                for xx in max(0, Int(cx) - 1)...min(w - 1, max(0, Int(cx) + 1)) {
                    if tylkoMaska && a[yy * w + xx] <= 0.5 { continue }
                    let k = (yy * w + xx) * 4
                    sr += Double(px[k]); sg += Double(px[k + 1]); sb += Double(px[k + 2]); n += 1
                }
            }
        }
        if n == 0 { continue }
        sr /= n; sg /= n; sb /= n
        let xa = max(0, Int(cx - g.r - 3)), xb = min(w - 1, Int(cx + g.r + 3))
        let ya = max(0, Int(cy - g.r - 3)), yb = min(h - 1, Int(cy + g.r + 3))
        if xa > xb || ya > yb { continue }
        for yy in ya...yb {
            for xx in xa...xb {
                let d = hypot(Double(xx) - cx, Double(yy) - cy)
                if d > g.r + 2 { continue }
                let k = (yy * w + xx) * 4
                if g.tol > 0 {
                    let dr = Double(px[k]) - sr, dg = Double(px[k + 1]) - sg, db = Double(px[k + 2]) - sb
                    if (dr * dr + dg * dg + db * db).squareRoot() > g.tol { continue }
                }
                let t = min(max((d - (g.r - 2)) / 4, 0), 1) // miękki brzeg na 4 px
                a[yy * w + xx] *= Float(t * t * (3 - 2 * t))
            }
        }
    }

    // Krawędź: wygładź schodki po powiększeniu maski, potem cofnij ją o kilka pikseli,
    // żeby nie świeciła obwódka z koloru tła.
    rozmyj(&a, w, h, r: 2)
    prog(&a, 0.3, 0.7)
    skurczMaske(&a, w, h, r: skurcz)
    if wtop > 0 { rozmyj(&a, w, h, r: wtop, przebiegi: 1) }

    // Odbarwianie krawędzi: półprzezroczyste piksele dostają kolor z wnętrza postaci,
    // dzięki czemu jasna ściana nie zostaje jako poświata wokół włosów.
    var rdzen = a
    prog(&rdzen, 0.9, 0.98)
    skurczMaske(&rdzen, w, h, r: 3)
    var sr = [Float](repeating: 0, count: w * h), sg = sr, sb = sr
    for k in 0..<(w * h) {
        let c = rdzen[k]
        sr[k] = Float(px[k * 4]) * c; sg[k] = Float(px[k * 4 + 1]) * c; sb[k] = Float(px[k * 4 + 2]) * c
    }
    var sw = rdzen
    rozmyj(&sr, w, h, r: 5); rozmyj(&sg, w, h, r: 5); rozmyj(&sb, w, h, r: 5); rozmyj(&sw, w, h, r: 5)
    for k in 0..<(w * h) {
        let al = a[k]
        if al <= 0.001 { px[k * 4] = 0; px[k * 4 + 1] = 0; px[k * 4 + 2] = 0; px[k * 4 + 3] = 0; continue }
        let c = rdzen[k]
        if c < 0.999 && sw[k] > 0.02 {
            let t = 1 - c
            px[k * 4] = UInt8(min(255, max(0, Float(px[k * 4]) * (1 - t) + sr[k] / sw[k] * t)))
            px[k * 4 + 1] = UInt8(min(255, max(0, Float(px[k * 4 + 1]) * (1 - t) + sg[k] / sw[k] * t)))
            px[k * 4 + 2] = UInt8(min(255, max(0, Float(px[k * 4 + 2]) * (1 - t) + sb[k] / sw[k] * t)))
        }
        px[k * 4 + 3] = UInt8(min(255, max(0, al * 255 + 0.5)))
    }

    func zapiszPNG(_ dane: [UInt8], _ sciezka: String, alfa: CGImageAlphaInfo) {
        guard let prov = CGDataProvider(data: Data(dane) as CFData),
              let im = CGImage(width: w, height: h, bitsPerComponent: 8, bitsPerPixel: 32, bytesPerRow: w * 4, space: sRGB,
                               bitmapInfo: CGBitmapInfo(rawValue: alfa.rawValue), provider: prov, decode: nil,
                               shouldInterpolate: false, intent: .defaultIntent),
              let dst = CGImageDestinationCreateWithURL(URL(fileURLWithPath: sciezka) as CFURL, UTType.png.identifier as CFString, 1, nil)
        else { blad("Nie mogę zapisać \(sciezka)") }
        CGImageDestinationAddImage(dst, im, nil)
        if !CGImageDestinationFinalize(dst) { blad("Nie mogę zapisać \(sciezka)") }
    }
    zapiszPNG(px, wyj, alfa: .last)
    if let mp = maskaPlik {
        var m = [UInt8](repeating: 255, count: w * h * 4)
        for k in 0..<(w * h) { let v = UInt8(min(255, max(0, a[k] * 255 + 0.5))); m[k * 4] = v; m[k * 4 + 1] = v; m[k * 4 + 2] = v }
        zapiszPNG(m, mp, alfa: .noneSkipLast)
    }

    var info: [String: Any] = [
        "plik": wyj, "zrodlo": ["w": W, "h": H], "kadr": ["x": x0, "y": y0, "w": w, "h": h],
        "tryb": uzyty, "obiekty_pierwszego_planu": instancje, "wybrane_obiekty": wybranych,
    ]
    if let f = (lm.results ?? []).max(by: { $0.boundingBox.width * $0.boundingBox.height < $1.boundingBox.width * $1.boundingBox.height }) {
        let bb = f.boundingBox
        // Twarz we współrzędnych wyciętego pliku.
        info["twarz"] = ["x": r1(Double(bb.minX) * Double(W) - Double(x0)), "y": r1((1 - Double(bb.maxY)) * Double(H) - Double(y0)),
                         "w": r1(Double(bb.width) * Double(W)), "h": r1(Double(bb.height) * Double(H))]
    }
    let js = try! JSONSerialization.data(withJSONObject: info, options: [.sortedKeys])
    print(String(data: js, encoding: .utf8)!)
}

// ---------------------------------------------------------------- jpg / skaluj

func przeskaluj(_ cg: CGImage, szer: Int?) -> CIImage {
    var im = CIImage(cgImage: cg)
    if let s = szer, s != cg.width {
        let f = CIFilter.lanczosScaleTransform()
        f.inputImage = im.clampedToExtent()
        f.scale = Float(s) / Float(cg.width)
        f.aspectRatio = 1
        let h = (Double(cg.height) * Double(s) / Double(cg.width)).rounded()
        im = f.outputImage!.cropped(to: CGRect(x: 0, y: 0, width: Double(s), height: h))
    }
    return im
}

func opcje(_ args: [String], od: Int) -> [String: String] {
    var o: [String: String] = [:]
    var i = od
    while i + 1 < args.count { o[args[i]] = args[i + 1]; i += 2 }
    return o
}

func komendaJpg(_ args: [String]) {
    guard args.count >= 2 else { blad("jpg: WEJ WYJ.jpg [--szer N] [--max-bajty N]") }
    let o = opcje(args, od: 2)
    guard let cg = wczytaj(args[0]) else { blad("Nie mogę wczytać \(args[0])") }
    let im = przeskaluj(cg, szer: o["--szer"].flatMap { Int($0) })
    let limit = o["--max-bajty"].flatMap { Int($0) } ?? 2_000_000
    // Tło pod przezroczystość, bo JPEG jej nie ma.
    let tlo = CIImage(color: CIColor(red: 0, green: 0, blue: 0)).cropped(to: im.extent)
    let plaski = im.composited(over: tlo)
    var q = 0.95
    var dane = Data()
    while q >= 0.5 {
        guard let d = ciCtx.jpegRepresentation(of: plaski, colorSpace: sRGB,
                                               options: [kCGImageDestinationLossyCompressionQuality as CIImageRepresentationOption: q]) else { blad("Zapis JPEG nie powiódł się") }
        dane = d
        if d.count <= limit { break }
        q -= 0.03
    }
    do { try dane.write(to: URL(fileURLWithPath: args[1])) } catch { blad("Zapis: \(error.localizedDescription)") }
    print("{\"plik\": \"\(args[1])\", \"bajty\": \(dane.count), \"jakosc\": \(r3(q)), \"w\": \(Int(im.extent.width)), \"h\": \(Int(im.extent.height))}")
}

func komendaSkaluj(_ args: [String]) {
    guard args.count >= 2 else { blad("skaluj: WEJ WYJ.png --szer N") }
    let o = opcje(args, od: 2)
    guard let cg = wczytaj(args[0]) else { blad("Nie mogę wczytać \(args[0])") }
    let im = przeskaluj(cg, szer: o["--szer"].flatMap { Int($0) })
    do { try ciCtx.writePNGRepresentation(of: im, to: URL(fileURLWithPath: args[1]), format: .RGBA8, colorSpace: sRGB) }
    catch { blad("Zapis PNG: \(error.localizedDescription)") }
}

// ---------------------------------------------------------------- tekst

func komendaTekst(_ args: [String]) {
    guard let wej = args.first, let cg = wczytaj(wej) else { blad("tekst: PLIK [--szer N]") }
    let o = opcje(args, od: 1)
    var obraz = cg
    if let s = o["--szer"].flatMap({ Int($0) }), s != cg.width {
        // Pomniejszenie pokazuje, co zostaje z napisu w rozmiarze, w jakim widzi go widz.
        let im = przeskaluj(cg, szer: s)
        guard let m = ciCtx.createCGImage(im, from: im.extent) else { blad("Nie mogę przeskalować") }
        obraz = m
    }
    let req = VNRecognizeTextRequest()
    req.recognitionLevel = .accurate
    req.recognitionLanguages = ["pl-PL", "en-US"]
    req.usesLanguageCorrection = false
    req.automaticallyDetectsLanguage = false
    req.minimumTextHeight = 0
    do { try VNImageRequestHandler(cgImage: obraz, options: [:]).perform([req]) } catch { blad("Vision: \(error.localizedDescription)") }
    var linie: [[String: Any]] = []
    for ob in req.results ?? [] {
        guard let k = ob.topCandidates(1).first else { continue }
        let b = ob.boundingBox
        linie.append(["tekst": k.string, "pewnosc": r3(Double(k.confidence)),
                      "x": r3(Double(b.minX)), "y": r3(1 - Double(b.maxY)), "w": r3(Double(b.width)), "h": r3(Double(b.height))])
    }
    let js = try! JSONSerialization.data(withJSONObject: ["plik": wej, "w": obraz.width, "h": obraz.height, "linie": linie], options: [.sortedKeys])
    print(String(data: js, encoding: .utf8)!)
}

// ---------------------------------------------------------------- start

let argv = Array(CommandLine.arguments.dropFirst())
guard let cmd = argv.first else { blad("Użycie: wizja ocen|wytnij|jpg|skaluj|tekst …") }
let reszta = Array(argv.dropFirst())
switch cmd {
case "ocen": komendaOcen(reszta)
case "wytnij": komendaWytnij(reszta)
case "jpg": komendaJpg(reszta)
case "skaluj": komendaSkaluj(reszta)
case "tekst": komendaTekst(reszta)
default: blad("Nieznana komenda: \(cmd)")
}
