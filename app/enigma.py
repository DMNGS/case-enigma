# Script      : enigma.py
# Description : Puzzle game using CrowPi
# Author      : DOMINGUES PEDROSA Samuel
# Date        : 2022.29.09, V1.0
import pygame
import RPi.GPIO as GPIO

# Initialize Pygame screen
pygame.init()
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Initialize d-pad
PIN_LEFT = 25
PIN_DOWN = 13
PIN_UP = 26
PIN_RIGHT = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LEFT, GPIO.IN)
GPIO.setup(PIN_DOWN, GPIO.IN)
GPIO.setup(PIN_UP, GPIO.IN)
GPIO.setup(PIN_RIGHT, GPIO.IN)

COLOR_OFF = (0, 150, 0)
COLOR_ON = (0, 255, 0)

down_color = COLOR_OFF
left_color = COLOR_OFF
right_color = COLOR_OFF
up_color = COLOR_OFF

pressed = True # Block the code from continusly reading an input
 
# First puzzle : reproduse a code on the d-pad
guess = ''
def d_pad_code():
    CODE = 'UUDDLRLR'
    global pressed, guess # Global so they don't reset every time the function is called
    solved = False
    left_color = COLOR_ON if not GPIO.input(PIN_LEFT) else COLOR_OFF    
    down_color = COLOR_ON if not GPIO.input(PIN_DOWN) else COLOR_OFF    
    up_color = COLOR_ON if not GPIO.input(PIN_UP) else COLOR_OFF    
    right_color = COLOR_ON if not GPIO.input(PIN_RIGHT) else COLOR_OFF
    
    guess += 'L' if not GPIO.input(PIN_LEFT) and not pressed else ''    
    guess += 'D' if not GPIO.input(PIN_DOWN) and not pressed else ''    
    guess += 'U' if not GPIO.input(PIN_UP) and not pressed else ''    
    guess += 'R' if not GPIO.input(PIN_RIGHT) and not pressed else ''
    
    pressed = True if not GPIO.input(PIN_LEFT) or not GPIO.input(PIN_DOWN) or not GPIO.input(PIN_UP) or not GPIO.input(PIN_RIGHT) else False
    
    if len(guess) > 0 and guess[len(guess)-1] != CODE[len(guess)-1]:
        guess = ''
        
    if guess == CODE:
        solved = True
    
    print(guess)
    
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, left_color, (100, 250), 75)
    pygame.draw.circle(screen, down_color, (250, 400), 75)
    pygame.draw.circle(screen, up_color, (250, 100), 75)
    pygame.draw.circle(screen, right_color, (400, 250), 75)
    
    return solved

# Get out of the loop when the game is finished
running = True
while running:
    # Close the game when the event is triggered
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if d_pad_code():
        running = False
            
    pygame.display.flip()

GPIO.cleanup() # Reset the GPIO
pygame.quit()