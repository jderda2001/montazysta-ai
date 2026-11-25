import Foundation
import Vision
import CoreImage
import ImageIO

// Uzycie: twarz plik1.png plik2.png ...  -> dla kazdego: nazwa, szerokosc, wysokosc, x, y, w, h (piksele, os y od GORY)
for path in CommandLine.arguments.dropFirst() {
    let url = URL(fileURLWithPath: path)
    guard let src = CGImageSourceCreateWithURL(url as CFURL, nil), let img = CGImageSourceCreateImageAtIndex(src, 0, nil) else { print("\(path) BLAD"); continue }
    let W = Double(img.width), H = Double(img.height)
    let req = VNDetectFaceRectanglesRequest()
    let handler = VNImageRequestHandler(cgImage: img, options: [:])
    do { try handler.perform([req]) } catch { print("\(path) BLAD \(error)"); continue }
    guard let r = (req.results ?? []).max(by: { $0.boundingBox.width < $1.boundingBox.width }) else { print("\(path) BRAK"); continue }
    let b = r.boundingBox  // znormalizowane, poczatek w lewym DOLNYM rogu
    print(String(format: "%@ %d %d %.1f %.1f %.1f %.1f", (path as NSString).lastPathComponent, img.width, img.height, b.minX * W, (1 - b.maxY) * H, b.width * W, b.height * H))
}
