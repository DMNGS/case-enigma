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
TRIG = 16
ECHO = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LEFT, GPIO.IN)
GPIO.setup(PIN_DOWN, GPIO.IN)
GPIO.setup(PIN_UP, GPIO.IN)
GPIO.setup(PIN_RIGHT, GPIO.IN)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
font = pygame.font.SysFont('freesansbold.ttf', 32)

down_color = COLOR_OFF
left_color = COLOR_OFF
right_color = COLOR_OFF
up_color = COLOR_OFF
pressed = True
guess = ''

level = 0
 
running = True
# Level 1 : Make a code with the D-pad on the bottom right of the CrowPi 
def d_pad_code():
    CODE = 'UUDDLRLR'
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
    pressed = True if not GPIO.input(PIN_LEFT) or not GPIO.input(PIN_DOWN) or not GPIO.input(PIN_UP) or not GPIO.input(PIN_RIGHT) else False
    
    if len(guess) > 0 and guess[len(guess)-1] != CODE[len(guess)-1]:
        guess = ''
        
    if guess == CODE:
        solved = True
    
    # Draw D-Pad
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, left_color, (100, 250), 75)
    pygame.draw.circle(screen, down_color, (250, 400), 75)
    pygame.draw.circle(screen, up_color, (250, 100), 75)
    pygame.draw.circle(screen, right_color, (400, 250), 75)
    
    return solved

# Level 2 : Put your hand at the right distance form the sensor
def distance():
    RIGHT_DITANCE = 500
    GOAL_DIST = 25
    DELTA = 1
    cur_dist = 0
    right_dist = False
    
    # Wait for sensor to settle
    GPIO.output(TRIG, False)
    time.sleep(2)

    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
        
    while GPIO.input(ECHO)==0:
        pulse_start = time.time()

    while GPIO.input(ECHO)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    
    text = font.render(str(distance), True, (0, 0, 0 ))
    text_rect = text.get_rect();
    text_rect.center = (250, 250)
    
    screen.fill((255, 255, 255))
    screen.blit(text, text_rect)
    
    if distance < GOAL_DIST + DELTA and distance > GOAL_DIST - DELTA:
        right_dist = True
        
    return right_dist
    
while running:
    # Close the game when the event is triggered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if level == 0:
        if d_pad_code():
            level = 1
    elif level == 1:
        if distance():
            level = 2
    else:
        running = False
            
    pygame.display.flip()
    
GPIO.cleanup()
pygame.quit()
