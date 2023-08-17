import os
import cv2
import numpy as np
import random

def aug_exposure(image, maxfactor):
    factor = random.uniform(1-(maxfactor-1), maxfactor)
    return np.clip(image * factor, 0, 255).astype(np.uint8)

def aug_sat(image, maxfactor):
    factor = random.uniform(1-(maxfactor-1), maxfactor)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:, 1] = np.clip(hsv[:,:, 1] * factor, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def aug_hue(image, maxangle):
    angle = random.uniform(-maxangle, maxangle)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:, 0] = np.clip(hsv[:,:, 0] + angle, 0, 180)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


def savephoto(image, label, name, final_path, augments=2, exposure=True, exposure_maxfactor=1.4, saturation=True, saturation_maxfactor=1.4, hue=True, hue_maxangle=10):

    #Guardamos como _0 la imagen original
    os.chdir(f"{final_path}/images")
    cv2.imwrite(f"{name}_0.jpg", image)

    if label != None:
        label_content = []
        for linea in label:
            label_content.append(linea.strip())
        os.chdir("..")
        os.chdir("labels")
        with open(f"{name}_0.txt", 'w') as f:
            for linea in label_content:
                f.write(linea + "\n")    
                
    os.chdir("..")
    os.chdir("..")

    #Guardamos las imagenes modificadas como _1, _2, _3, etc
    for i in range(augments):
        image_mod = image.copy()

        if exposure:
            image_mod = aug_exposure(image_mod, exposure_maxfactor)
        if saturation:
            image_mod = aug_sat(image_mod, saturation_maxfactor)
        if hue:
            image_mod = aug_hue(image_mod, hue_maxangle)
        os.chdir(f"{final_path}/images")
        cv2.imwrite(f"{name}_{i+1}.jpg", image_mod)
        if label != None:
            os.chdir("..")
            os.chdir("labels")
            with open(f"{name}_{i+1}.txt", 'w') as f:
                for linea in label_content:
                    f.write(linea + "\n")  
        os.chdir("..")
        os.chdir("..")