import pygame
import RPi.GPIO as GPIO

pygame.init()

CODE = 'UUDDLRLR'
print(CODE[0])

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

COLOR_OFF = (0, 150, 0)
COLOR_ON = (0, 255, 0)

PIN_LEFT = 25
PIN_DOWN = 13
PIN_UP = 26
PIN_RIGHT = 19

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN_LEFT, GPIO.IN)
GPIO.setup(PIN_DOWN, GPIO.IN)
GPIO.setup(PIN_UP, GPIO.IN)
GPIO.setup(PIN_RIGHT, GPIO.IN)
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

down_color = COLOR_OFF
left_color = COLOR_OFF
right_color = COLOR_OFF
up_color = COLOR_OFF
pressed = True
guess = ''
 
running = True
def d_pad_code():
    global pressed, guess
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
    
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    if d_pad_code():
        running = False
            
    pygame.display.flip()
    
GPIO.cleanup()
pygame.quit()