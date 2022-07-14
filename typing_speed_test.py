import pygame
import sys
from random import choice
import time

pygame.init()

screen = pygame.display.set_mode((1280, 640))
pygame.display.set_caption('Typing speed test')

icon_time_surface = pygame.image.load('icon_time.png')
icon_accuracy_surface = pygame.image.load('icon_accuracy.png')
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
    text_to_be_entered_for_result = ''
    input_started = False
    accuracy = ''
    typing_speed = ''
    text_for_test = ''
    counter_of_incorrect_inputs = 0
    start_time = 0
    end_time = 0
    text_before_current_input = ''
    current_row = 0


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

    def draw_elements_of_result(self):
        screen.blit(icon_time_surface, (920, 140)) # icon_rect(x,y) отдельно
        screen.blit(font.render(self.typing_speed, True, color_3), (1000, 140))  

        screen.blit(icon_accuracy_surface, (920, 220))
        screen.blit(font.render(self.accuracy, True, color_3), (1000, 220))



    def generate_random_text(self):
        with open ('texts.txt', 'r') as file:
            rows =[line for line in file if line]
            self.text_for_test = choice(rows).replace('\n', '')

    def split_text_by_rows(self):
        if self.text_for_test:
            split_text_by_spaces = self.text_for_test.split(' ')
            text_to_add = ''

            for word in split_text_by_spaces:
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
        y = 80
        for row in self.text_split_by_rows:
            screen.blit(font.render(row, True, color_9), (x, y))
            y += 40

    
    def input_text(self, letter):
        if self.input_started == False:
            self.text_to_be_entered_for_result = self.text_for_test
            self.input_started = True
        if len(self.text_to_be_entered_for_result)> 0 and letter == self.text_to_be_entered_for_result[0]:
            self.text_to_be_entered_for_result = self.text_to_be_entered_for_result[1:]
            self.text_before_current_input += letter
            for row in self.text_split_by_rows:
                index = self.text_split_by_rows.index(row)
                if self.text_before_current_input == row:
                    self.current_row = index + 1
                    self.text_before_current_input = ''
        else:
            self.counter_of_incorrect_inputs += 1
        if len(self.text_to_be_entered_for_result) == 0:
            self.show_result()   
        


    def restart_game(self):
        self.input_started = False
        self.is_game_started = False
        self.text_for_test = ''
        self.text_split_by_rows = []
        self.counter_of_incorrect_inputs = 0
        self.text_before_current_input = ''
        self.text_to_be_entered_for_result = ''
        self.current_row = 0

    
    def show_result(self):
        self.end_time = time.perf_counter()
        typing_speed_result = round(len(self.text_for_test) / (self.end_time - self.start_time) * 60, 1)
        self.typing_speed = f'{typing_speed_result} c/min'

        accuracy_result = round(100 - (self.counter_of_incorrect_inputs * 100 / len(self.text_for_test)), 1)
        self.accuracy = f'{accuracy_result} %'
        self.restart_game()

    def highlight_current_letter(self):
        if len(self.text_to_be_entered_for_result)>0 or self.current_row > 0 and self.is_game_started == True:

            x_start = 50 
            y_start = 80
            x_higlight_letter = x_start + font.render(self.text_before_current_input, 1, color_7).get_width()
            print(self.text_before_current_input, self.text_to_be_entered_for_result[0], self.text_before_current_input + self.text_to_be_entered_for_result[0])
            y_higlight_letter = y_start + 40 * (self.current_row)
            letter = self.text_to_be_entered_for_result[0]
            screen.blit(font.render(letter, True, color_4, color_5), (x_higlight_letter, y_higlight_letter))



game = Game()


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
                game.start_time = time.perf_counter()
            elif (x>=920 and x<=1080 and y >= 80 and y<= 120) and game.is_game_started == True:      
                game.restart_game()

        elif event.type == pygame.KEYDOWN and game.is_game_started == True:
            if event.unicode:
                game.input_text(event.unicode)


    screen.fill(bg_color)
    game.draw_background_fields()
    game.draw_buttons()
    game.draw_text()
    game.draw_elements_of_result()
    game.highlight_current_letter()

    pygame.display.flip()