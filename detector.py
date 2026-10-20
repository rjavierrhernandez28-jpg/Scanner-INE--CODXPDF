import cv2
import numpy as np


def encontrar_contorno_id(imagen):
    """Busca el contorno que más se parezca a una INE."""

    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)

    # Detectamos bordes
    bordes = cv2.Canny(blur, 50, 150)

    # Cerramos pequeños huecos en los bordes
    #bordes = cv2.dilate(bordes, None, iterations=1)
    
    kernel = np.ones((3, 3), np.uint8)

    bordes = cv2.morphologyEx(
        bordes,
        cv2.MORPH_CLOSE,
        kernel
        )

    contornos, _ = cv2.findContours(
        bordes,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    # La INE mide 85.60 × 53.98 mm
    proporcion_ine = 85.60 / 53.98

    candidatos = []

    for c in contornos:

        area = cv2.contourArea(c)

        # Ignoramos objetos demasiado pequeños
        if area < 1000:
            continue

        perimetro = cv2.arcLength(c, True)

        aprox = cv2.approxPolyDP(
            c,
            0.02 * perimetro,
            True
        )

        if len(aprox) != 4:
            continue

        puntos = aprox.reshape(4, 2)

        # Calculamos el rectángulo que contiene al candidato
        x, y, ancho, alto = cv2.boundingRect(puntos)

        if alto == 0 or ancho == 0:
            continue

        proporcion = max(ancho, alto) / min(ancho, alto)

        # Qué tan cerca está de la proporción de la INE
        diferencia = abs(proporcion - proporcion_ine)

        candidatos.append(
            (diferencia, -area, puntos)
        )

    if not candidatos:
        return None

    # Primero gana el que tenga la proporción más cercana.
    # En caso de empate, gana el de mayor área.
    candidatos.sort(
        key=lambda candidato: (
            candidato[0],
            candidato[1]
        )
    )

    _, _, esquinas = candidatos[0]

    # Refinamos las esquinas
    esquinas = np.float32(esquinas)

    esquinas_refinadas = cv2.cornerSubPix(
        np.float32(gris),
        esquinas,
        (5, 5),
        (-1, -1),
        (
            cv2.TERM_CRITERIA_EPS +
            cv2.TERM_CRITERIA_MAX_ITER,
            40,
            0.001
        )
    )

    return esquinas_refinadas