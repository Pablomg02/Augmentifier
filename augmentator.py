import os
import cv2
import numpy as np
import random

def exp(image, maxfactor):
    factor = random.uniform(1-(maxfactor-1), maxfactor)
    return np.clip(image * factor, 0, 255).astype(np.uint8)

def sat(image, maxfactor):
    factor = random.uniform(1-(maxfactor-1), maxfactor)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:, 1] = np.clip(hsv[:,:, 1] * factor, 0, 255)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def hue(image, maxangle):
    angle = random.uniform(-maxangle, maxangle)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:,:, 0] = np.clip(hsv[:,:, 0] + angle, 0, 180)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def xflip(image, prob):
    if random.random()<prob:
        return cv2.flip(image,0)
    else:
        return image
    
def yflip(image, prob):
    if random.random()<prob:
        return cv2.flip(image,1)
    else:
        return image
    
def blur(image, maxvalue):
    value = random.randint(1,maxvalue)
    if value % 2 == 0:
        value += 1
    return cv2.blur(image,(value,value))

def grayscale(image, prob):
    if random.random()<prob:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        return image




def getlabel(label):
    label_content = []
    for linea in label:
        label_content.append(linea.strip())
    return label_content


def savephoto(image_path, label_path, name, final_path, augments=3, do_exposure=True, exposure_maxfactor=1.4, do_saturation=True, saturation_maxfactor=1.4, do_hue=True, hue_maxangle=10, do_xflip = True, xflip_prob = 0.5, do_yflip = True, yflip_prob = 0.5, do_blur= True, blur_maxvalue = 9, do_grayscale = True, grayscale_prob = 0.1):
    image = cv2.imread(image_path)
    try:
        label = open(label_path, 'r')
    except:
        label = None

    #Guardamos como _0 la imagen original
    os.chdir(f"{final_path}/images")
    cv2.imwrite(f"{name}_0.jpg", image)

    if label != None:
        label_content = getlabel(label)
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

        if do_exposure:
            image_mod = exp(image_mod, exposure_maxfactor)
        if do_saturation:
            image_mod = sat(image_mod, saturation_maxfactor)
        if do_hue:
            image_mod = hue(image_mod, hue_maxangle)
        if do_xflip:
            image_mod = xflip(image_mod, xflip_prob)
        if do_yflip:
            image_mod = yflip(image_mod, yflip_prob)
        if do_blur:
            image_mod = blur(image_mod, blur_maxvalue)
        if do_grayscale:
            image_mod = grayscale(image_mod, grayscale_prob)

        #Now that we have the modified image, we save it
        os.chdir(f"{final_path}/images")
        cv2.imwrite(f"{name}_{i+1}.jpg", image_mod)

        #If the label already exists, we save it too
        if label != None:
            if label_content != []:
                os.chdir("..")
                os.chdir("labels")
                with open(f"{name}_{i+1}.txt", 'w') as f:
                    for linea in label_content:
                        f.write(linea + "\n")  
            #Now that we finished with the label, we close it
            label.close()
        os.chdir("..")
        os.chdir("..")