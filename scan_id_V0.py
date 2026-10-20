"""
scan_id.py
Toma una foto de una credencial/ID y la endereza (perspective correction),
como si la hubieras escaneado.

Uso:
    python scan_id.py foto.jpg
    -> genera foto_scanned.jpg

    python scan_id.py foto.jpg --debug
    -> además genera foto_debug.jpg mostrando el contorno detectado

Requiere: opencv-python, numpy
    pip install opencv-python numpy
"""

import cv2
import numpy as np
import sys
import os


def encontrar_contorno_id(imagen):
    """Busca el contorno de 4 puntos más grande en la imagen (la ID)."""
    gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gris, (5, 5), 0)

    # Canny detecta bordes (transiciones fuertes de brillo)
    bordes = cv2.Canny(blur, 50, 150)

    # Dilatamos un poco para cerrar huecos en los bordes
    bordes = cv2.dilate(bordes, None, iterations=1)

    contornos, _ = cv2.findContours(
        bordes, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Ordenamos contornos de mayor a menor área, nos quedamos con los top 5
    contornos = sorted(contornos, key=cv2.contourArea, reverse=True)[:5]

    for c in contornos:
        perimetro = cv2.arcLength(c, True)
        # approxPolyDP simplifica el contorno a un polígono con menos puntos
        aprox = cv2.approxPolyDP(c, 0.02 * perimetro, True)

        if len(aprox) == 4:
            return aprox.reshape(4, 2)

    return None  # no encontró nada con forma de rectángulo


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


def enderezar(imagen, pts):
    """Aplica warpPerspective para 'aplanar' la ID a un rectángulo perfecto."""
    rect = ordenar_puntos(pts)
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

    return resultado


def guardar_debug(imagen, puntos, ruta):
    """Dibuja el contorno detectado y numera las esquinas sobre la foto original."""
    debug_img = imagen.copy()

    # Dibuja el polígono completo (línea verde)
    cv2.polylines(debug_img, [puntos.astype(int)], True, (0, 255, 0), 3)

    # Marca cada esquina con un círculo y su número, para ver el orden detectado
    for i, punto in enumerate(puntos.astype(int)):
        cv2.circle(debug_img, tuple(punto), 10, (0, 0, 255), -1)
        cv2.putText(debug_img, str(i), tuple(punto + 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

    nombre, ext = os.path.splitext(ruta)
    salida_debug = f"{nombre}_debug{ext}"
    cv2.imwrite(salida_debug, debug_img)
    print(f"Debug guardado en: {salida_debug}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python scan_id.py <ruta_imagen> [--debug]")
        sys.exit(1)

    ruta = sys.argv[1]
    modo_debug = "--debug" in sys.argv

    imagen = cv2.imread(ruta)

    if imagen is None:
        print(f"No pude abrir la imagen: {ruta}")
        sys.exit(1)

    puntos = encontrar_contorno_id(imagen)

    if puntos is None:
        print("No encontré un rectángulo de 4 lados claro. Intenta con:")
        print("- mejor contraste entre la ID y el fondo (usa un fondo oscuro/liso)")
        print("- más luz, foto menos borrosa")
        sys.exit(1)

    if modo_debug:
        guardar_debug(imagen, puntos, ruta)

    recortada = enderezar(imagen, puntos)

    nombre, ext = os.path.splitext(ruta)
    salida = f"{nombre}_scanned{ext}"
    cv2.imwrite(salida, recortada)
    print(f"Listo! Guardé el resultado en: {salida}")


if __name__ == "__main__":
    main()