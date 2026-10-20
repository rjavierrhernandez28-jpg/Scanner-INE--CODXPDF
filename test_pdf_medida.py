import pymupdf


pdf = pymupdf.open("prueba_pdf.pdf")

pagina = pdf[0]

ancho_pt = pagina.rect.width
alto_pt = pagina.rect.height

ancho_mm = ancho_pt * 25.4 / 72
alto_mm = alto_pt * 25.4 / 72

print("Tamaño del PDF:")
print("Ancho:", ancho_mm, "mm")
print("Alto:", alto_mm, "mm")

pdf.close()