import cv2
from PIL import Image


def milimetros_a_pixeles(milimetros, dpi):
    pulgadas = milimetros / 25.4
    pixeles = pulgadas * dpi
    return round(pixeles)


def calcular_tamano(ancho_mm, alto_mm, dpi):
    ancho_px = milimetros_a_pixeles(ancho_mm, dpi)
    alto_px = milimetros_a_pixeles(alto_mm, dpi)

    return ancho_px, alto_px


def redimensionar_imagen(imagen, ancho_px, alto_px):
    return cv2.resize(imagen,(ancho_px, alto_px))


def guardar_con_dpi(imagen, ruta, dpi):
    if imagen.shape[2] == 4:
        imagen_pil = Image.fromarray(
            cv2.cvtColor(imagen, cv2.COLOR_BGRA2RGBA)
        )
    else:
        imagen_pil = Image.fromarray(
            cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        )

    imagen_pil.save(ruta, dpi=(dpi, dpi))