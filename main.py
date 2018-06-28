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
  "/home/cantarela/cerebro/samples/Original", 
  "CC0359_ge_3_58_F.nii.gz"
)
imageRange = 26
'''
image = []
imageRange = 30
for x in range(0,imageRange):
  for y in range(0,imageRange):
    for z in range(0,imageRange):
      image.append((x,y,z))
'''
mriFile = nib.load(mriFilename)
image = mriFile.get_fdata()
newImage = []
x, y, z = image.shape
factor = 10
for i in range(0,x,factor):
  newImage.append([])
  for j in range(0,y,factor):
    newImage[int(i/factor)].append([])
    for k in range(0,z,factor):
      newImage[int(i/factor)][int(j/factor)].append(image[i][j][k])

x, y, z = np.asarray(newImage).shape
maxVal = np.asarray(newImage).max()
filled = np.zeros((x, y, z))
for i in range(0,x):
  for j in range(0,y):
    for k in range(0,z):
      color = newImage[i][j][k]
      if(color > maxVal/10):
        filled[i][j][k] = min(1, color/maxVal)

print(filled)
#sys.exit()
def surfaceOnly(image):
  time1 = time.time()

  global filled
  x1 = np.zeros((20, 26, 26))
  x2 = np.zeros((20, 26, 26))
  y1 = np.zeros((20, 26, 26))
  y2 = np.zeros((20, 26, 26))
  z1 = np.zeros((20, 26, 26))
  z2 = np.zeros((20, 26, 26))
    
  time2 = time.time()

  for x in range(0,20):
    for y in range(0,26):
      for z in range(0,26):
        if(filled[x][y][z]):
          if not(x - 1 >= 0) or not(filled[x-1][y][z]):
            x1[x][y][z] = 1
          if not(x + 1 < 20) or not(filled[x+1][y][z]):
            x2[x][y][z] = 1
          if not(y - 1 >= 0) or not(filled[x][y-1][z]):
            y1[x][y][z] = 1
          if not(y + 1 < 26) or not(filled[x][y+1][z]):
            y2[x][y][z] = 1
          if not(z - 1 >= 0) or not(filled[x][y][z-1]):
            z1[x][y][z] = 1
          if not(z + 1 < 26) or not(filled[x][y][z-1]):
            z2[x][y][z] = 1

  time3 = time.time()

  print((time2 - time1)*1000)      
  print((time3 - time2)*1000)    

  return (x1, x2, y1, y2, z1, z2)

imageSurface = surfaceOnly(image)

def Voxel(origin, color, size):
  size /= 1
  global imageSurface
  global imageRange
  x, y, z = origin
  global filled
  r = g = b = filled[x][y][z]
  divisor = 3

  gl.glPushMatrix()

  gl.glColor3f(r, g, b)
  gl.glTranslatef((x-imageRange/2)/divisor, (y-imageRange/2)/divisor, (z-imageRange/2)/divisor)
  
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

    global image
    global imageRange
    global filled

    for point in image:
      x, y, z = point
      if filled[x][y][z]:
        Voxel(point, ((x)*1./imageRange,(y)*1./imageRange,(z)*1./imageRange), 1)

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
    camera = {"x": 0, "y": 0, "z": 0}
    _ = glut.glutDisplayFunc(display)
    _ = glut.glutReshapeFunc(reshape)
    _ = glut.glutKeyboardFunc(keyboard)

    glut.glutMainLoop()


if __name__ == "__main__" :
    main()
