from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18
import random
import math

# Camera-related variables
mode_camera = 0 
camera_pos = (0,500,500)
angle_camera=0
height_camera = 250
fovY = 120  # Field of view
GRID_LENGTH = 1200  # Length of grid lines
rand_var = 423
r_step=5.0

SCALE_of_player= 0.6

fpm = False
########################### SECTION FOR DECLARING VARIABLES #################################
#p = player
px, py, pz, ptheta = 0, 0,50.0,0
player_velo_z=0.0
gravity = .5
j_p= 15.0  #player jump speed
m_s= .5 #player move speed 
on_ground=True

# Game variables
w_z = -50   # water_z
w_speed = 0.005 # water speed

w_accel = 0.00000000002 # just to make the game playable
score=0
game_over = False
max_p = 10   # max platform
p_gap = 80  #platfrom gap
p_size=80
platforms = [
    (0, 0, 0, 100),
    (random.uniform(-100, 100), random.uniform(-100, 100), 80, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 160, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 240, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 320, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 400, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 480, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 560, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 640, p_size),
    (random.uniform(-100, 100), random.uniform(-100, 100), 720, p_size),
]

########################### DRAW TEXT #################################

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    
    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    
    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

########################## DRAW HERO ##############################
def drawHero():
    global px, py, ptheta

    glPushMatrix()
    glTranslatef(px, py, pz)
    glRotatef(ptheta, 0, 0, 1)

    # Legs
    glColor3f(0, 0, 1) 
    
    # Left leg
    glPushMatrix()
    glTranslatef(0, -20, 0) 

    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(0,20, 0)

    gluCylinder(gluNewQuadric(), 10, 15, 60, 10, 10)
    glPopMatrix()

    # Body
    glPushMatrix()
    glColor3f(255/255, 182/255, 193/255) 
    glTranslatef(0, 0, 80)  
    glutSolidCube(60)
    glPopMatrix()

    # Head
    glPushMatrix()
    glColor3f(1, 1, 1)  
    glTranslatef(0, 0, 130)  
    gluSphere(gluNewQuadric(), 15, 10, 10)  
    glPopMatrix()

    r,g,b = (255,224,196)
    r = r/255
    g = g/255
    b = b/255
    glColor3f(r,g,b)  

    # First hand (right side)
    glPushMatrix()
    glTranslatef(20, -30, 80)  
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 10, 5, 30, 10, 10)  
    glPopMatrix()

    # Second hand (left side)
    glPushMatrix()
    glTranslatef(20, 60, 80)  
    glRotatef(90, 1, 0, 0)  
    gluCylinder(gluNewQuadric(), 5, 10, 30, 10, 10)  
    glPopMatrix()


    glPopMatrix()  

########################## BOUNDARY 333333333333333333333
def drawBoundary():
    global w_z
    glBegin(GL_QUADS)
    glColor3f(0.8, 0.3, 0.9)

    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH,  GRID_LENGTH, 0)
    glVertex3f(-GRID_LENGTH,  GRID_LENGTH, 200)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 200)

    glColor3f(0.2, 0.7, 0.6)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH,  GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH,  GRID_LENGTH, 200)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 200)

    glColor3f(0.3, 0.3, 0.9)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, GRID_LENGTH, 200)
    glVertex3f(-GRID_LENGTH, GRID_LENGTH, 200)

    glColor3f(0.4, 0.9, 0.2)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 0)
    glVertex3f(GRID_LENGTH, -GRID_LENGTH, 200)
    glVertex3f(-GRID_LENGTH, -GRID_LENGTH, 200)

    glEnd()


# Movement control variables
mv_w = False
mv_s = False
mv_l = False
mv_r = False
mv_sl = False
mv_sr = False

def keyboardListener(key, x, y):
    """
    Handles keyboard key presses.
    """
    global mv_w, mv_s, mv_l, mv_r, mv_sl, mv_sr
    global px, py, ptheta, player_velo_z, pz, on_ground, w_z, w_speed, game_over, w_accel

    if key == b'w':
        mv_w = True
    elif key == b's':
        mv_s = True
    elif key == b'a':
        mv_l = True
    elif key == b'd':
        mv_r = True
    elif key == b'q':
        mv_sl = True
    elif key == b'e':
        mv_sr = True
    elif key == b' ' and on_ground:
        player_velo_z = j_p
        on_ground = False
    elif key == b'r':
        # Reset game
        px, py, pz = 0, 0, 50
        ptheta = 0
        player_velo_z = 0
        on_ground = True
        w_z = -100
        w_s = 0.005
        w_accel = 0.0
        game_over = False
        global angle_camera, fovY
        angle_camera = 0
        fovY = 120
        
    glutPostRedisplay()

def keyboardUpListener(key, x, y):
    """
    Handles keyboard key releases.
    """
    global mv_w, mv_s, mv_l, mv_r, mv_sl, mv_sr

    if key == b'w':
        mv_w = False
    elif key == b's':
        mv_s = False
    elif key == b'a':
        mv_l = False
    elif key == b'd':
        mv_r = False
    elif key == b'q':
        mv_sl = False
    elif key == b'e':
        mv_sr = False
        
    glutPostRedisplay()

def changing_position_smoothly():
    global px, py, ptheta, mv_w, mv_s, mv_l, mv_r, mv_sl, mv_sr, m_s
    
    rad = math.radians(ptheta)
    dir_x = math.cos(rad)
    dir_y = math.sin(rad)
    left_x = -dir_y
    left_y = dir_x

    # Process continuous movement based on key states
    if mv_w:
        px += dir_x * m_s
        py += dir_y * m_s
    if mv_s:
        px -= dir_x * m_s
        py -= dir_y * m_s
    if mv_l:
        ptheta -= .5
    if mv_r:
        ptheta += .5
    if mv_sl:
        px += left_x * m_s
        py += left_y * m_s
    if mv_sr:
        px -= left_x * m_s
        py -= left_y * m_s


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, fovY,angle_camera, mode_camera, height_camera,px, py, ptheta, player_velo_z, pz, on_ground, w_z, w_speed, game_over, cam_z

    s = 10  # height step
    r_step = 3 # rotation step for camera
    # Move camera up (UP arrow key)

    #if key == GLUT_KEY_UP:
        #fovY += 1

    # # Move camera down (DOWN arrow key)
    #if key == GLUT_KEY_DOWN:
        #fovY -= 1
    #if key == GLUT_KEY_LEFT:
       # px -= m_s
    #if key == GLUT_KEY_RIGHT:
       # px += m_s

    rad = math.radians(ptheta)
    
    if key == GLUT_KEY_UP:
        height_camera += 10

    if key == GLUT_KEY_DOWN:
        height_camera -= 10

  
    if key == GLUT_KEY_LEFT:
        angle_camera -= r_step
        if angle_camera < 0:
            angle_camera += 360
    if key == GLUT_KEY_RIGHT:
        angle_camera += r_step
        if angle_camera >= 360:
            angle_camera -= 360

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global fpm
    
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fpm = not fpm
    glutPostRedisplay()

   
def fpmChanger():
    x = px + 60*math.cos(math.radians(ptheta))
    y = py + 60*math.sin(math.radians(ptheta))
    z = pz

    secondx = x + math.cos(math.radians(ptheta))
    secondy = y + math.sin(math.radians(ptheta))

    gluLookAt(x, y, z,
            secondx, secondy, z,
            0, 0, 1)
    


cam_x = 0
cam_y = 0
cam_z = 0
def setupCamera():
    global fpm, px, py,pz, ptheta,angle_camera,height_camera,cam_x, cam_y, cam_z

    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()

    gluPerspective(fovY, 1.25, 0.1, 2000) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if not fpm:
        # Third-person: Rotate around player
        radius = 600
        cam_x = px + radius * math.cos(math.radians(angle_camera))
        cam_y = py + radius * math.sin(math.radians(angle_camera))
        cam_z = pz + height_camera
        gluLookAt(cam_x, cam_y, cam_z,
                  px, py, pz+15,  # Look at player with z-offset
                  0, 0, 1)
    else:
        # First-person
        fpmChanger()


def idle():
    """
    Idle function that runs continuously:
    - Triggers screen redraw for real-time updates.
    """
    # Ensure the screen updates with the latest changes
    global player_velo_z, pz, on_ground, w_z, w_speed, game_over,score
    changing_position_smoothly()
    if game_over:
        glutPostRedisplay()
        return
    old_pz=pz
    player_velo_z -= gravity
    pz += player_velo_z
    
    if on_ground:
       for plat_x, plat_y, plat_z, plat_size in platforms:
            half_size = plat_size / 2
            plat_top = plat_z + half_size
            if (plat_x - half_size <= px <= plat_x + half_size and
                plat_y - half_size <= py <= plat_y + half_size and
                pz < plat_top):
                pz = plat_top
                player_velo_z = 0
                on_ground = True
                break
    else:
       for plat_x, plat_y, plat_z, plat_size in platforms:
            half_size = plat_size / 2
            plat_top = plat_z + half_size
            if (plat_x - half_size <= px <= plat_x + half_size and
                plat_y - half_size <= py <= plat_y + half_size and
                old_pz >= plat_top and
                pz < plat_top and
                player_velo_z <= 0):
                pz = plat_top
                player_velo_z = 0
                on_ground = True
                break
   
    # not falling below ground
    if pz < 0:
        pz = 0
        player_velo_z = 0
        on_ground = True
    w_z += w_speed
    w_speed += w_accel
    if pz <= w_z:
        game_over = True
    glutPostRedisplay()

  
    #glutPostRedisplay()
    score = max(score, int(pz))
    glutPostRedisplay()


def showScreen():
    """
    Display function to render the game scene:
    - Clears the screen and sets up the camera.
    - Draws everything of the screen
    """

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()

    
    glBegin(GL_QUADS)
    glColor4f(0.0, 0.5, 1.0, 0.8)  # Blue water
    glVertex3f(-1000, -1000, w_z)
    glVertex3f(1000, -1000, w_z)
    glVertex3f(1000, 1000, w_z)
    glVertex3f(-1000, 1000, w_z)
    glEnd()

    for plat_x, plat_y, plat_z, plat_size in platforms:
        glPushMatrix()
        glColor3f(1, 0, 0)
        glTranslatef(plat_x, plat_y, plat_z)
        glutSolidCube(plat_size)
        glPopMatrix()
    
    drawBoundary()
    drawHero()
    draw_text(10, 770, f"Player Height: {pz:.1f}")
    draw_text(10, 740, f"Water Level: {w_z:.1f}")
    draw_text(10, 710, f"Player Angle: {ptheta:.1f}")
    draw_text(10, 680, f"Score: {score}")
    if game_over:
        draw_text(400, 400, "Game Over - Press R to Restart")
    glutSwapBuffers()


# Main function to set up OpenGL window and loop
def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)  # Double buffering, RGB color, depth test
    glutInitWindowSize(1000, 800)  # Window size
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Michael Phelps RISING WATER ESCAPE")  # Create the window
    # glEnable(GL_DEPTH_TEST)
    # glEnable(GL_BLEND)

    # glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutKeyboardUpFunc(keyboardUpListener)  # Register key up listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()