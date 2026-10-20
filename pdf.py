from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm


def crear_pdf(ruta, imagen_superior, imagen_inferior, ancho_mm, alto_mm):
    x_mm, y_superior, y_inferior = posiciones_dos_imagenes(
        ancho_mm,
        alto_mm
    )

    pdf = canvas.Canvas(ruta, pagesize=letter)

    agregar_imagen(
    pdf,
    imagen_superior,
    ancho_mm,
    alto_mm,
    x_mm,
    y_superior
    )

    agregar_imagen(
    pdf,
    imagen_inferior,
    ancho_mm,
    alto_mm,
    x_mm,
    y_inferior
    )

    pdf.save()


def centrar_imagen(ancho_mm, alto_mm):
    ancho_hoja = 215.9
    alto_hoja = 279.4

    x = (ancho_hoja - ancho_mm) / 2
    y = (alto_hoja - alto_mm) / 2

    return x, y


def agregar_imagen(pdf, imagen, ancho_mm, alto_mm, x_mm, y_mm):
    ancho = ancho_mm * mm
    alto = alto_mm * mm

    x = x_mm * mm
    y = y_mm * mm

    pdf.drawImage(
        imagen,
        x,
        y,
        width=ancho,
        height=alto,
        mask="auto"
    )


def posiciones_dos_imagenes(ancho_mm, alto_mm):
    ancho_hoja = 215.9
    alto_hoja = 279.4

    x = (ancho_hoja - ancho_mm) / 2

    espacio_vertical = (
        alto_hoja - (alto_mm * 2)
    ) / 3

    y_inferior = espacio_vertical
    y_superior = espacio_vertical + alto_mm + espacio_vertical

    return x, y_superior, y_inferior