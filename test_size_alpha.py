import cv2
import config

from size import calcular_tamano, redimensionar_imagen, guardar_con_dpi


imagen = cv2.imread("prueba.jpeg")

ancho, alto = calcular_tamano(
    config.INE_ANCHO_MM,
    config.INE_ALTO_MM,
    config.DPI
)

imagen_redimensionada = redimensionar_imagen(
    imagen,
    ancho,
    alto
)

guardar_con_dpi(
    imagen_redimensionada,
    "prueba_size_dpi.png",
    config.DPI
)

print("Tamaño:", ancho, "x", alto)
print("DPI:", config.DPI)
print("Imagen guardada como prueba_size_dpi.png")