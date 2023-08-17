import os
import cv2
import numpy as np
import random

import augmentator as aug

#========FUNCIONES========#
def finaldir(final):
    if not os.path.exists(final):
        os.makedirs(final)
        os.makedirs(final_images)
        os.makedirs(final_labels)

#========PRINTS DE INICIO========#
print("\n\n\n=============================================")
print("Este programa tiene como utilidad generar imágenes modificadas para aumentar el Dataset de entrenamiento")
print("El nombre de la carpeta raiz es a elección del usuario, pero debe contener las imágenes en la carpeta 'images' y las etiquetas en la carpeta 'labels'")
print("=============================================\n\n")


#========INPUTS========#
inicial = input("Ingrese el nombre de la carpeta donde se encuentran las imagenes y las etiquetas: ") #Carpeta donde se encuentran las imagenes sin tratar
final = f"{inicial}_augmented" #Carpeta donde se guardaran las imagenes tratadas

inicial_images = f"{inicial}/images" #Carpeta donde se encuentran las imagenes sin tratar
inicial_labels = f"{inicial}/labels" #Carpeta donde se encuentran las etiquetas sin tratar

final_images = f"{final}/images" #Carpeta donde se guardaran las imagenes tratadas
final_labels = f"{final}/labels" #Carpeta donde se guardaran las etiquetas tratadas


#========MAIN========#
# Crear carpeta final
finaldir(final) #creacion de carpeta final

archivos = os.listdir(inicial_images) #Lista de archivos en la carpeta inicial

#ahora se recorren los archivos de la carpeta inicial y se guardan en la carpeta final
for archivo in archivos:
    image = cv2.imread(f"{inicial_images}/{archivo}") #Es mejor hacer esto directamente en la funcion de augmentator.py
    try:
        label = open(f"{inicial_labels}/{archivo[:-4]}.txt", 'r') #Es mejor hacer esto directamente en la funcion de augmentator.py
    except: 
        label = None

    aug.savephoto(image, label, name = archivo[:-4], final_path = final, augments=5, exposure_maxfactor=1.8, saturation_maxfactor=1.8, hue_maxangle=20)

    if label != None: label.close()



