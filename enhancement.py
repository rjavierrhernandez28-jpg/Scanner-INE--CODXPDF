import cv2
import numpy as np


def mejorar_imagen(imagen):
    imagen = mejorar_contraste(imagen)
    imagen = redondear_esquinas(imagen)
    return imagen

def mejorar_contraste(imagen):
    hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )
    v = clahe.apply(v)
    hsv = cv2.merge([h, s, v])
    imagen = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return imagen


def redondear_esquinas(imagen):
    alto, ancho = imagen.shape[:2]
    mascara = np.zeros((alto, ancho), dtype=np.uint8)
    radio = int(min(alto, ancho) * 0.03)
    cv2.rectangle(
        mascara,
        (radio, 0),
        (ancho - radio, alto),
        255,
        -1
    )
    cv2.rectangle(
        mascara,
        (0, radio),
        (ancho, alto - radio),
        255,
        -1
    )
    cv2.circle(
    mascara,
    (radio, radio),
    radio,
    255,
    -1
    )
    cv2.circle(
    mascara,
    (ancho - radio, radio),
    radio,
    255,
    -1
    )
    cv2.circle(
    mascara,
    (ancho - radio, alto - radio),
    radio,
    255,
    -1
    )
    cv2.circle(
    mascara,
    (radio, alto - radio),
    radio,
    255,
    -1
    )
    b, g, r = cv2.split(imagen)
    resultado = cv2.merge([b, g, r, mascara])
    return resultado