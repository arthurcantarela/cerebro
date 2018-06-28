from __future__ import division
from __future__ import print_function

import os
import sys
import copy

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

import numpy as np
import nibabel as nib

import time
mriFilename = os.path.join(
  "/home/cantarela/cerebro/Original", 
  "CC0300_ge_3_58_M.nii.gz"
)
manualFilename = os.path.join (
  "/home/cantarela/cerebro/Manual", 
  "CC0300_ge_3_58_M_manual.nii.gz"
)
mriFilename2 = os.path.join(
  "/home/cantarela/cerebro/Original", 
  "CC0019_philips_15_57_F.nii.gz"
)
mriFilename3 = os.path.join(
  "/home/cantarela/cerebro/Original", 
  "CC0172_siemens_15_52_M.nii.gz"
)
mriFile = nib.load(mriFilename)
manualFile = nib.load(manualFilename)
image = mriFile.get_fdata()
imageManual = manualFile.get_fdata()
print(np.asarray(image).max())
newImage = []
newImageManual = []
x, y, z = image.shape
factor = 1
clipping = True
for i in range(0,x,factor):
  newImage.append([])
  newImageManual.append([])
  for j in range(0,y,factor):
    newImage[int(i/factor)].append([])
    newImageManual[int(i/factor)].append([])
    for k in range(0,z,factor):
      newImage[int(i/factor)][int(j/factor)].append(image[i][j][k])
      newImageManual[int(i/factor)][int(j/factor)].append(imageManual[i][j][k])

x, y, z = np.asarray(newImage).shape
maxVal = np.asarray(newImage).max()
filled = np.zeros((x, y, z))
for i in range(0,x):
  for j in range(0,y):
    for k in range(0,z):
      color = newImage[i][j][k]
      if(color > maxVal/5 and (newImageManual[i][j][k] or not clipping)):
        filled[i][j][k] = min(1, color/maxVal)

xRange, yRange, zRange = filled.shape
maxRange = max(xRange, yRange, zRange)
imageRange = (xRange, yRange, zRange)

#print(filled)
#sys.exit()
def surfaceOnly(image):
  time1 = time.time()

  global filled
  global imageRange
  x1 = np.zeros(imageRange)
  x2 = np.zeros(imageRange)
  y1 = np.zeros(imageRange)
  y2 = np.zeros(imageRange)
  z1 = np.zeros(imageRange)
  z2 = np.zeros(imageRange)
    
  time2 = time.time()

  xRange, yRange, zRange = imageRange
  for x in range(0,xRange):
    for y in range(0,yRange):
      for z in range(0,zRange):
        if(filled[x][y][z]):
          if not(x - 1 >= 0) or not(filled[x-1][y][z]):
            x1[x][y][z] = 1
          if not(x + 1 < xRange) or not(filled[x+1][y][z]):
            x2[x][y][z] = 1
          if not(y - 1 >= 0) or not(filled[x][y-1][z]):
            y1[x][y][z] = 1
          if not(y + 1 < yRange) or not(filled[x][y+1][z]):
            y2[x][y][z] = 1
          if not(z - 1 >= 0) or not(filled[x][y][z-1]):
            z1[x][y][z] = 1
          if not(z + 1 < zRange) or not(filled[x][y][z-1]):
            z2[x][y][z] = 1

  time3 = time.time()

  print((time2 - time1)*1000)      
  print((time3 - time2)*1000)    

  return (x1, x2, y1, y2, z1, z2)

imageSurface = surfaceOnly(image)

def Voxel(origin, size=1):
  global imageSurface
  global maxRange
  x, y, z = origin
  global filled
  r = g = b = filled[x][y][z]
  divisor = maxRange/12

  gl.glPushMatrix()

  gl.glColor3f(r, g, b)
  gl.glTranslatef((x-maxRange/2)/divisor, (y-maxRange/2)/divisor, (z-maxRange/2)/divisor)
  
  vertices= (
    (size/2/divisor, size/2/divisor, size/2/divisor),
    (size/2/divisor, size/2/divisor, -size/2/divisor),
    (size/2/divisor, -size/2/divisor, size/2/divisor),
    (size/2/divisor, -size/2/divisor, -size/2/divisor),
    (-size/2/divisor, size/2/divisor, size/2/divisor),
    (-size/2/divisor, size/2/divisor, -size/2/divisor),
    (-size/2/divisor, -size/2/divisor, size/2/divisor),
    (-size/2/divisor, -size/2/divisor, -size/2/divisor)
  )
  
  faces = [
    (0,1,3,2),
    (4,5,7,6),
    (0,1,5,4),
    (2,3,7,6),
    (0,2,6,4),
    (1,3,7,5)
  ]
  faces = []
  x1, x2, y1, y2, z1, z2 = imageSurface
  if x1[x][y][z]: faces.append((4,5,7,6))
  if x2[x][y][z]: faces.append((0,1,3,2))
  if y1[x][y][z]: faces.append((2,3,7,6))
  if y2[x][y][z]: faces.append((0,1,5,4))
  if z1[x][y][z]: faces.append((1,3,7,5))
  if z2[x][y][z]: faces.append((0,2,6,4))

  for face in faces:
    gl.glBegin(gl.GL_QUADS)
    for vertex in face:
      gl.glVertex3fv(vertices[vertex])
    gl.glEnd()

  gl.glPopMatrix()

def init() :
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glClearDepth(1.0)
    
    gl.glShadeModel(gl.GL_FLAT)
    # gl.glShadeModel(gl.GL_SMOOTH)
    
    gl.glEnable(gl.GL_DEPTH_TEST)
    


def display() :
    time1 = time.time()
    global camera
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glPushMatrix()
    gl.glTranslatef(0.0, 0.0, -10.0)

    gl.glRotatef(camera["x"], 1.0, 0.0, 0.0)
    gl.glRotatef(camera["y"], 0.0, 1.0, 0.0)
    gl.glRotatef(camera["z"], 0.0, 0.0, 1.0)

    global filled
    global imageManual
    x, y, z = filled.shape
    for i in range(0, x):
      for j in range(0, y):
        for k in range(0, z):
          if(filled[i][j][k]):
            Voxel((i,j,k))

    gl.glPopMatrix()
    glut.glutSwapBuffers()
    print((time.time() - time1)*1000)


def reshape(w, h) :
    gl.glViewport (0, 0, w, h)
    gl.glMatrixMode(gl.GL_PROJECTION)
    gl.glLoadIdentity ()
    glu.gluPerspective(60.0, w/h, 1.0, 20.0)
    gl.glMatrixMode(gl.GL_MODELVIEW)
    gl.glLoadIdentity()
    glu.gluLookAt(0.0, 0.0, 5.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


def keyboard(key, x, y) :
    global camera
    if key == 'x' :
        camera["x"] = (camera["x"] + 10) % 360
    elif key == 'X' :
        camera["x"] = (camera["x"] - 10) % 360
    elif key == 'y' :
        camera["y"] = (camera["y"] + 10) % 360
    elif key == 'Y' :
        camera["y"] = (camera["y"] - 10) % 360
    elif key == 'z' :
        camera["z"] = (camera["z"] + 10) % 360
    elif key == 'Z' :
        camera["z"] = (camera["z"] - 10) % 360
    else :
        return
    glut.glutPostRedisplay()


def main() :
    _ = glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB | glut.GLUT_DEPTH)

    glut.glutInitWindowSize(800, 800)
    glut.glutInitWindowPosition(100, 100)
    _ = glut.glutCreateWindow(sys.argv[0])

    init()

    global camera
    camera = {"x": -90, "y": 0, "z": 135}
    _ = glut.glutDisplayFunc(display)
    _ = glut.glutReshapeFunc(reshape)
    _ = glut.glutKeyboardFunc(keyboard)

    glut.glutMainLoop()


if __name__ == "__main__" :
    main()
