import pygame
import sys
from random import choice

pygame.init()

screen = pygame.display.set_mode((1280, 640))
pygame.display.set_caption('Typing speed test')

# Colors

bg_color = (25, 36, 177) #1924B1
color_1 = (47, 53, 132) #2F3584
color_2 = (8, 16, 115) #081073
color_3 = (76, 87, 216) #4C57D8
color_4 = (114, 121, 216) #7279D8

color_5 = (255, 187, 0) #FFBB00
color_6 = (191, 153, 48) #BF9930
color_7 = (166, 122, 0) #A67A00
color_8 = (255, 204, 64) #FFCC40	
color_9 = (255, 218, 115) #FFDA73




class Game():
    leftFieldRect = pygame.Rect(40,40,800,560)
    rightFieldRect = pygame.Rect(880,40,360,560)
    buttonGenerateRandomText = pygame.Rect()
    buttonStart = pygame.Rect()
    buttonRestart = pygame.Rect()


    def __init__(self, accuracy, typing_speed, text_for_test):
        self.accuracy = accuracy
        self.typing_speed = typing_speed
        self.text_for_test = text_for_test


    def draw_background_fields(self):
        pygame.draw.rect(screen, color_3, self.leftFieldRect, 0)
        pygame.draw.rect(screen, color_8, self.rightFieldRect, 0)
    
    def draw_buttons(self):
        pass

    def count_Accuracy_and_TypingSpeed(self):
        pass

    def generate_random_text(self):
        with open ('texts.txt', 'r') as file:
            rows =[line for line in file if line]
            self.text_for_test = choice(rows).replace('\n', '')


game = Game(accuracy= 0, typing_speed= 0, text_for_test = '')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    

    screen.fill(bg_color)
    game.draw_background_fields()

    if len(game.text_for_test) == 0:
        game.generate_random_text()



    pygame.display.flip()