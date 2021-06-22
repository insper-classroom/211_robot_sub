#! /usr/bin/env python3
# -*- coding:utf-8 -*-
# Sugerimos rodar com:
# roslaunch turtlebot3_gazebo  turtlebot3_stage_4.launch

from __future__ import print_function, division
import rospy

import numpy as np

import cv2

from geometry_msgs.msg import Twist, Vector3
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

import math


bridge = CvBridge()


ranges = None
minv = 0
maxv = 10

camera_image = np.zeros((480, 640, 3))

def scaneou(dado):
    global ranges
    global minv
    global maxv
    # Prints suprimidos para evitar ruido
    #print("Faixa valida: ", dado.range_min , " - ", dado.range_max )
    #print("Leituras:")
    ranges = np.array(dado.ranges).round(decimals=2)
    minv = dado.range_min 
    maxv = dado.range_max
 
# A função a seguir é chamada sempre que chega um novo frame
# Não faça cv2.imshow aqui
# Use a variável camera_image para processar opecv no loop principal
def roda_todo_frame(imagem):
    global camera_image

    print("frame")
    try:
        cv_image = bridge.compressed_imgmsg_to_cv2(imagem, "bgr8")
        camera_image = cv_image.copy()
    except CvBridgeError as e:
        print('ex', e)

def desenha(cv_image):
    """
        Use esta função como exemplo de como desenhar na tela
    """
    cv2.circle(cv_image,(256,256),64,(0,255,0),2)
    cv2.line(cv_image,(256,256),(400,400),(255,0,0),5)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(cv_image,'Boa sorte!',(0,50), font, 2,(255,255,255),2,cv2.LINE_AA)

def draw_lidar(cv_image, leituras):
    if leituras is None:
        return
    bot = [256,256] # centro do robô
    escala = 50 # transforma 0.01m em 0.5 px

    raio_bot = int(0.1*escala)
    # Desenha o robot
    cv2.circle(cv_image,(bot[0],bot[1]),raio_bot,(255,0,0),1)

    for i in range(len(leituras)):
        rad = math.radians(i)
        dist = leituras[i]
        if minv < dist < maxv:
            xl = int(bot[0] + dist*math.cos(rad)*50)
            yl = int(bot[1] + dist*math.sin(rad)*50)
            cv2.circle(cv_image,(xl,yl),1,(0,255,0),2)


def draw_hough(input):
    cv_image = input.copy()
    img_gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)   
    # O trecho abaixo é copiado direto da aula 2, parte sobre Hough, colocando só ma checagem para None na primeira iteraćão
    lines = cv2.HoughLinesP(img_gray, 10, math.pi/180.0, 100, np.array([]), 45, 5)
    if lines is None:
        print("No lines found")
        return [], cv_image
    a,b,c = lines.shape
    for i in range(a):
        # Faz uma linha ligando o ponto inicial ao ponto final, com a cor vermelha (BGR)
        cv2.line(cv_image, (lines[i][0][0], lines[i][0][1]), (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 1, cv2.LINE_AA)
    return lines, cv_image



def center_of_contour(contorno):
    """ Retorna uma tupla (cx, cy) que desenha o centro do contorno"""
    M = cv2.moments(contorno)
    if M["m00"] > 0.001:
        # Usando a expressão do centróide definida em: https://en.wikipedia.org/wiki/Image_moment
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        return (int(cX), int(cY))
    else:
        return (-1, -1)

def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,2)
    cv2.line(img,(x,y - size),(x, y + size),color,2)

        
        
if __name__=="__main__":

    rospy.init_node("q3sub")
    topico_imagem = "/camera/image/compressed"


    velocidade_saida = rospy.Publisher("/cmd_vel", Twist, queue_size = 3 )
    recebe_scan = rospy.Subscriber("/scan", LaserScan, scaneou)
    recebedor = rospy.Subscriber(topico_imagem, CompressedImage, roda_todo_frame, queue_size=4, buff_size = 2**24)

    
    zero = Twist(Vector3(0,0,0), Vector3(0,0,0))
    giro = Twist(Vector3(0,0,0), Vector3(0,0,0.1))


    cv2.namedWindow("Imagem do laser")


    cont = 0

    velocidade_saida.publish(giro)

    first = True
    
    while not rospy.is_shutdown():
        # Cria uma imagem 512 x 512 para desenhar o que é "visto" pelo laser
        laser_bgr = np.zeros(shape=[512, 512, 3], dtype=np.uint8)
        # Chama funćões de desenho
        draw_lidar(laser_bgr, ranges)

        lines, hough_bgr = draw_hough(laser_bgr)

        # Note que a imagem da câmera está em camera_image
            
        
        # Imprime a imagem de saida
        cv2.imshow("Imagem do laser", hough_bgr)
        # Imagem vista pela camera
        cv2.imshow("Imagem da camera", camera_image)       
        if first: 
            cv2.moveWindow("Imagem da camera", 600,300)
            first = False
        cv2.waitKey(1) # TRocamos o 0 por 40 para esperar 40 millisegundos
        rospy.sleep(0.01)



