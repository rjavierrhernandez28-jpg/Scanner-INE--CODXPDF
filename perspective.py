import cv2
import numpy as np


def ordenar_puntos(pts):
    """
    Ordena los 4 puntos como: arriba-izq, arriba-der, abajo-der, abajo-izq.
    Necesario porque approxPolyDP no garantiza un orden consistente.
    """
    rect = np.zeros((4, 2), dtype="float32")

    suma = pts.sum(axis=1)
    rect[0] = pts[np.argmin(suma)]  # arriba-izq: menor x+y
    rect[2] = pts[np.argmax(suma)]  # abajo-der: mayor x+y

    diferencia = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diferencia)]  # arriba-der: menor y-x
    rect[3] = pts[np.argmax(diferencia)]  # abajo-izq: mayor y-x

    return rect


def detectar_cara(imagen):
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    ruta_cascada = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"

    detector = cv2.CascadeClassifier(ruta_cascada)

    caras = detector.detectMultiScale(
        gris,
        scaleFactor=1.1,
        minNeighbors=5
    )

    return len(caras)


def corregir_orientacion(imagen):

    normal = detectar_cara(imagen)

    girada = cv2.rotate(imagen, cv2.ROTATE_180)
    invertida = detectar_cara(girada)

    print(f"Caras normal: {normal}")
    print(f"Caras girada: {invertida}")

    if invertida > normal:
        print("Girando imagen 180 grados")
        return girada

    return imagen


def enderezar(imagen, pts):
    """Aplica warpPerspective para 'aplanar' la ID a un rectángulo perfecto."""
    rect = ordenar_puntos(pts)

    print("Puntos ordenados:")
    print(rect)

    (tl, tr, br, bl) = rect

    # Calculamos el ancho y alto reales usando distancia euclidiana
    ancho_a = np.linalg.norm(br - bl)
    ancho_b = np.linalg.norm(tr - tl)
    ancho_max = int(max(ancho_a, ancho_b))

    alto_a = np.linalg.norm(tr - br)
    alto_b = np.linalg.norm(tl - bl)
    alto_max = int(max(alto_a, alto_b))

    # Puntos destino: un rectángulo perfecto de ancho_max x alto_max
    destino = np.array([
        [0, 0],
        [ancho_max - 1, 0],
        [ancho_max - 1, alto_max - 1],
        [0, alto_max - 1]
    ], dtype="float32")

    matriz = cv2.getPerspectiveTransform(rect, destino)
    resultado = cv2.warpPerspective(imagen, matriz, (ancho_max, alto_max))

    # Las IDs (INE, licencia, etc.) casi siempre son horizontales.
    # Si el resultado salió más alto que ancho, lo rotamos 90°.
    alto, ancho = resultado.shape[:2]
    if alto > ancho:
        resultado = cv2.rotate(resultado, cv2.ROTATE_90_CLOCKWISE)

    resultado = corregir_orientacion(resultado)

    return resultado