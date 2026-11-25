import PDFKit
import AppKit
// Uzycie: pdf_strony WEJ.pdf KATALOG SZEROKOSC  -> strona_01.png ...
let a = CommandLine.arguments
guard let doc = PDFDocument(url: URL(fileURLWithPath: a[1])) else { print("nie otwieram PDF"); exit(1) }
let w = CGFloat(Double(a[3]) ?? 1200)
print("stron:", doc.pageCount)
for i in 0..<doc.pageCount {
  guard let p = doc.page(at: i) else { continue }
  let r = p.bounds(for: .mediaBox); let s = w / r.width
  let size = NSSize(width: w, height: (r.height * s).rounded())
  let img = p.thumbnail(of: size, for: .mediaBox)
  guard let t = img.tiffRepresentation, let b = NSBitmapImageRep(data: t), let png = b.representation(using: .png, properties: [:]) else { continue }
  try! png.write(to: URL(fileURLWithPath: String(format: "%@/strona_%02d.png", a[2], i + 1)))
}
