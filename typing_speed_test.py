import pygame
import sys
from random import choice
import time

pygame.init()

screen = pygame.display.set_mode((1280, 640))
pygame.display.set_caption('Typing speed test')

icon_time_surface = pygame.image.load('icon_time.png')
icon_accuracy_surface = pygame.image.load('icon_accuracy.png')
text_file = 'texts.txt'

# Colors 
color_backgorund = (25, 36, 177) 
color_left_field = (76, 87, 216) 
color_right_field = (255, 204, 64)	
# Text colors
color_text = (255, 218, 115)
color_highlight_letter = (114, 121, 216)
color_highlight_letter_bg = (255, 187, 0)
color_result_text = (76, 87, 216) 

# Button colors
color_button = (8, 16, 115) 
color_button_text = (114, 121, 216) 

font_for_text = pygame.font.SysFont('segoeuisemibold', 20)
font_for_buttons = pygame.font.SysFont('segoeuisemibold', 28)
font_for_result = pygame.font.SysFont('segoeuisemibold', 35)

#Rectangles
leftFieldRect = pygame.Rect(40, 40, 800, 560)
rightFieldRect = pygame.Rect(880, 40, 360, 560)
buttonStartRect = pygame.Rect(920, 80, 160, 40)
buttonRestartRect = pygame.Rect(920, 80, 160, 40)

button_coordinates = (940, 80)
icon_time_coordinates = (920, 140)
icon_accuracy_coordinates = (920, 220)
typing_speed_coordinates = (1000, 140)
accuracy_coordinates = (1000, 225)

text_start_x = 50
text_start_y = 80
row_spacing = 40
text_width_limit = 750



class Game():
    text_split_by_rows = []
    is_game_started = False
    input_started = False
    all_test_text = ''
    text_remained_for_result = ''
    text_before_current_input = ''
    accuracy = ''
    typing_speed = ''
    counter_of_incorrect_inputs = 0
    start_time = 0
    end_time = 0
    current_row = 0


    def draw_elements(self):
        self.draw_background_fields()
        self.draw_buttons()
        self.draw_text()
        self.draw_elements_of_result()
        self.highlight_current_letter()


    def draw_background_fields(self):
        pygame.draw.rect(screen, color_left_field, leftFieldRect, 0)
        pygame.draw.rect(screen, color_right_field, rightFieldRect, 0)
    

    def draw_buttons(self):
        if self.is_game_started == True:
            text = 'Restart'
            rect = buttonRestartRect
        else:
            text = 'Start'
            rect = buttonStartRect
            
        pygame.draw.rect(screen, color_button, rect)
        screen.blit(font_for_buttons.render(text, True, color_button_text), button_coordinates)         


    def draw_elements_of_result(self):
        screen.blit(icon_time_surface, icon_time_coordinates)
        screen.blit(font_for_result.render(self.typing_speed, True, color_result_text), typing_speed_coordinates)  

        screen.blit(icon_accuracy_surface, icon_accuracy_coordinates)
        screen.blit(font_for_result.render(self.accuracy, True, color_result_text), accuracy_coordinates)


    def generate_random_text(self):
        with open (text_file, 'r') as file:
            rows =[line for line in file if line]
            self.all_test_text = choice(rows).replace('\n', '')


    def split_text_by_rows(self):
        if self.all_test_text:
            split_text_by_spaces = self.all_test_text.split(' ')
            text_to_add = ''

            for word in split_text_by_spaces:
                if len(self.text_split_by_rows) == 0 and text_to_add == '':
                    text_to_add += word + ' '
                elif font_for_text.render(text_to_add + word, 1, color_text).get_width() < text_width_limit:
                    text_to_add += word + ' '
                else:
                    self.text_split_by_rows.append(text_to_add)
                    text_to_add = word + ' '
            self.text_split_by_rows.append(text_to_add)


    def draw_text(self):
        pos_y = text_start_y
        for row in self.text_split_by_rows:
            screen.blit(font_for_text.render(row, True, color_text), (text_start_x, pos_y))
            pos_y += row_spacing

    
    def input_text(self, letter):
        if self.input_started == False:
            self.text_remained_for_result = self.all_test_text
            self.input_started = True
        if len(self.text_remained_for_result)> 0 and letter == self.text_remained_for_result[0]:
            self.text_remained_for_result = self.text_remained_for_result[1:]
            self.text_before_current_input += letter
            for row in self.text_split_by_rows:
                index = self.text_split_by_rows.index(row)
                if self.text_before_current_input == row:
                    self.current_row = index + 1
                    self.text_before_current_input = ''
        else:
            self.counter_of_incorrect_inputs += 1
        if len(self.text_remained_for_result) == 0:
            self.show_result()
 

    def restart_game(self):
        self.input_started = False
        self.is_game_started = False
        self.all_test_text = ''
        self.text_split_by_rows = []
        self.counter_of_incorrect_inputs = 0
        self.text_before_current_input = ''
        self.text_remained_for_result = ''
        self.current_row = 0

    
    def show_result(self):
        self.end_time = time.perf_counter()
        typing_speed_result = round(len(self.all_test_text) / (self.end_time - self.start_time) * 60, 1)
        self.typing_speed = f'{typing_speed_result} c/min'

        accuracy_result = round(100 - (self.counter_of_incorrect_inputs * 100 / len(self.all_test_text)), 1)
        self.accuracy = f'{accuracy_result} %'
        self.restart_game()


    def highlight_current_letter(self):
        if (len(self.text_remained_for_result) > 0 or self.current_row > 0) and self.is_game_started == True:
            calculated_width = font_for_text.render(self.text_before_current_input, 1, color_highlight_letter).get_width()
            x_higlight_letter = text_start_x + calculated_width
            y_higlight_letter = text_start_y + row_spacing * (self.current_row)
            letter = self.text_remained_for_result[0]
            screen.blit(font_for_text.render(letter, True, color_highlight_letter, color_highlight_letter_bg), (x_higlight_letter, y_higlight_letter))


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

    screen.fill(color_backgorund)
    game.draw_elements()
    pygame.display.flip()