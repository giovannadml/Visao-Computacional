# ~/Arquivos de Programas/python/python.exe
# -*- coding: utf-8 -*-

# Programa com câmera webcam e opencv

import cv2 as cv
import os,sys, os.path
import numpy as np
import math


def image_da_webcam(img):
    """
    ->>> !!!! FECHE A JANELA COM A TECLA ESC !!!! <<<<-
        deve receber a imagem da camera e retornar uma imagems filtrada.
    """  
    imgGray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    bordas = cv.Canny(imgGray, 310,190)
    #  Usando a função HoughCircles para reconhecer os círculos na imagem
    #  Os parâmetros min e max Radius configuram o tamanho mínimo e máximo do raio 
    # dos círculos para pegar apenas os maiores
    circles = cv.HoughCircles(bordas,cv.HOUGH_GRADIENT,1,30, param1=50, param2=30,
        minRadius=45,maxRadius=70)

    contornos_img = img.copy()

    circles_list = []

    if circles is not None:    
        # só vai tentar desenhar os contornos e calcular o ângulo se tiver 
        # algum elemento em circles
        circles = np.uint16(np.around(circles))
        for p in circles[0,:]:
            cv.circle(contornos_img,(p[0],p[1]),p[2],(129, 129, 219),3)
            cv.circle(contornos_img,(p[0],p[1]),2,(250,100,10),3)
            # area = math.pi * p[2] * p[2]
            circles_list.append(p)
        if len(circles_list) == 2:
            # cv.line usada para criar a reta entre os centros dos círculos
            cv.line(contornos_img,(circles_list[0][0], circles_list[0][1]),
                (circles_list[1][0],circles_list[1][1]),(0,0,255),3)

            # cálculo do ângulo da reta criada em relação ao plano horizontal
            deltaX = circles_list[0][1] - circles_list[1][1]
            deltaY = circles_list[0][0] - circles_list[1][0]
            angR = math.atan2(deltaY, deltaX)
            angD = round(math.degrees(angR),2)

            cv.putText(contornos_img, str(f'{angD}'), (20,20), 
                cv.FONT_HERSHEY_SIMPLEX,1,(200,50,0),2,cv.LINE_AA)


    return contornos_img

cv.namedWindow("circles")
# define a entrada de video para webcam
webcam = cv.VideoCapture(0) 

#configura o tamanho da janela 
webcam.set(cv.CAP_PROP_FRAME_WIDTH, 740)
webcam.set(cv.CAP_PROP_FRAME_HEIGHT, 480)

if webcam.isOpened(): # try to get the first frame
    rval, frame = webcam.read()
else:
    rval = False

while rval:
    
    img = image_da_webcam(frame) 
    # passa o frame para a função imagem_da_webcam e recebe em img
    # a imagem tratada


    cv.imshow("circles", img)
    cv.imshow("original", frame)
    rval, frame = webcam.read()
    key = cv.waitKey(20)
    if key == 27: # exit on ESC
        break

cv.destroyWindow("circles")
webcam.release()
