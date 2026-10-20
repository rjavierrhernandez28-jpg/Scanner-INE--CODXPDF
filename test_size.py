import cv2
import config
from PIL import Image
from size import calcular_tamano, redimensionar_imagen, guardar_con_dpi


imagen = cv2.imread("prueba.jpeg")

ancho, alto = calcular_tamano(
    config.INE_ANCHO_MM, 
    config.INE_ALTO_MM, 
    config.DPI
    )

imagen_redimensionada = redimensionar_imagen(imagen, ancho, alto)

guardar_con_dpi(imagen_redimensionada, "prueba_size.jpeg", 300)

print("Dimensiones reales:", imagen_redimensionada.shape[1], "x", imagen_redimensionada.shape[0])
print("Tamaño calculado:", ancho, "x", alto)
print("Imagen guardada como prueba_size.jpeg")

imagen_guardada = Image.open("prueba_size.jpeg")

print("DPI guardados:", imagen_guardada.info.get("dpi"))