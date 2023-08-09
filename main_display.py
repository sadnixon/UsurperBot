from gameBonus import gameBonus
from gameBonusDeck import gameBonusDeck
from gameCard import gameCard
from gameDeck import gameDeck
from gameSetup import gameSetup
from gameAI import gameAI
from utilities import print_card_list
from utilities import evaluation
from action_utilities import execute_instant
from action_utilities import execute_pre_scoring
from utilities import check_possible_placement
from utilities import grid_deep_copy
from input_utilities import *

import pygame
from pygame import *
import math


keys_to_coords = {113:(0,0),
119:(0,1),
101:(0,2),
97:(1,0),
115:(1,1),
100:(1,2),
122:(2,0),
120:(2,1),
99:(2,2)}

class usurperGame:
    def __init__(self, p_zero_name, p_one_name, p_zero_type, p_one_type, p_zero_ai_level='random', p_one_ai_level='random',p_zero_ai_draft_level='random',p_one_ai_draft_level='random',p_zero_bonus_id='',p_one_bonus_id='',prebake_order=[], prebake_starter=-1):
        self.p_zero_name = p_zero_name
        self.p_one_name = p_one_name
        self.p_zero_type = p_zero_type
        self.p_one_type = p_one_type
        self.setup = gameSetup(p_zero_bonus_id,p_one_bonus_id,prebake_order,prebake_starter)
        self.p_ai = [gameAI(0, p_zero_ai_level,p_zero_ai_draft_level,True), gameAI(1, p_one_ai_level,p_one_ai_draft_level,True)]

    def mainLoop(self):
        print("Begin draft phase.")
        self.setup.start_draft_phase()

        pygame.init()
        largest_size = pygame.display.list_modes()[0]

        screen = pygame.display.set_mode(largest_size,HWSURFACE|DOUBLEBUF|RESIZABLE)
        
        for event in pygame.event.get():
            if event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
            
        pygame.display.update()

        game_height, game_width = 4240, 7560
        screen_height = screen.get_height()
        screen_width = screen.get_width()

        self.setup.set_card_sizes(screen_width,screen_height,game_width,game_height,True)

        self.p_ai[0].player_see_bonus(self.setup.p_zero_bonus[0])
        self.p_ai[1].player_see_bonus(self.setup.p_one_bonus[0])

        while len(self.setup.p_zero_hand) < 9 or len(self.setup.p_one_hand) < 9:
            print(f"{[self.p_zero_name,self.p_one_name][self.setup.turn]}'s turn!")
            if self.setup.turn == 0:
                print(f"{self.p_zero_name}'s hand:")
                print_card_list(self.setup.p_zero_hand)
                print(f"{self.p_zero_name}'s bonus:")
                print_card_list(self.setup.p_zero_bonus)
            else:
                print(f"{self.p_one_name}'s hand:")
                print_card_list(self.setup.p_one_hand)
                print(f"{self.p_one_name}'s bonus:")
                print_card_list(self.setup.p_one_bonus)
            print("Draft options:")
            print_card_list(self.setup.draft_options)
            if (self.setup.turn == 0 and self.p_zero_type == 'Human') or (self.setup.turn == 1 and self.p_one_type == 'Human'):
                draft_selection_index = input_waiter_draft(screen,self.setup,game_width,game_height)
            else:
                draft_selection_index = self.p_ai[self.setup.turn].draft_decision(
                    self.setup)

            self.p_ai[self.setup.turn].player_see_card(
                self.setup.draft_options[draft_selection_index])
            self.p_ai[abs(self.setup.turn - 1)].opp_draft_card(
                self.setup.draft_options[draft_selection_index])

            self.setup.draft_card(draft_selection_index, self.setup.turn)

            self.setup.next_turn()
        
        p_zero_draft = [card.card_id for card in self.setup.p_zero_hand].copy()
        p_one_draft = [card.card_id for card in self.setup.p_one_hand].copy()

        print("Begin play phase.")
        self.setup.start_play_phase()

        screen_height = screen.get_height()
        screen_width = screen.get_width()
        game_height, game_width = 4505, 7938
        self.setup.set_card_sizes(screen_width,screen_height,game_width,game_height)

        while check_possible_placement(self.setup.p_zero_grid, self.setup.p_zero_hand) or check_possible_placement(self.setup.p_one_grid, self.setup.p_one_hand):
            if not check_possible_placement([self.setup.p_zero_grid, self.setup.p_one_grid][self.setup.turn], [self.setup.p_zero_hand, self.setup.p_one_hand][self.setup.turn]):
                print(
                    f"{[self.p_zero_name,self.p_one_name][self.setup.turn]} has no placements!")
                self.setup.next_turn()
                continue
            print(f"{[self.p_zero_name,self.p_one_name][self.setup.turn]}'s turn!")
            if self.setup.turn == 0:
                print(f"{self.p_zero_name}'s hand:")
                print_card_list(self.setup.p_zero_hand)
                print(f"{self.p_zero_name}'s bonus:")
                print_card_list(self.setup.p_zero_bonus)
                print(f"{self.p_zero_name}'s grid:")
                print_card_list(self.setup.p_zero_grid[0])
                print_card_list(self.setup.p_zero_grid[1])
                print_card_list(self.setup.p_zero_grid[2])
            else:
                print(f"{self.p_one_name}'s hand:")
                print_card_list(self.setup.p_one_hand)
                print(f"{self.p_one_name}'s bonus:")
                print_card_list(self.setup.p_one_bonus)
                print(f"{self.p_one_name}'s grid:")
                print_card_list(self.setup.p_one_grid[0])
                print_card_list(self.setup.p_one_grid[1])
                print_card_list(self.setup.p_one_grid[2])
            if (self.setup.turn == 0 and self.p_zero_type == 'Human') or (self.setup.turn == 1 and self.p_one_type == 'Human'):
                #print("Select a card to place:")
                #card_selection_index = input_waiter_csi(game_width,game_height,game_surface,screen,self.setup)
                    
                #print("Select an x and y coordinate to place the card in")
                #card_placement_x, card_placement_y = input_waiter_xy(game_width,game_height,game_surface,screen,self.setup,card_selection_index,True)
                #card_selection_index,card_placement_x,card_placement_y = input_waiter_xy_2(game_width,game_height,game_surface,screen,self.setup,True)
                
                card_selection_index,card_placement_x,card_placement_y = input_waiter_play(screen,self.setup,game_width,game_height,player=True)
            else:
                card_selection_index, card_placement_x, card_placement_y = self.p_ai[self.setup.turn].play_decision(
                    self.setup)

            self.setup.play_card(
                self.setup.turn, card_selection_index, card_placement_x, card_placement_y)
            print(card_placement_x,card_placement_y)
            print([self.setup.p_zero_grid,self.setup.p_one_grid][self.setup.turn][card_placement_x][card_placement_y])
            self.p_ai[abs(self.setup.turn - 1)].opp_play_card([self.setup.p_zero_grid,
                                                               self.setup.p_one_grid][self.setup.turn][card_placement_x][card_placement_y])

            if [self.setup.p_zero_grid, self.setup.p_one_grid][self.setup.turn][card_placement_x][card_placement_y].instant:
                execute_instant(self.setup, self.setup.turn, self.p_ai, self.p_zero_name, self.p_one_name,
                                self.p_zero_type, self.p_one_type, card_placement_x, card_placement_y,display = True, screen = screen,game_width = game_width, game_height = game_height)

            self.setup.next_turn()

        if self.setup.turn == 0:
            execute_pre_scoring(
                self.setup, self.p_ai[0], self.p_zero_name, self.p_zero_type,display = True,screen = screen,game_width = game_width,game_height = game_height)
            self.setup.next_turn()
            execute_pre_scoring(
                self.setup, self.p_ai[1], self.p_one_name, self.p_one_type,display = True,screen = screen,game_width = game_width,game_height = game_height)
        else:
            execute_pre_scoring(
                self.setup, self.p_ai[1], self.p_one_name, self.p_one_type,display = True,screen = screen,game_width = game_width,game_height = game_height)
            self.setup.next_turn()
            execute_pre_scoring(
                self.setup, self.p_ai[0], self.p_zero_name, self.p_zero_type,display = True,screen = screen,game_width = game_width,game_height = game_height)

        p_zero_score, p_zero_indivs, p_zero_bonus_score = evaluation(
            self.setup.p_zero_grid, self.setup.p_one_grid, self.setup.p_zero_bonus, individuals=True)
        p_one_score, p_one_indivs, p_one_bonus_score = evaluation(
            self.setup.p_one_grid, self.setup.p_zero_grid, self.setup.p_one_bonus, individuals=True)

        print(f"{self.p_zero_name}'s bonus:")
        print_card_list(self.setup.p_zero_bonus)
        print(f"{self.p_zero_name}'s grid:")
        print_card_list(self.setup.p_zero_grid[0])
        print_card_list(self.setup.p_zero_grid[1])
        print_card_list(self.setup.p_zero_grid[2])

        print(f"{self.p_one_name}'s bonus:")
        print_card_list(self.setup.p_one_bonus)
        print(f"{self.p_one_name}'s grid:")
        print_card_list(self.setup.p_one_grid[0])
        print_card_list(self.setup.p_one_grid[1])
        print_card_list(self.setup.p_one_grid[2])

        print(f"{self.p_zero_name} got {p_zero_score}!")
        print(f"{self.p_one_name} got {p_one_score}!")
        if p_zero_score > p_one_score:
            print(f"{self.p_zero_name} WINS!")
        elif p_zero_score < p_one_score:
            print(f"{self.p_one_name} WINS!")
        else:
            print("IT'S A PERFECT TIE!")

        screen_height = screen.get_height()
        screen_width = screen.get_width()
        game_height, game_width = 4240, 6804
        self.setup.set_card_sizes(screen_width,screen_height,game_width,game_height,results=True)
        restart = input_waiter_results(screen,self.setup,game_width,game_height,self.p_zero_name,self.p_one_name,p_zero_score,p_one_score,p_zero_bonus_score,p_one_bonus_score)

        #return p_zero_score, p_one_score, p_zero_draft, p_one_draft, p_zero_indivs, p_one_indivs, self.setup.p_zero_grid, self.setup.p_one_grid, p_zero_bonus_score, p_one_bonus_score
        return restart


start_game = True
while start_game:
    game = usurperGame("Spencer", "Cuck", 'Human', 'AI','full','full','wifes_boyfriend','wifes_boyfriend',prebake_starter = 0)
    restart = game.mainLoop()
    if restart == 'n':
        start_game = False