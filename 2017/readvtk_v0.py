import string,sys
import csv
import os
import math
import numpy as np
import matplotlib.pyplot as plt

#Inicia a rotina que le o arquivo com os pontos onde seram colocados os momentos magneticos
namefileImput1='estrutura.vtk'
print(namefileImput1)
file = open(namefileImput1,'r')
linha=[]
while 1:
    line = file.readline() # read a line from he file
    if not line: break # if end-of-file: quit
    linha.append(line)

namefileOutput1='estruturaWF56645.vtk'
file1=open(namefileOutput1,'w')

for i in range(0,len(linha)):
    file1.write(linha[i])

file1.write('VECTORS vectors float\n')

mx = '1 '
my = '3 '
mz = '4\n'

palavras=linha[4].split()
numeropontos=int(palavras[1])
print(numeropontos)


for i in range(0,numeropontos):
    file1.write(mx)
    file1.write(my)
    file1.write(mz)   
        

   

