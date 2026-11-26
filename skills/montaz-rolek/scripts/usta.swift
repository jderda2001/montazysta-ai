import Foundation
import Vision
import ImageIO

// Uzycie: usta plik1.jpg plik2.jpg ...
// Wyjscie (CSV, os y od GORY, piksele obrazu):
// plik,twarz_x,twarz_y,twarz_w,twarz_h,broda_y,czubek_y,usta,oczy,yaw
// usta = wysokosc wewnetrznych warg / wysokosc twarzy (0 = zamkniete)
// oczy = srednia wysokosc/szerokosc oka (mrugniecie ~ <0.15)
func extent(_ pts: [CGPoint]) -> (CGFloat, CGFloat, CGFloat, CGFloat) {
    let xs = pts.map { $0.x }, ys = pts.map { $0.y }
    return (xs.min() ?? 0, xs.max() ?? 0, ys.min() ?? 0, ys.max() ?? 0)
}
print("plik,twarz_x,twarz_y,twarz_w,twarz_h,broda_y,czubek_y,usta,oczy,yaw")
for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    let name = (path as NSString).lastPathComponent
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil),
          let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { print("\(name),BLAD"); continue }
    let W = CGFloat(img.width), H = CGFloat(img.height)
    let req = VNDetectFaceLandmarksRequest()
    let handler = VNImageRequestHandler(cgImage: img, options: [:])
    do { try handler.perform([req]) } catch { print("\(name),BLAD"); continue }
    guard let f = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }),
          let lm = f.landmarks else { print("\(name),BRAK"); continue }
    let size = CGSize(width: W, height: H)
    let b = f.boundingBox
    var usta: CGFloat = -1, oczy: CGFloat = -1, broda: CGFloat = -1
    if let il = lm.innerLips {
        let e = extent(il.pointsInImage(imageSize: size))
        usta = (e.3 - e.2) / (b.height * H)
    }
    var ev: [CGFloat] = []
    for eye in [lm.leftEye, lm.rightEye] {
        if let eye = eye {
            let e = extent(eye.pointsInImage(imageSize: size))
            if e.1 - e.0 > 0 { ev.append((e.3 - e.2) / (e.1 - e.0)) }
        }
    }
    if !ev.isEmpty { oczy = ev.reduce(0, +) / CGFloat(ev.count) }
    if let fc = lm.faceContour {
        let e = extent(fc.pointsInImage(imageSize: size))
        broda = H - e.2   // najnizszy punkt konturu (obraz Vision ma y od dolu)
    }
    let yaw = f.yaw?.doubleValue ?? 0
    print(String(format: "%@,%.0f,%.0f,%.0f,%.0f,%.0f,%.0f,%.4f,%.3f,%.3f", name,
                 b.minX * W, (1 - b.maxY) * H, b.width * W, b.height * H, broda, (1 - b.maxY) * H, usta, oczy, yaw))
}
