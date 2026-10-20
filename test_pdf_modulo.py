import config
from pdf import crear_pdf


crear_pdf(
    "prueba_dos_caras.pdf",
    "prueba_size.jpeg",
    "prueba_size.jpeg",
    config.INE_ANCHO_MM,
    config.INE_ALTO_MM
)

print("PDF de dos caras creado correctamente.")