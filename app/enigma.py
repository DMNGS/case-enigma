# Script : enigma.py
# Description : CrowPi puzzle game
# Author : DOMIGNUES PEDROSA Samuel
# Date : 2022.09.29, V0.0
# Date : 2022.11.20, V1.0

import pygame
import RPi.GPIO as GPIO
import time

# Initialize Pygame screen
pygame.init()
pygame.display.set_caption('Authentificator')
# Setup Display and main font
screen = pygame.display.set_mode((600, 550))
font = pygame.font.SysFont('freesansbold.ttf', 32)

# Initialize PIN numbers
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

# Global variables
pressed = True
guess = ''
tries = 1
elapsed = 0

level = 1

# Verifies if the guess is correct compared to the code
def check_guess(inp, code):
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
    
    TEXT_QUESTION = 'Please entrer your contract code'
    TEXT_HINT = 'Are you stuck at contract? Enter the code!'
    solved = False
    
    global pressed, guess, tries
    
    # Set colors depending on button pressed
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
        tries = 0
    
    # Make player try again or clean variables for future use
    if not check_guess(guess, CODE):
        guess = ''
        tries += 1
        pressed = False
    
    # Draw D-Pad
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, left_color, (100, 300), 75)
    pygame.draw.circle(screen, down_color, (250, 450), 75)
    pygame.draw.circle(screen, up_color, (250, 150), 75)
    pygame.draw.circle(screen, right_color, (400, 300), 75)
    
    # Display text
    text_question = font.render('Layer 1 : ' + TEXT_QUESTION, True, (0, 0, 0))
    question_rect = text_question.get_rect()
    question_rect.center = (230, 25)
    # Display the text
    screen.blit(text_question, question_rect)
    
    # Display hint text
    if tries >= 4:
        text_question = font.render(TEXT_HINT, True, (0, 0, 0))
        question_rect = text_question.get_rect()
        question_rect.center = (230, 55)
        screen.blit(text_question, question_rect)
    
    return solved

# Level 2 : Put your hand at the right distance form the sensor
def distance():
    GOAL_DIST = 15
    DELTA = 1
    
    TEXT_TOO_HIGH = 'Too high'
    TEXT_TOO_LOW = 'Too low'
    TEXT_RIGHT = 'Correct'
    TEXT_QUESTION = 'Palm Scanner, please put your hand at the right distance'
    TEXT_HINT = 'A quarter of a minutes already passed.'
    
    right_dist = False
    global tries
    
    # Wait for sensor to settle
    GPIO.output(PIN_TRIG, False)
    time.sleep(2)
    tries += 1

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
    
    # Check if the sensor gives the right value
    # and choose the text accordingly
    if dist < GOAL_DIST + DELTA and dist > GOAL_DIST - DELTA:
        text = TEXT_RIGHT
        right_dist = True
        tries = 1
    elif dist < GOAL_DIST - DELTA:
        text = TEXT_TOO_LOW
    else:
        text = TEXT_TOO_HIGH
    
    # Create the object and rectangle for the text
    text_obj = font.render(text, True, (0, 0, 0))
    text_rect = text_obj.get_rect()
    text_rect.center = (250, 250)
    # Display the text
    screen.fill((255, 255, 255))
    screen.blit(text_obj, text_rect)
    
    # Question text
    text_question = font.render('Layer 2 : ' + TEXT_QUESTION, True, (0, 0, 0))
    question_rect = text_question.get_rect()
    question_rect.center = (250, 25)
    screen.blit(text_question, question_rect)
    
    # Display hint text
    if tries >= 7: # After 16 sec (closest to 15
        text_question = font.render(TEXT_HINT, True, (0, 0, 0))
        question_rect = text_question.get_rect()
        question_rect.center = (230, 55)
        screen.blit(text_question, question_rect)
        
    return right_dist

# Level 3 : make a morse code using the touch sensor
def morse_code():
    guessed = False
    CODE='...---...'
    DOT_TIME = 200
    DASH_TIME = 600
    DELTA = 100
    
    TEXT_QUESTION = 'Enter fingerprint code'
    TEXT_HINT = "It wasn't 1234 but it was equivalent"
    
    global guess, elapsed, tries
    
    if elapsed > 0:
        if elapsed < DOT_TIME + DELTA\
           and elapsed > DOT_TIME > DOT_TIME - DELTA:
            guess += '.'
        elif elapsed > DOT_TIME > DOT_TIME - DELTA:
            guess += '-'
            
        if guess == CODE:
            guessed = True
            tries = 1
            
        if not check_guess(guess, CODE):
            guess = ''
            
        elapsed = 0
    
    # Draw graphics
    screen.fill((255, 255, 255))
    # Create the object and rectangle for the text
    text_obj = font.render(guess, True, (0, 0, 0))
    text_rect = text_obj.get_rect()
    text_rect.center = (250, 250)
    screen.fill((255, 255, 255))
    screen.blit(text_obj, text_rect)
    
    # Question text
    text_question = font.render('Layer 3 : ' + TEXT_QUESTION, True, (0, 0, 0))
    question_rect = text_question.get_rect()
    question_rect.center = (200, 25)
    screen.blit(text_question, question_rect)
    
    # Display hint text
    if tries >= 3:
        text_question = font.render(TEXT_HINT, True, (0, 0, 0))
        question_rect = text_question.get_rect()
        question_rect.center = (230, 55)
        screen.blit(text_question, question_rect)
    
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

def end_screen():
    screen.fill((255, 255, 255))
    # Question text
    text_1 = font.render('User indentified: Unknown', True, (0, 0, 0))
    text_2 = font.render('Information available:', True, (0, 0, 0))
    text_3 = font.render('None', True, (0, 0, 0))
    
    rect_1 = text_1.get_rect()
    rect_1.center = (150, 25)
    rect_2 = text_2.get_rect()
    rect_2.center = (125, 50)
    rect_3 = text_3.get_rect()
    rect_3.center = (40, 100)
    
    screen.blit(text_1, rect_1)
    screen.blit(text_2, rect_2)
    screen.blit(text_3, rect_3)

# Main game loop
running = True
while running:
    # Close the game when the event is triggered
    for event in pygame.event.get():
        if event.type == pygame.QUIT\
           or (event.type == pygame.KEYDOWN\
               and event.key== pygame.K_ESCAPE):
            running = False
    
    # Determine current level
    if level == 1:
        if d_pad_code():
            level = 2
    elif level == 2:
        if distance():
            level = 3
    elif level == 3:
        if morse_code():
            level = 4
    elif level ==  4:
        end_screen()
    else:
        running = False
            
    pygame.display.flip()
    
GPIO.cleanup()
pygame.quit()