from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GLUT import GLUT_BITMAP_HELVETICA_18

import math

# Camera-related variables
mode_camera = 0 
camera_pos = (0,500,500)
angle_camera=0
height_camera = 250
fovY = 120  # Field of view
GRID_LENGTH = 600  # Length of grid lines
rand_var = 423
r_step=5.0

SCALE_of_player= 0.6

fpm = False
########################### SECTION FOR DECLARING VARIABLES #################################
#p = player
px, py, pz, ptheta = 0, 0,50.0,0
player_velo_z=0.0
gravity = 0.3
j_p=15.0  #jump speed
m_s= 5.0 #move speed 
on_ground=True

# Game variables
w_z = -100   # water_z
w_speed = 0.005 # water speed

w_accel = 0.0 # just to make the game playable
score=0
game_over = False
platforms = [
    (0, 0, 0, 100),
    (150, 100, 100, 80),
    (-200, -150, 200, 60),
    (250, -200, 300, 50),
    (-100, 300, 400, 40),
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
    glTranslatef(px, py, 0)
    glRotatef(ptheta, 0, 0, 1)

    # Legs
    glColor3f(0, 0, 1) 
    
    # Left leg
    glPushMatrix()
    glTranslatef(0, -20, 0) 

    gluCylinder(gluNewQuadric(), 10, 30, 40, 10, 10)
    glPopMatrix()
    
    # Right leg
    glPushMatrix()
    glTranslatef(0,20, 0)

    gluCylinder(gluNewQuadric(), 10, 30, 40, 10, 10)
    glPopMatrix()

    # Body
    glPushMatrix()
    glColor3f(2/255, 48/255, 32/255) 
    glTranslatef(0, 0, 80)  
    glutSolidCube(80)
    glPopMatrix()

    # Head
    glPushMatrix()
    glColor3f(0, 0, 0)  
    glTranslatef(0, 0, 140)  
    gluSphere(gluNewQuadric(), 20, 10, 10)  
    glPopMatrix()

    r,g,b = (255,224,196)
    r = r/255
    g = g/255
    b = b/255
    glColor3f(r,g,b)  

    # First hand (right side)
    glPushMatrix()
    glTranslatef(40, -40, 80)  
    glRotatef(90, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 15, 5, 50, 10, 10) 
    glPopMatrix()
    
    # Second hand (left side)
    glPushMatrix()
    glTranslatef(40, 40, 80)  
    glRotatef(90, 0, 1, 0)  
    gluCylinder(gluNewQuadric(), 15, 5, 50, 10, 10)  
    glPopMatrix()


    glPopMatrix()  


def keyboardListener(key, x, y):
    """
    Handles keyboard inputs for player movement, gun rotation, camera updates, and cheat mode toggles.
    """
    global px, py, ptheta, player_velo_z, pz, on_ground, w_z, w_speed, game_over,w_accel
    rad = math.radians(ptheta)
    dir_x = math.cos(rad)
    dir_y = math.sin(rad)
    left_x = -dir_y
    left_y = dir_x

    if key == b'w':
        px += dir_x * m_s
        py += dir_y * m_s
    if key == b's':
        px -= dir_x * m_s
        py -= dir_y * m_s
    if key == b'a':
        ptheta -= 5

    if key == b'd':
        ptheta += 5

    if key == b'q':  # Strafe left
        px += left_x * m_s
        py += left_y * m_s
    if key == b'e':  # Strafe right
        px -= left_x * m_s
        py -= left_y * m_s
    if key == b' ' and on_ground:
        player_velo_z = j_p
        on_ground = False
    if key == b'r':
        px, py, pz = 0, 0, 50
        ptheta = 0
        player_velo_z = 0
        on_ground = True
        w_z = -100
        w_s = 0.005
        w_accel=0.0
        game_over = False
        global angle_camera, fovY
        angle_camera = 0
        fovY = 120
    glutPostRedisplay()
    


    # # Move forward (W key)
    # if key == b'w':  

    # # Move backward (S key)
    # if key == b's':

    # # Rotate gun left (A key)
    # if key == b'a':

    # # Rotate gun right (D key)
    # if key == b'd':

    # # Toggle cheat mode (C key)
    # if key == b'c':

    # # Toggle cheat vision (V key)
    # if key == b'v':

    # # Reset the game if R key is pressed
    # if key == b'r':


def specialKeyListener(key, x, y):
    """
    Handles special key inputs (arrow keys) for adjusting the camera angle and height.
    """
    global camera_pos, fovY,angle_camera, mode_camera, height_camera,px, py, ptheta, player_velo_z, pz, on_ground, w_z, w_speed, game_over
    #x, y, z = camera_pos

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
        fovY += 1
    if key == GLUT_KEY_DOWN:
        fovY -= 1
  
    if key == GLUT_KEY_LEFT:
        angle_camera -= r_step
        if angle_camera < 0:
            angle_camera += 360
    if key == GLUT_KEY_RIGHT:
        angle_camera += r_step
        if angle_camera >= 360:
            angle_camera -= 360


   

   

    #camera_pos = (x, y, z)
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global fpm
    """
    Handles mouse inputs for firing bullets (left click) and toggling camera mode (right click).
    """
        # # Left mouse button fires a bullet
        # if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:

        # # Right mouse button toggles camera tracking mode
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fpm = not fpm
    glutPostRedisplay()


#def setupCamera():
    #global mode_camera, angle_camera, height_camera, px,py,pz, ptheta
    """
    Configures the camera's projection and view settings.
    Uses a perspective projection and positions the camera to look at the target.
    """
    #glMatrixMode(GL_PROJECTION)  # Switch to projection matrix mode
    #glLoadIdentity()  # Reset the projection matrix
    # Set up a perspective projection (field of view, aspect ratio, near clip, far clip)
    #gluPerspective(fovY, 1.25, 0.1, 1500) # Think why aspect ration is 1.25?
    #glMatrixMode(GL_MODELVIEW)  # Switch to model-view matrix mode
    #glLoadIdentity()  # Reset the model-view matrix

    #Extract camera position and look-at target
   
def fpmChanger():
    x = px + 60*math.cos(math.radians(ptheta))
    y = py + 60*math.sin(math.radians(ptheta))
    z = 100 

    secondx = x + math.cos(math.radians(ptheta))
    secondy = y + math.sin(math.radians(ptheta))

    gluLookAt(x, y, z,
            secondx, secondy, z,
            0, 0, 1)
    
def setupCamera():
    global fpm, px, py,pz, ptheta,angle_camera,height_camera,camera_pos

    glMatrixMode(GL_PROJECTION) 
    glLoadIdentity()

    gluPerspective(fovY, 1.25, 0.1, 1500) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if not fpm:
        # Third-person: Rotate around player
        radius = 600
        cam_x = px + radius * math.cos(math.radians(angle_camera))
        cam_y = py + radius * math.sin(math.radians(angle_camera))
        cam_z = height_camera
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
    # Clear color and depth buffers
    #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    #glLoadIdentity()  # Reset modelview matrix
    #glViewport(0, 0, 1000, 800)  # Set viewport size

    #setupCamera()  # Configure camera perspective


    # Display game info text at a fixed screen position
    #draw_text(10, 770, f"A Random Fixed Position Text")
    #draw_text(10, 740, f"See how the position and variable change?: {rand_var}")
    #drawHero()
    # Swap buffers for smooth rendering (double buffering)
    #glutSwapBuffers()
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
        glColor3f(0.5, 0.5, 0.5)
        glTranslatef(plat_x, plat_y, plat_z)
        glutSolidCube(plat_size)
        glPopMatrix()
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
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glutDisplayFunc(showScreen)  # Register display function
    glutKeyboardFunc(keyboardListener)  # Register keyboard listener
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)  # Register the idle function to move the bullet automatically

    glutMainLoop()  # Enter the GLUT main loop

if __name__ == "__main__":
    main()