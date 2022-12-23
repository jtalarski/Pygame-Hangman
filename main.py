import pygame
import math
import random
# import os
# from pygame.locals import QUIT

# Tutorial from YouTube Tech with Tim https://youtu.be/W6cjx7t39d4

''' SETUP DISPLAY '''
pygame.init()
WIDTH, HEIGHT = 800, 500
# Sets area of display
win = pygame.display.set_mode((WIDTH, HEIGHT))
# Sets title of display area
pygame.display.set_caption("Hangman Game")

''' BUTTON VARIABLES '''
RADIUS = 20
GAP = 15
letters = [] # [x,y, letter, visible]
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2 )
starty = 400
A = 65 # ASCII code for capital A
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i // 13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])
    
''' FONT '''
LETTER_FONT = pygame.font.SysFont('comicsans', 30)
WORD_FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 45)

''' LOAD IMAGES '''
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

''' GAME VARIABLES '''
hangman_status = 0
words = ['HOLIDAY', 'WINTER', 'SNOWMAN', 'SNOWBALL']
# Use the random package
word = random.choice(words)
guessed =[]


''' COLORS '''
WHITE = (255,255,255)
LT_ORG = (254,153,0)


''' SETUP GAME LOOP'''
def draw():
    # Fill window background
    win.fill(LT_ORG)
    # Insert title
    text = TITLE_FONT.render('My Stolen Hangman Game', 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
    # Draw word to guess
    display_word =''
    for letter in word:
        if letter in guessed:
            display_word += letter + ' '
        else:
            display_word += '_ '
    text = WORD_FONT.render(display_word, 1, WHITE)
    win.blit(text, (400,200))

    # Draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, WHITE, (x, y), RADIUS, 3) 
            text = LETTER_FONT.render(ltr, 1, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
    
    win.blit(images[hangman_status], (150,100)) 
    # Tell pygame to update the display
    pygame.display.update()
    

def display_message(message):
    pygame.time.delay(1000)
    win.fill(LT_ORG)
    text = WORD_FONT.render(message, 1, WHITE)
    win.blit(text, (WIDTH/2 - text.get_width() /
             2, HEIGHT/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)
   
# Decide how fast you want the game to display
FPS = 60
# Setup Pygame clock to monitor speed
clock = pygame.time.Clock()
# Set up loop that will keep display running in the loop
run = True

# Need a Pygame loop that 'listens' for input, run at FPS
while run:
    clock.tick(FPS)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Setup collision (button touch)    
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible:
                    dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                    if dis < RADIUS:
                        letter[3] = False # 3 because the visible tag is the 4th value in letter
                        guessed.append(ltr)
                        if ltr not in word:
                            hangman_status += 1
    draw()
    
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    
    if won:
        display_message('You WON!')
        break
        
    if hangman_status == 6:
        display_message('You LOST!')
        break
    
pygame.quit()