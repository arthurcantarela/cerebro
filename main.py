from __future__ import division
from __future__ import print_function

import sys
import copy

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut


  

image = []
imageRange = 8
for x in range(-imageRange,imageRange):
  for y in range(-imageRange,imageRange):
    for z in range(-imageRange,imageRange):
      image.append((x,y,z))

# image = []
def surfaceOnly(image):
  global imageRange

  filled = []
  for x in range(-imageRange,imageRange):
    filled.append([])
    for y in range(-imageRange,imageRange):
      filled[x+imageRange].append([])
      for z in range(-imageRange,imageRange):
        filled[x+imageRange][y+imageRange].append(1 if (x,y,z) in image else 0)

  surfaceOnly = copy.deepcopy(filled)
  for x in range(-imageRange,imageRange):
    for y in range(-imageRange,imageRange):
      for z in range(-imageRange,imageRange):
        if(filled[x+imageRange][y+imageRange][z+imageRange] == 1):
          surfaceOnly[x+imageRange][y+imageRange][z+imageRange] = []
          for face in range(-1,2,2):
            if not(x + face >= -imageRange and x + face < imageRange) or not(filled[x+imageRange+face][y+imageRange][z+imageRange]):
              surfaceOnly[x+imageRange][y+imageRange][z+imageRange].append((face,0,0))
            if not(y + face >= -imageRange and y + face < imageRange) or not(filled[x+imageRange][y+imageRange+face][z+imageRange]):
              surfaceOnly[x+imageRange][y+imageRange][z+imageRange].append((0,face,0))
            if not(z + face >= -imageRange and z + face < imageRange) or not(filled[x+imageRange][y+imageRange][z+imageRange+face]):
              surfaceOnly[x+imageRange][y+imageRange][z+imageRange].append((0,0,face))

  return surfaceOnly

imageSurface = surfaceOnly(image)

def Voxel(origin, color, size):
  # size /= 2
  global imageSurface
  global imageRange
  x, y, z = origin
  r, g, b = color
  divisor = 2

  gl.glPushMatrix()

  gl.glColor3f(r, g, b)
  gl.glTranslatef(x/divisor, y/divisor, z/divisor)
  
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
  
  facesAvaiable = imageSurface[x+imageRange][y+imageRange][z+imageRange]
  if(1,0,0) in facesAvaiable: faces.append((0,1,3,2))
  if(-1,0,0) in facesAvaiable: faces.append((4,5,7,6))
  if(0,1,0) in facesAvaiable: faces.append((0,1,5,4))
  if(0,-1,0) in facesAvaiable: faces.append((2,3,7,6))
  if(0,0,1) in facesAvaiable: faces.append((0,2,6,4))
  if(0,0,-1) in facesAvaiable: faces.append((1,3,7,5))

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
    global camera
    gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
    gl.glPushMatrix()
    gl.glTranslatef(0.0, 0.0, -10.0)

    gl.glRotatef(camera["x"], 1.0, 0.0, 0.0)
    gl.glRotatef(camera["y"], 0.0, 1.0, 0.0)
    gl.glRotatef(camera["z"], 0.0, 0.0, 1.0)

    global image
    global imageRange

    for point in image:
      x, y, z = point
      Voxel(point, ((x+imageRange)*1./(imageRange*2),(y+imageRange)*1./(imageRange*2),(z+imageRange)*1./(imageRange*2)), 1)

    gl.glPopMatrix()
    glut.glutSwapBuffers()


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
