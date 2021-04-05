import meshio
import pandas as pd
import sys
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import csv

#Inicia a rotina que le o arquivo com os pontos onde seram colocados os momentos magneticos
namefileImput1='estrutura.vtk'
points, cells, point_data, cell_data, field_data = meshio.read(namefileImput1)

print(field_data)


npo=len(points)
print (npo)
coord = pd.DataFrame(points, columns=['X', 'Y', 'Z'])
#Finaliza a rotina que le o arquivo com os pontos onde seram colocados os momentos magneticos

# Define momentos magneticos do IMPUT1
mx=np.zeros(npo)
my=np.zeros(npo)
mz=np.zeros(npo)

for i2 in range(0,npo):
    mx[i2]=1.0
    my[i2]=2.0
    mz[i2]=3.0
    
field_data= dict([('Field',(mx ,my, mz))])


namefileOutputWF1='estruturaWF.vtk'
meshio.write(namefileOutputWF1,points,cells,point_data=point_data,cell_data=cell_data,field_data=field_data,file_format='vtk-ascii')


#Inicia a rotina que le o arquivo onde sera calculado o campo magnetico
namefileImput2='barra.vtk'
points1, cells1, point_data1, cell_data1, field_data1 = meshio.read(namefileImput2)
print (len (points1))
coord1 = pd.DataFrame(points1, columns=['X1', 'Y1', 'Z1'])
#Finaliza rotina que le o arquivo com os pontos onde serao colocados os momentos magneticos

#Inicia a rotina que le o arquivo onde sera calculado o campo magnetico

fout = open('file.xyz','w')
fout.write(str(npo)+'\n')
fout.write(str(npo)+'\n')
for i2 in range(0,npo):
    textolinha='C '+str(coord['X'][i2])+'\t\t'+str(coord['Y'][i2])+'\t\t'+str(coord['Z'][i2])+'\n'
    fout.write(textolinha)
fout.close()
# Finaliza a rotina que le o arquivo onde sera calculado o campo magnetico

# Inicia o calculo do campo magnetico
xe=coord['X']
ye=coord['Y']
ze=coord['Z']

mu0 = 4.0*np.pi * 10**(1) #* 10**(-7)                            #Constante Magnetica                       
def Bfield(x,y,z):
    global mu0
    global coord
    npo=len(coord)
    x1,y1,z1 = coord['X'],coord['Y'],coord['Z']
    
    bx=0.0; by=0.0; bz=0.0 
    for i in range(0,npo-1):
        
        xij=x-x1[i]
        yij=y-y1[i]
        zij=z-z1[i]
        
        rij= np.sqrt(xij**2+yij**2+zij**2)
        
        rij1=1.0/rij
        rij3=rij1*rij1*rij1
        rij5=rij3*rij1*rij1
        
        mag = mu0/(4*np.pi)
        mjrij=mx[i]*xij+my[i]*yij+mz[i]*zij
        
        bx = bx+mag * (mx[i]*rij3-3*mjrij*xij*rij5)           #Bx
        by = by+mag * (my[i]*rij3-3*mjrij*yij*rij5)           #By
        bz = bz+mag * (mz[i]*rij3-3*mjrij*zij*rij5)           #Bz
    return bx,by,bz
# Finaliza a rotina que calcula o campo Magnetico

xs=coord1['X1']
ys=coord1['Y1']
zs=coord1['Z1']

# Calculando os campos
bx1,by1,bz1 = Bfield(xs,ys,zs)                                   #Calculates Magnetic field in the bar

field_data1= dict([('MagField',[bx1,by1,bz1])])
namefileOutputWF1='barraBField.vtk'
meshio.write(namefileOutputWF1,points1,cells1,point_data=point_data1,cell_data=cell_data1,field_data=field_data1,file_format='vtk-ascii')




# Inicia a rotina que calcula a forca magnetica
def ForcaMag(bx,by,bz,nx,ny,nz,da):
    global mu0
    fx=0.0; fy=0.0; fz=0.0 
    for i in range(0,len(x)-1):
        
        fx = fx+(1/mu0)*( 0.5*(bx*bx-by*by-bz*bz)*nx + bx*by*ny + bx*bz*nz)*da           #fx
        fy = fy+(1/mu0)*( 0.5*(by*by-bx*bx-bz*bz)*ny + bx*by*nx + by*bz*nz)*da           #fy
        fz = fz+(1/mu0)*( 0.5*(bz*bz-bx*bx-by*by)*nz + by*bz*ny + bx*bz*nx)*da           #fz
    return fx,fy,fz
#Finaliza a rotina que calcula a forca magnetica
#Inicia o calculo dos vetores normais a estrutura
def calcNormal(x,y,z):
    global mu0
    nx=0.0; ny=0.0; nz=0.0 ; da=0.0
       
    nx = nx+0.0           #nx
    ny = ny+0.0           #ny
    nz = nz+0.0           #nz
    return nx,ny,nz,da


# Plotando os campos
xe,ye,ze,mx,my,mz = zip([xe,ye,ze,mx,my,mz])

# 3d figure
fig1 = plt.figure(1)
ax1 = fig1.gca(projection='3d')
ax1 = fig1.add_subplot(111, projection='3d')

ax1.quiver(xe,ye,ze,mx,my,mz,color='black')        #Plotando momentos magneticos	
ax1.scatter(xe, ye, ze,color='black')

ax1.quiver(xs,ys,zs,bx1,by1,bz1,color='r')        #Plotando campos mageticos
ax1.scatter(xs, ys, zs,color='g')

plt.title('Magnetic field of a spiral wire')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('EstruturaComM.png')
plt.show()

