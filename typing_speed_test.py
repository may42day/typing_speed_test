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

font = pygame.font.SysFont('segoeuisemibold', 20)

class Game():
    leftFieldRect = pygame.Rect(40,40,800,560)
    rightFieldRect = pygame.Rect(880,40,360,560)
    buttonStart = pygame.Rect(920, 80, 160, 40)
    buttonRestart = pygame.Rect(920, 80, 160, 40)
    text_split_by_rows = []
    is_game_started = False
    button_text_x = 940
    button_text_y = 85


    def __init__(self, accuracy, typing_speed, text_for_test):
        self.accuracy = accuracy
        self.typing_speed = typing_speed
        self.text_for_test = text_for_test


    def draw_background_fields(self):
        pygame.draw.rect(screen, color_3, self.leftFieldRect, 0)
        pygame.draw.rect(screen, color_8, self.rightFieldRect, 0)
    

    def draw_buttons(self):
        if self.is_game_started == True:
            pygame.draw.rect(screen, color_1, self.buttonRestart)
            screen.blit(font.render('Restart', True, color_4), (self.button_text_x, self.button_text_y))
        else:
            pygame.draw.rect(screen, color_2, self.buttonStart)
            screen.blit(font.render('Start', True, color_4), (self.button_text_x, self.button_text_y))


    def count_Accuracy_and_TypingSpeed(self):
        pass


    def generate_random_text(self):
        with open ('texts.txt', 'r') as file:
            rows =[line for line in file if line]
            self.text_for_test = choice(rows).replace('\n', '')

    def split_text_by_rows(self):
        if self.text_for_test:
            split_text_by_spaces = self.text_for_test.split(' ')
            text_to_add = ''
            count = 0


            for word in split_text_by_spaces:
                count += 1
                if len(self.text_split_by_rows) == 0 and text_to_add == '':
                    text_to_add += word + ' '
                elif font.render(text_to_add + word, 1, color_7).get_width() < 750:
                    text_to_add += word + ' '
                else:
                    self.text_split_by_rows.append(text_to_add)
                    text_to_add = word + ' '
            self.text_split_by_rows.append(text_to_add)

    def draw_text(self):
        x = 50
        y = 40
        for row in self.text_split_by_rows:
            screen.blit(font.render(row, True, color_9), (x, y))
            y += 40


game = Game(accuracy= 0, typing_speed= 0, text_for_test = '')


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if (x>=920 and x<=1080 and y >= 80 and y<= 120) and game.is_game_started == False:
                game.generate_random_text()
                game.split_text_by_rows()
                game.is_game_started = True
            elif (x>=920 and x<=1080 and y >= 80 and y<= 120) and game.is_game_started == True:
                game.is_game_started = False
                game.text_for_test = ''
                game.text_split_by_rows = []

    screen.fill(bg_color)
    game.draw_background_fields()
    game.draw_buttons()
    game.draw_text()

    pygame.display.flip()