#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários

def cvt(gray_bgr):
    return cv2.cvtColor(gray_bgr, cv2.COLOR_BGR2GRAY)

## Inicio dos valores de conferencia
## USe isto para testar seu programa


filenames = "cookies01.png cookies02.png cookies03.png cookies03.png".split()

frames = [cv2.imread(f) for f in filenames]


# Trabalhe nesta função
# Pode criar e chamar novas funções o quanto quiser
def encontra(imagem_bgr): 
    """ Recebe uma imagem grande e uma sub imagem e devolve um dicionário com chaves 4, 8 e 16
        em cada posição contendo uma lista de tuplas i,j com os encontros daquelas resolucoes
    """      

    creme = 0
    chocolate = 0
    biscoitos = 0
    cookies = 0 
    total_no_azul = 0
    total_no_vermelho = 0

    ## Faça cv2.imshow para output visual
    cv2.imshow("Imagem na funcao procura", imagem_bgr)

    return creme, chocolate, biscoitos, cookies, total_no_azul, total_no_vermelho


if __name__ == "__main__":

    # Inicializa a leitura dos arquivos
    bgr = frames
    
    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")


        
    for i in range(len(frames)):
       

        creme, chocolate, biscoitos, cookies, total_no_azul, total_no_vermelho = encontra(frames[i])

        if cv2.waitKey(2000) & 0xFF == ord('q'):
            break



