from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


ancho_mm = 85.60
alto_mm = 53.98

ancho_pdf = ancho_mm * mm
alto_pdf = alto_mm * mm

pdf = canvas.Canvas("prueba_pdf.pdf", pagesize=(ancho_pdf, alto_pdf))

pdf.drawImage(
    "prueba_size.jpeg",
    0,
    0,
    width=ancho_pdf,
    height=alto_pdf
)

pdf.save()

print("PDF creado: prueba_pdf.pdf")
print("Tamaño físico:", ancho_mm, "x", alto_mm, "mm")