from __future__ import division
from __future__ import print_function

import sys

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut

def Voxel(origin, color, size):
  x, y, z = origin
  r, g, b = color

  gl.glPushMatrix()

  gl.glColor3f(r, g, b)
  gl.glTranslatef(x, y, z)
  
  vertices= (
    (size/2, size/2, size/2),
    (size/2, size/2, -size/2),
    (size/2, -size/2, size/2),
    (size/2, -size/2, -size/2),
    (-size/2, size/2, size/2),
    (-size/2, size/2, -size/2),
    (-size/2, -size/2, size/2),
    (-size/2, -size/2, -size/2)
  )
  faces = (
    (0,1,3,2),
    (4,5,7,6),
    (0,1,5,4),
    (2,3,7,6),
    (0,2,6,4),
    (1,3,7,5)
  )
  for face in faces:
    gl.glBegin(gl.GL_QUADS)
    for vertex in face:
      gl.glVertex3fv(vertices[vertex])
    gl.glEnd()

  gl.glPopMatrix()

def init() :
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glShadeModel(gl.GL_FLAT)
    gl.glEnable(gl.GL_DEPTH_TEST)
    


def display() :
    global camera
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glPushMatrix()
    gl.glTranslatef(0.0, 0.0, -10.0)

    gl.glRotatef(camera["x"], 1.0, 0.0, 0.0)
    gl.glRotatef(camera["y"], 0.0, 1.0, 0.0)
    gl.glRotatef(camera["z"], 0.0, 0.0, 1.0)

    for x in range(-5,5):
      for y in range(-5,5):
        for z in range(-5,5):
          point = (x, y, z)
          Voxel(point, ((x+5)*1./10.,(y+5)*1./10.,(z+5)*1./10.), 1)

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
        camera["x"] = (camera["x"] + 1) % 360
    elif key == 'X' :
        camera["x"] = (camera["x"] - 1) % 360
    elif key == 'y' :
        camera["y"] = (camera["y"] + 1) % 360
    elif key == 'Y' :
        camera["y"] = (camera["y"] - 1) % 360
    elif key == 'z' :
        camera["z"] = (camera["z"] + 1) % 360
    elif key == 'Z' :
        camera["z"] = (camera["z"] - 1) % 360
    else :
        return
    glut.glutPostRedisplay()


def main() :
    _ = glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)

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
