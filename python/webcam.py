# ~/Arquivos de Programas/python/python.exe
# -*- coding: utf-8 -*-

# Programa simples com camera webcam e opencv

import cv2 as cv
import os,sys, os.path
import numpy as np

#filtro azul = h115 s172 v144   r79 g226 b208
image_lower_hsv1 = np.array([160,172,115])
image_upper_hsv1 = np.array([135,172,115])
#filtro vermelho = h0 s212 v88   r177 g11 b11
image_lower_hsv2 = np.array([92,212,0])
image_upper_hsv2 = np.array([64,212,0])


def filtro_de_cor(img_bgr, low_hsv, high_hsv):
    """ retorna a imagem filtrada """
    img = cv.cvtColor(img_bgr,cv.COLOR_BGR2HSV)
    mask = cv.inRange(img, low_hsv, high_hsv)
    return mask 

def mascara_or(mask1, mask2):

    """ retorna a mascara or """
    mask = cv.bitwise_or(mask1, mask2)
    return mask

def mascara_and(mask1, mask2):
     """ retorna a mascara and """
     mask = cv.bitwise_and(mask1, mask2)
     
     return mask

def desenha_cruz(img, cX,cY, size, color):
     """ faz a cruz no ponto cx cy"""
     cv.line(img,(cX - size,cY),(cX + size,cY),color,5)
     cv.line(img,(cX,cY - size),(cX, cY + size),color,5)    

def escreve_texto(img, text, origem, color):
     """ escreve a localização do centro de massa """
 
     font = cv.FONT_HERSHEY_SIMPLEX
     origem = (0,50)
     cv.putText(img, str(text), origem, font,1,color,2,cv.LINE_AA)



def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """  
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1,20, param1=50, param2=30,minRadius=0,maxRadius=0)

    mask_hsv1 = filtro_de_cor(img, image_lower_hsv1, image_upper_hsv1)
    mask_hsv2 = filtro_de_cor(img, image_lower_hsv2, image_upper_hsv2)
    
    mask_hsv = mascara_or(mask_hsv1, mask_hsv2)
    
    contornos, _ = cv.findContours(mask_hsv, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) 

    mask_rgb = cv.cvtColor(mask_hsv, cv.COLOR_GRAY2RGB) 
    contornos_img = mask_rgb.copy()
    
    circles = []

    areas = []
    maior = 0
    for c in contornos:
        area = cv.contourArea(c)
        if area > maior:
            circles.append(c)
            maior = area
            areas.append(area)

    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # criando um círculo na cor branca a partir do centro dos círculos para cobri-los e mostrar na imagem apenas os maiores
        cv.circle(img,(i[0],i[1]),2,(255, 255, 255), 250)
    
    M = cv.moments(maior)

    # Verifica se existe alguma para calcular, se sim calcula e exibe no display
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        
        cv.drawContours(contornos_img, [maior], -1, [255, 0, 0], 5)
       
        #faz a cruz no centro de massa
        desenha_cruz(contornos_img, cX,cY, 20, (0,0,255))

        
        # Para escrever vamos definir uma fonte 
        texto = cY , cX
        origem = (0,50)
 
        escreve_texto(contornos_img, texto, origem, (0,255,0)) 
            
    else:
    # se não existe nada para segmentar
        cX, cY = 0, 0
        # Para escrever vamos definir uma fonte 
        texto = 'nao tem nada'
        origem = (0,50)
        escreve_texto(contornos_img, texto, origem, (0,0,255))
    


    return contornos_img

cv.namedWindow("circles")
# define a entrada de video para webcam
vc = cv.VideoCapture(0)

#vc = cv.VideoCapture("video.mp4") # para ler um video mp4 

#configura o tamanho da janela 
vc.set(cv.CAP_PROP_FRAME_WIDTH, 640)
vc.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame) # passa o frame para a função imagem_da_webcam e recebe em img imagem tratada



    cv.imshow("preview", img)
    cv.imshow("original", frame)
    rval, frame = vc.read()
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break

cv.destroyWindow("preview")
vc.release()
