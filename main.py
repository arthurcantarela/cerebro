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
  
  gl.glBegin(gl.GL_LINES)
  vertices= (
    (size/2, -size/2, -size/2),
    (size/2, size/2, -size/2),
    (-size/2, size/2, -size/2),
    (-size/2, -size/2, -size/2),
    (size/2, -size/2, size/2),
    (size/2, size/2, size/2),
    (-size/2, -size/2, size/2),
    (-size/2, size/2, size/2)
  )
  edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
  )
  for edge in edges:
    for vertex in edge:
      gl.glVertex3fv(vertices[vertex])
  gl.glEnd()

  gl.glPopMatrix()

def init() :
    gl.glClearColor(0.0, 0.0, 0.0, 0.0)
    gl.glShadeModel(gl.GL_FLAT)


def display() :
    global camera
    gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    gl.glPushMatrix()
    gl.glRotatef(camera, 1.0, 0.0, 0.0)

    resolution = .5
    points = [
      (0,0,resolution),
      (0,resolution,0),
      (-resolution,0,0),
      (0,0,0),
      (resolution,0,0),
      (0,-resolution,0),
      (0,0,-resolution)
    ]
    for point in points:
      Voxel(point, (1,0,0), resolution)

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
    if key == 'c' :
        camera = (camera + 10) % 360
    elif key == 'C' :
        camera = (camera - 10) % 360
    else :
        return
    glut.glutPostRedisplay()


def main() :
    _ = glut.glutInit(sys.argv)
    glut.glutInitDisplayMode(glut.GLUT_DOUBLE | glut.GLUT_RGB)

    glut.glutInitWindowSize(500, 500)
    glut.glutInitWindowPosition(100, 100)
    _ = glut.glutCreateWindow(sys.argv[0])

    init()

    global camera
    camera = 0
    _ = glut.glutDisplayFunc(display)
    _ = glut.glutReshapeFunc(reshape)
    _ = glut.glutKeyboardFunc(keyboard)

    glut.glutMainLoop()


if __name__ == "__main__" :
    main()
