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


padrao_gabarito = cv2.imread("p2b_exemplo_mini_8_8.png")
imagem_gabarito = cv2.imread("p2b_exemplo.png")

padrao_gabarito = cvt(padrao_gabarito)
imagem_gabarito = cvt(imagem_gabarito)

# Fim dos valores de conferencia

padrao1 = cv2.imread("q2_img_1_mini.png")
padrao2 = cv2.imread("q2_img_2_mini.png")
padrao3 = cv2.imread("q2_img_3_mini.png")

padroes = [padrao1, padrao2, padrao3]

padroes = [cvt(img) for img in padroes]

teste1 = cv2.imread("q2_img_1.png")
teste2 = cv2.imread("q2_img_2.png")
teste3 = cv2.imread("q2_img_3.png")

frames = [teste1, teste2, teste3]

frames = [cvt(f) for f in frames]






# Trabalhe nesta função
# Pode criar e chamar novas funções o quanto quiser
def procura(frame_gray, imagem8x8gray): 
    """ Recebe uma imagem grande e uma sub imagem e devolve um dicionário com chaves 4, 8 e 16
        em cada posição contendo uma lista de tuplas i,j com os encontros daquelas resolucoes
    """      
    
    # Esta é apenas a saída para a imagem de teste. Obviamente você deve criar o seu
    return {16: [(9, 14), (16, 9), (11, 1), (3, 16), (10, 4), (3, 14), (2, 6)],
 4: [(3, 10), (1, 4), (10, 2), (5, 2), (11, 9), (12, 11)],
 8: [(3, 5), (9, 5), (7, 14)]}

## Adicionados DEPOIS da prova para melhorar a clareza

def resize_big(img, scale):
    """ Resizes a grayscale image"""
    out_size = np.array(img.shape)*int(scale)
    print(img.shape, out_size)
    return cv2.resize(src=img, dsize=tuple(out_size), interpolation=cv2.INTER_NEAREST)

def resize_big_color(img, scale):
    """ Resizes a grayscale image"""
    out_size = np.array(img.shape)*int(scale)
    out_size = out_size[:-1]
    print(img.shape, out_size)
    return cv2.resize(src=img, dsize=tuple(out_size), interpolation=cv2.INTER_NEAREST)


if __name__ == "__main__":

    # Inicializa a leitura dos arquivos
    bgr = frames
    
    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")


        
    for i in range(len(frames)):
        dicionario = procura(frames[i], padroes[i])
        print("resultado encontrado", dicionario)

        imagem_grande = resize_big(frames[i], 2)
        padrao_grande = resize_big(padroes[i], 16 )


        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('Imagem de entrada', imagem_grande)
        cv2.imshow('Padrao', padrao_grande)

        if cv2.waitKey(1500) & 0xFF == ord('q'):
            break



