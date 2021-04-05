import string,sys
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import math

#Inicia a rotina que le o arquivo com os pontos onde seram colocados os momentos magneticos

namefileImput1='estrutura.vtk'
print(namefileImput1)
file1 = open(namefileImput1,'r')

linha=[]
while 1:
    line = file1.readline() # read a line from he file
    if not line: break # if end-of-file: quit
    linha.append(line)

palavras=linha[4].split()
npts=int(palavras[1])

x=[]
y=[]
z=[]
for i in range(0,npts):
    coor=linha[5+i].split()
    x.append(float(coor[0]))
    y.append(float(coor[1]))
    z.append(float(coor[2]))
#Finaliza a rotina que le o arquivo com os pontos onde seram colocados os momentos magneticos

#Inicia rotina que escreve no primeiro arquivo lido
namefileOutput1='estruturaWF56645.vtk'
file1=open(namefileOutput1,'w')

for i in range(0,len(linha)):
    file1.write(linha[i])

file1.write(' \n')#Escreve no arquivo.
file1.write('POINT_DATA '+str(npts)+'\n')#Escreve no arquivo.
file1.write('VECTORS vectors float\n')#Escreve no arquivo.

# Define momentos magneticos do IMPUT1

mx=[]
my=[]
mz=[]
for i in range(0,npts):
    modm=1.0
    thetai=np.pi/2
    phi=(np.pi/2)*np.arctan2(x[i],y[i])
    mz.append(modm*np.cos(thetai))
    mxy=np.sqrt(modm*modm-mz[i]*mz[i])
    mx.append(mxy*np.cos(phi))
    my.append(mxy*np.sin(phi))

    file1.write(str(mx[i])+'  ')
    file1.write(str(my[i])+'  ')
    file1.write(str(mz[i])+'  \n') 
#Finalizarotina que escreve no primeiro arquivo lido      

Bex=10.0
Bey=0.0
Bez=0.0
dt=0.001
for tempo in range(0,1000):
    
    for i in range(0,npts):
        dmdtx=my[i]*Bez-mz[i]*Bey
        dmdty=mz[i]*Bex-mx[i]*Bez
        dmdtz=mx[i]*Bey-my[i]*Bex
        
        mx[i]=mx[i]+dmdtx*dt
        my[i]=my[i]+dmdty*dt
        mz[i]=mz[i]+dmdtz*dt
    
    namefileOutput1='estruturaWF_'+str(tempo)+'.vtk'
    print(namefileOutput1)
#Inicia rotina que escreve no arquivo.

    file1=open(namefileOutput1,'w')
    for i in range(0,len(linha)):
        file1.write(linha[i])

    file1.write(' \n')#Escreve no arquivo.
    file1.write('POINT_DATA '+str(npts)+'\n')#Escreve no arquivo.
    file1.write('VECTORS vectors float\n')#Escreve no arquivo.

    for i in range(0,npts):
        file1.write(str(mx[i])+'  ')
        file1.write(str(my[i])+'  ')
        file1.write(str(mz[i])+'  \n') 
#Finalizarotina que escreve no primeiro arquivo lido     
    


#Inicia a rotina que le o arquivo onde sera calculado o campo magnetico
#namefileImput2='barra.vtk'
#file2=open(namefileImput2,'r')
#linha1=[]

#palavras1=linha[4].split()
#numeropontos1=int(palavras1[1])
#print(numeropontos1)
