import cv2
import numpy as np
import sys
import os
import config


from detector import encontrar_contorno_id
from perspective import enderezar
from enhancement import mejorar_imagen
from size import calcular_tamano, redimensionar_imagen, guardar_con_dpi
from pdf import crear_pdf


INPUT_DIR = "input"
OUTPUT_DIR = "output"


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

    nombre = os.path.splitext(os.path.basename(ruta))[0]
    ext = os.path.splitext(ruta)[1]

    salida_debug = os.path.join(OUTPUT_DIR, f"{nombre}_debug{ext}")

    cv2.imwrite(salida_debug, debug_img)
    print(f"Debug guardado en: {salida_debug}")


def procesar_imagen(imagen, puntos):
    recortada = enderezar(imagen, puntos)
    recortada = mejorar_imagen(recortada)

    ancho, alto = calcular_tamano(
        config.INE_ANCHO_MM,
        config.INE_ALTO_MM,
        config.DPI
    )

    recortada = redimensionar_imagen(
        recortada,
        ancho,
        alto
    )

    return recortada


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <frente> <reverso> [--debug]")
        sys.exit(1)

    ruta_frente = sys.argv[1]
    ruta_reverso = sys.argv[2]

    modo_debug = "--debug" in sys.argv

    imagen_frente = cv2.imread(ruta_frente)

    if imagen_frente is None:
        print(f"No pude abrir la imagen: {ruta_frente}")
        sys.exit(1)

    puntos_frente = encontrar_contorno_id(imagen_frente)

    if puntos_frente is None:
        print("No encontré la INE en el frente.")
        sys.exit(1)

    if modo_debug:
        guardar_debug(imagen_frente, puntos_frente, ruta_frente)

    frente = procesar_imagen(
        imagen_frente,
        puntos_frente
        )

    print("Frente procesado:", frente.shape)

    imagen_reverso = cv2.imread(ruta_reverso)

    if imagen_reverso is None:
        print(f"No pude abrir la imagen: {ruta_reverso}")
        sys.exit(1)

    puntos_reverso = encontrar_contorno_id(imagen_reverso)

    if puntos_reverso is None:
        print("No encontré la INE en el reverso.")
        sys.exit(1)

    if modo_debug:
        guardar_debug(
        imagen_reverso,
        puntos_reverso,
        ruta_reverso
        )

    reverso = procesar_imagen(
        imagen_reverso,
        puntos_reverso
        )

    print("Reverso procesado:", reverso.shape)

    ruta_frente = os.path.join(
    OUTPUT_DIR,
    "frente_temp.png"
    )

    ruta_reverso = os.path.join(
        OUTPUT_DIR,
        "reverso_temp.png"
        )

    guardar_con_dpi(
        frente,
        ruta_frente,
        config.DPI
        )

    guardar_con_dpi(
        reverso,
        ruta_reverso,
        config.DPI
        )

    print("Frente guardado:", ruta_frente)
    print("Reverso guardado:", ruta_reverso)

    ruta_pdf = os.path.join(
    OUTPUT_DIR,
    "INE.pdf"
    )

    crear_pdf(
        ruta_pdf,
        ruta_frente,
        ruta_reverso,
        config.INE_ANCHO_MM,
        config.INE_ALTO_MM
        )

    print(f"PDF creado: {ruta_pdf}")


if __name__ == "__main__":
    main()