from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import csv

x = np.linspace(-3,3,21)
y = np.linspace(-10,10,21)
z = np.linspace(-3,3,21)

x1 = x
y1 = y
z1 = z

x,y,z = np.meshgrid(x,y,z)

# 3d figure
fig1 = plt.figure(1)
ax1 = fig1.gca(projection='3d')
#ax1 = fig1.add_subplot(111)

t=np.linspace(-50,50,1000)

def espiral(r):
    global t
    phi = 2*np.pi*t
    x = r*np.cos(phi)
    y = 0.1*t
    z = r*np.sin(phi)
    return x,y,z

raio=1.0
cx,cy,cz = espiral(raio)                                   #Wire
Icur = 0.1*10.0**(6)                                           #Amps in the wire
mu = 4*np.pi * 10**(-7)                            #Magnetic constant                       


def B(x,y,z):
    global mu,Icur
    global t
    global cx,cy,cz
    x1,y1,z1 = cx,cy,cz
    
    bx=0.0; by=0.0; bz=0.0 
    for i in range(0,len(t)-1):
        im1=i+1
        dlx = x1[im1]-x1[i]
        dly = y1[im1]-y1[i]
        dlz = z1[im1]-z1[i]
        
        xij=x-x1[i]
        yij=y-y1[i]
        zij=z-z1[i]
        
        rij= np.sqrt(xij**2+yij**2+zij**2)
        mag = (mu/(4*np.pi))*(Icur/rij**3)                   #Magnitude of the vector B

        bx = bx+mag * (dly*zij-dlz*yij)           #Bx
        by = by+mag * (dlz*xij-dlx*zij)           #By
        bz = bz+mag * (dlx*yij-dly*xij)           #Bz
    return bx,by,bz


# Plot of the fields
bx1,by1,bz1 = B(x,y,z)                                   #Magnetic field

#print(by1)
elev=5.0
azim=10.0
ax1.view_init(elev,azim)

# Plot of the 3d vector field
ax1.quiver(x,y,z,bx1,by1,bz1,color='b',length=1)        #Plot the magnetic field
ax1.plot(cx,cy,cz,label='Cylinder',color='r')       #Plot wire

#ax1.plot(z,bz2,label='Cylinder',color='r')       #Plot wire


plt.title('Magnetic field of a spiral wire')
plt.xlabel('x')
plt.ylabel('y')
plt.savefig('B(xyz)elev%sazim.png'%elev)
plt.show()

fig2 = plt.figure(2)
ax2 = fig2.add_subplot(111)
ax2 = fig2.gca()

def By(x,y,z):
    global mu,Icur
    global t
    global cx,cy,cz
    x1,y1,z1 = cx,cy,cz
    
    by=0.0 
    for i in range(0,len(cx)-1):
        im1=i+1
        dlx = x1[im1]-x1[i]
        dly = y1[im1]-y1[i]
        dlz = z1[im1]-z1[i]
        
        xij=x-x1[i]
        yij=y-y1[i]
        zij=z-z1[i]
        
        rij= np.sqrt(xij**2+yij**2+zij**2)
        mag = (mu/(4*np.pi))*(Icur/rij**3)                   #Magnitude of the vector B

#        bx = bx+mag * (dly*zij-dlz*yij)           #Bx
        by = by+mag * (dlz*xij-dlx*zij)           #By
#        bz = bz+mag * (dlx*yij-dly*xij)           #Bz
    return by

def Bpamela(z):
    N=100
    Lz=10.0  #cm
    global mu,Icur,raio
    mag = (mu/(2))*(N*Icur/Lz)                   #Magnitude of the vector B
    alpha=z+Lz/2
    beta=z-Lz/2
    bz =mag * (beta/np.sqrt(raio**2+beta**2)-alpha/np.sqrt(raio**2+alpha**2))           #Bz
    return bz


plt.title('Magnetic field y component of a spiral wire at x=0,z=0')
plt.xlabel('y')
plt.ylabel('By')

by2 = By(0.0,y1,0.0)
by3 = Bpamela(y1)
ax2.plot(y1,by2,'ro',y1,by3,'b-')

plt.savefig('By(y).png')
plt.show()

with open('MagField.csv', 'wb') as testfile:
    csv_writer = csv.writer(testfile, delimiter=',')
    for i in range(len(x1)):
        for j in range(len(y1)):
            for k in range(len(z1)):
#                xra=(-1.0+2*i/20.)*3.0
#                yra=(-1.0+2*j/20.)*3.0
#                zra=(-1.0+2*k/20.)*3.0
#                ra2=(xra-0.0)**2+(yra-0.0)**2+(zra-0.0)**2
#                bx4,by4,bz4 = B(xra,yra,zra)
                csv_writer.writerow([x1[i],y1[j],z1[k],bx1[i][j][k],by1[i][j][k],bz1[i][j][k]])

with open('MagField.vtk', 'wb') as testfile:
    csv_writer = csv.writer(testfile, delimiter='\t')
    
    csv_writer.writerow(["# vtk DataFile Version 2.0 https://www.cfd-online.com/Forums/paraview/12960-paraview-vector-field.html"])
    csv_writer.writerow(["Unstructured Grid Example"])
    csv_writer.writerow(["ASCII"])
    csv_writer.writerow(["DATASET UNSTRUCTURED_GRID"])
    N=len(x1)*len(y1)*len(z1)
    csv_writer.writerow(["POINTS %s float"%N])
    for i in range(len(x1)):
        for j in range(len(y1)):
            for k in range(len(z1)):
#                xra=(-1.0+2*i/20.)*3.0
#                yra=(-1.0+2*j/20.)*3.0
#                zra=(-1.0+2*k/20.)*3.0
#                ra2=(xra-0.0)**2+(yra-0.0)**2+(zra-0.0)**2
#                bx4,by4,bz4 = B(xra,yra,zra)
                csv_writer.writerow([x1[i],y1[j],z1[k]])
    N2=2*N            
    csv_writer.writerow(["CELLS %s"%N+" %s"%N2])
    for i in range(len(x1)):
        for j in range(len(y1)):
            for k in range(len(z1)):
                csv_writer.writerow([1,0])
    csv_writer.writerow(["CELL_TYPES %s"%N])
    for i in range(len(x1)):
        for j in range(len(y1)):
            for k in range(len(z1)):
                csv_writer.writerow([1])
    csv_writer.writerow(["POINT_DATA %s"%N])
    csv_writer.writerow(["SCALARS scalarvalue float 1"])
    csv_writer.writerow(["LOOKUP_TABLE density"])    
    for i in range(len(x1)):
        for j in range(len(y1)):
            for k in range(len(z1)):
                density=1.0*z1[k]
                csv_writer.writerow([density])
    csv_writer.writerow(["VECTORS MagField float"])    
    for i in range(len(x1)):
        for j in range(len(y1)):
            for k in range(len(z1)):
                csv_writer.writerow([bx1[i][j][k],by1[i][j][k],bz1[i][j][k]])
