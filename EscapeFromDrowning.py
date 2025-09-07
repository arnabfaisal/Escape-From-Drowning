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
gravity = .15
j_p= 12.0  #player jump speed
m_s= .5 #player move speed 
on_ground=True

##################################### boxes ####################################
p_gap = 90          # avg platform vertical gap
P_MIN_SIZE = 90     # bigger platforms
P_MAX_SIZE = 140

SPAWN_XY_RANGE = 140   # how far from origin/platform column to spread
MIN_PLAYER_DIST = 140  # don't spawn too close to player

BONUS_CHANCE = 0.18    # 18% of spawns are bonus
BONUS_COLOR = (1.0, 0.9, 0.2)
NORMAL_COLOR = (1.0, 0.2, 0.2)

######################### GAME STATES VAR ############################

score = 0
best_height = 0
game_over = False  #nothing
max_p = 14            # allow more platforms in pool

on_ground=True

# Game variables  water level function
w_z = -50   # water_z
w_speed = 0.005 # water speed

w_accel = 0.00000000002 # just to make the game playable
score=0
game_over = False
max_p = 10   # max platform
p_gap = 100  #platfrom gap
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



# ======== PLATFORM HELPER FUNCTIONS ========

def make_platform(z, base_x, base_y, is_bonus=False):
    """Spawn a platform with balanced randomness (not too clustered)."""
    size = random.randint(P_MIN_SIZE, P_MAX_SIZE)

    # Horizontal spread: wide enough to look random, but not too far
    spread = 120 if not is_bonus else 180
    x = base_x + random.uniform(-spread, spread)
    y = base_y + random.uniform(-spread, spread)

    # Random colors
    if is_bonus:
        color = BONUS_COLOR
    else:
        color = (random.random(), random.random(), random.random())

    return {
        "x": x, "y": y, "z": z, "size": size,
        "bonus": is_bonus, "visited": False, "color": color
    }

def init_platforms():
    """Initialize the starting ground and first staircase of platforms."""
    plats = []
    # Big starting ground
    plats.append({"x": 0, "y": 0, "z": 0, "size": 220,
                  "bonus": False, "visited": False, "color": (0.6, 0.6, 0.6)})

    # Start a staircase upward
    z = 80
    last_x, last_y = 0, 0
    for _ in range(9):
        is_bonus = (random.random() < BONUS_CHANCE)
        new_plat = make_platform(z, last_x, last_y, is_bonus)
        plats.append(new_plat)

        # update base for next step (main path always reachable)
        last_x, last_y = new_plat["x"], new_plat["y"]

        # keep vertical gap within jumpable range
        max_jump_height = j_p * 3   # safe max
        z += min(p_gap + random.uniform(-10, 10), max_jump_height)

    return plats

platforms = init_platforms()





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
    global px, py, ptheta, player_velo_z, pz, on_ground, w_z, w_speed, game_over, w_accel,score

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
        score = 0
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


# ======== PLATFORM SUPPORT & SPAWNING  ========
def platform_top_if_supported(x, y, z):
    """
    Returns (is_supported, plat_index, top_z) if the player is within a platform's X/Y
    and near its top surface.
    """
    for i, p in enumerate(platforms):
        half = p["size"] * 0.5
        if (p["x"] - half <= x <= p["x"] + half and
            p["y"] - half <= y <= p["y"] + half):
            top = p["z"] + half
            # Only allow support if player is above or slightly below top
            if z >= top - 5.0:  
                return True, i, top
    return False, -1, 0.0


def highest_platform_z():
    return max(p["z"] + p["size"] * 0.5 for p in platforms)

def prune_old_platforms(water_z):
    # remove platforms far below water to keep list short
    keep = []
    cutoff = water_z - 200
    for p in platforms:
        if p["z"] + p["size"] * 0.5 >= cutoff:
            keep.append(p)
    return keep

def maybe_spawn_more():
    """Spawn platforms with fair gaps and less clustering."""
    global platforms
    top = highest_platform_z()
    last_x, last_y = platforms[-1]["x"], platforms[-1]["y"]

    while top < pz + 500:
        max_jump_height = j_p * 3

        # Bigger, more natural vertical gaps (100–160)
        vertical_gap = random.uniform(100, 160)
        top += min(vertical_gap, max_jump_height)

        # Main guaranteed platform
        main_plat = make_platform(top, last_x, last_y)
        platforms.append(main_plat)

        # Only sometimes shift base → prevents “cluster piles”
        if random.random() < 0.6:
            last_x, last_y = main_plat["x"], main_plat["y"]

        # Bonus platform (rare & scattered wider)
        if random.random() < BONUS_CHANCE * 0.5:
            bonus = make_platform(top, last_x, last_y, is_bonus=True)
            platforms.append(bonus)


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
    distance = 200
    height = 100

    cam_x = px - distance * math.cos(math.radians(ptheta))
    cam_y = py - distance * math.sin(math.radians(ptheta))
    cam_z = pz + height

    gluLookAt(cam_x, cam_y, cam_z,
              px, py, pz + 30,  # Look at player's upper body
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
    global player_velo_z, pz, on_ground, w_z, w_speed, game_over, score, best_height, platforms

    if game_over:
        glutPostRedisplay()
        return

    changing_position_smoothly()

    # Determine if player is still supported after horizontal move
    supported, sup_i, sup_top = platform_top_if_supported(px, py, pz)
    if on_ground:
        # If we walked off the platform bounds, start falling
        if not supported or pz > sup_top + 0.5:
            on_ground = False
        else:
            # stay glued to top
            pz = sup_top
            player_velo_z = 0.0

    if not on_ground:
        old_pz = pz
        player_velo_z -= gravity
        pz += player_velo_z

        # Landing check: descending through a top surface within bounds
        landed, li, ltop = platform_top_if_supported(px, py, old_pz)
        if landed and old_pz >= ltop and pz <= ltop and player_velo_z <= 0.0:
            pz = ltop
            player_velo_z = 0.0
            on_ground = True

            # SCORING on first touch
            plat = platforms[li]
            if not plat["visited"]:
                plat["visited"] = True
                score += 10 if plat["bonus"] else 1

    # Keep above ground plane
    if pz < 0:
        pz = 0
        player_velo_z = 0
        on_ground = True

    # Water progresses
    w_z += w_speed
    w_speed += w_accel

    if pz <= w_z:
        game_over = True

    # Height best for HUD
    best_height = max(best_height, int(math.ceil(pz)))

    # Spawn / prune platforms over time
    platforms = prune_old_platforms(w_z)
    maybe_spawn_more()

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
    
    for p in platforms:
        glPushMatrix()
        glColor3f(*p["color"])
        glTranslatef(p["x"], p["y"], p["z"])
        glutSolidCube(p["size"])
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
    #glEnable(GL_DEPTH_TEST)
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