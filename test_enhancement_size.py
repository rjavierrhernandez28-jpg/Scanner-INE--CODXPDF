import cv2
import config

from enhancement import mejorar_imagen
from size import calcular_tamano, redimensionar_imagen, guardar_con_dpi


imagen = cv2.imread("prueba.jpeg")

imagen_mejorada = mejorar_imagen(imagen)

ancho, alto = calcular_tamano(
    config.INE_ANCHO_MM,
    config.INE_ALTO_MM,
    config.DPI
)

imagen_final = redimensionar_imagen(
    imagen_mejorada,
    ancho,
    alto
)

guardar_con_dpi(
    imagen_final,
    "prueba_final.png",
    config.DPI
)

print("Tamaño final:", ancho, "x", alto)
print("DPI:", config.DPI)
print("Imagen final guardada como prueba_final.png")