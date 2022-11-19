import pygame
import RPi.GPIO as GPIO
import time

# Initialize Pygame screen
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Initialize d-pad
PIN_LEFT = 25
PIN_DOWN = 13
PIN_UP = 26
PIN_RIGHT = 19
PIN_TRIG = 16
PIN_ECHO = 12
PIN_TOUCH = 17

# Setup GPIO PINs
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LEFT, GPIO.IN)
GPIO.setup(PIN_DOWN, GPIO.IN)
GPIO.setup(PIN_UP, GPIO.IN)
GPIO.setup(PIN_RIGHT, GPIO.IN)
GPIO.setup(PIN_TRIG,GPIO.OUT)
GPIO.setup(PIN_ECHO,GPIO.IN)
GPIO.setup(PIN_TOUCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Setup Display and main font
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.SysFont('freesansbold.ttf', 32)

# Global variables
pressed = True
guess = ''
elapsed = 0

level = 1

# Verifies if the guess is correct compared to the code
def check_guess(inp, code):
    print(code)
    print(inp)
    if (len(inp) > 0 and inp[len(inp)-1] != code[len(inp)-1])\
       or guess == code:
        return False
    else:
        return True

# Level 1 : Make a code with the D-pad on the bottom right of the CrowPi 
def d_pad_code():
    CODE = 'UUDDLRLR'
    COLOR_OFF = (0, 150, 0)
    COLOR_ON = (0, 255, 0)
    
    global pressed, guess # Global so they don't reset every time the function is called
    solved = False
    left_color = COLOR_ON if not GPIO.input(PIN_LEFT) else COLOR_OFF    
    down_color = COLOR_ON if not GPIO.input(PIN_DOWN) else COLOR_OFF    
    up_color = COLOR_ON if not GPIO.input(PIN_UP) else COLOR_OFF    
    right_color = COLOR_ON if not GPIO.input(PIN_RIGHT) else COLOR_OFF
    
    # Check which button was pressed
    guess += 'L' if not GPIO.input(PIN_LEFT) and not pressed else ''    
    guess += 'D' if not GPIO.input(PIN_DOWN) and not pressed else ''    
    guess += 'U' if not GPIO.input(PIN_UP) and not pressed else ''    
    guess += 'R' if not GPIO.input(PIN_RIGHT) and not pressed else ''
    
    # Only check input only when pressed
    pressed = True if not GPIO.input(PIN_LEFT)\
                or not GPIO.input(PIN_DOWN)\
                or not GPIO.input(PIN_UP)\
                or not GPIO.input(PIN_RIGHT) else False
    
    if guess == CODE:
        solved = True
    
    # Make player try again or clean variables for future use
    print(guess)
    if not check_guess(guess, CODE):
        guess = ''
        pressed = False
    
    # Draw D-Pad
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, left_color, (100, 250), 75)
    pygame.draw.circle(screen, down_color, (250, 400), 75)
    pygame.draw.circle(screen, up_color, (250, 100), 75)
    pygame.draw.circle(screen, right_color, (400, 250), 75)
    
    return solved

# Level 2 : Put your hand at the right distance form the sensor
def distance():
    GOAL_DIST = 15
    DELTA = 1
    TEXT_TOO_HIGH = 'Too high'
    TEXT_TOO_LOW = 'Too low'
    TEXT_RIGHT = 'Correct'
    
    right_dist = False
    
    # Wait for sensor to settle
    GPIO.output(PIN_TRIG, False)
    time.sleep(2)

    GPIO.output(PIN_TRIG, True)
    time.sleep(0.00001)
    GPIO.output(PIN_TRIG, False)
        
    while GPIO.input(PIN_ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(PIN_ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    dist = pulse_duration * 17150
    dist = round(dist, 2)
    print(dist)
    
    # Check if the sensor gives the right value
    # and choose the text accordingly
    if dist < GOAL_DIST + DELTA and dist > GOAL_DIST - DELTA:
        text = TEXT_RIGHT
        right_dist = True
    elif dist < GOAL_DIST - DELTA:
        text = TEXT_TOO_LOW
    else:
        text = TEXT_TOO_HIGH
    
    # Create the object and rectangle for the text
    text_obj = font.render(text, True, (0, 0, 0 ))
    text_rect = text_obj.get_rect();
    text_rect.center = (250, 250)
    
    # Display the text
    screen.fill((255, 255, 255))
    screen.blit(text_obj, text_rect)
        
    return right_dist

# Level 3 : make a morse code using the touch sensor
def morse_code():
    global guess
    guessed = False
    CODE='ssslllsss'
    DOT_TIME = 200
    DASH_TIME = 700
    DELTA = 100
    global elapsed
    
    if elapsed > 0:
        print(elapsed)
        if elapsed < DOT_TIME + DELTA\
           and elapsed > DOT_TIME > DOT_TIME - DELTA:
            guess += 's'
        elif elapsed > DOT_TIME > DOT_TIME - DELTA:
            guess += 'l'
            
        if guess == CODE:
            guessed = True
            
        if not check_guess(guess, CODE):
            guess = ''
            print(guess)
            
        elapsed = 0
    
    # Draw graphics
    screen.fill((255, 255, 255))
    # Create the object and rectangle for the text
    text_obj = font.render("TODO", True, (0, 0, 0 ))
    text_rect = text_obj.get_rect();
    text_rect.center = (250, 250)
    
    # Display the text
    screen.fill((255, 255, 255))
    screen.blit(text_obj, text_rect)
    
    return guessed

# Callback for the sensor to have accurate mesurment
def morse_callback(channel):
    if level == 3:
        global start, end, elapsed
        
        if GPIO.input(PIN_TOUCH) == 1:
            start = time.time()
        if GPIO.input(PIN_TOUCH) == 0:
            end = time.time()
            elapsed = (end - start) * 1000 # Measure in [ms] instead of [s]
            
# Add event detector for the touch sensor
GPIO.add_event_detect(PIN_TOUCH, GPIO.BOTH, callback=morse_callback, bouncetime=200)
    
# Main game loop
running = True
while running:
    # Close the game when the event is triggered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if level == 1:
        if d_pad_code():
            level = 2
    elif level == 2:
        if distance():
            level = 3
    elif level == 3:
        if morse_code():
            level = 4
    else:
        running = False
            
    pygame.display.flip()
    
GPIO.cleanup()
pygame.quit()
