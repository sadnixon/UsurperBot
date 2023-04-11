from gameCard import gameCard
from gameDeck import gameDeck
from gameBonus import gameBonus
from gameBonusDeck import gameBonusDeck
import random
import pygame


class gameSetup:
    def __init__(self, p_zero_bonus_id='', p_one_bonus_id='', prebake_order=[], prebake_starter=-1, test=False):
        self.main_deck = gameDeck()
        self.bonus_deck = gameBonusDeck()
        self.B7_card = self.main_deck.deck[[
            card.card_id for card in self.main_deck.deck].index('B7')]
        self.draft_options = []
        self.discard_pile = []
        self.p_zero_hand = []
        self.p_zero_bonus = []
        self.p_one_hand = []
        self.p_one_bonus = []
        self.p_zero_grid = [[0, 0, 0],
                            [0, 0, 0],
                            [0, 0, 0]]
        self.p_one_grid = [[0, 0, 0],
                           [0, 0, 0],
                           [0, 0, 0]]
        if prebake_starter == -1:
            self.turn = random.choice([0, 1])
        else:
            self.turn = prebake_starter
        self.p_zero_bonus_id = p_zero_bonus_id
        self.p_one_bonus_id = p_one_bonus_id
        self.prebake_order = prebake_order

        if not test:
            self.master_card_image_dict = {
                'R': [pygame.image.load('hq_card_images/R'+str(i)+'.png') for i in range(1,12)],
                'G': [pygame.image.load('hq_card_images/G'+str(i)+'.png') for i in range(1,12)],
                'B': [pygame.image.load('hq_card_images/B'+str(i)+'.png') for i in range(1,12)],
                'Y': [pygame.image.load('hq_card_images/Y'+str(i)+'.png') for i in range(1,12)],
                'X': [pygame.image.load('hq_card_images/X'+str(i)+'.png') for i in range(1,11)]
            }

            self.master_card_back = pygame.image.load('hq_card_images/card_back.png')
            self.master_bonus_back = pygame.image.load('hq_card_images/card_back_bonus.png')

            self.card_image_dict = {
                'R': [pygame.image.load('hq_card_images/R'+str(i)+'.png') for i in range(1,12)],
                'G': [pygame.image.load('hq_card_images/G'+str(i)+'.png') for i in range(1,12)],
                'B': [pygame.image.load('hq_card_images/B'+str(i)+'.png') for i in range(1,12)],
                'Y': [pygame.image.load('hq_card_images/Y'+str(i)+'.png') for i in range(1,12)],
                'X': [pygame.image.load('hq_card_images/X'+str(i)+'.png') for i in range(1,11)]
            }

            self.card_back = pygame.image.load('hq_card_images/card_back.png')
            self.bonus_back = pygame.image.load('hq_card_images/card_back_bonus.png')

    def set_card_sizes(self,screen_width,screen_height,game_width,game_height,draft=True):
        if  game_width/game_height < screen_width/screen_height:
            max_surface_x = round(screen_height*(game_width/game_height))
            max_surface_y = screen_height
        else:
            max_surface_x = screen_width
            max_surface_y = round(screen_width*(game_height/game_width))
        
        if draft:
            card_x = round(max_surface_x * 1/10)
            card_y = round(max_surface_y * 1/4)
        else:
            card_x = round(max_surface_x * 2/21)
            card_y = round(max_surface_y * 4/17)

        for i in range(len(list(self.card_image_dict.keys()))):
            for j in range(len(self.card_image_dict[list(self.card_image_dict.keys())[i]])):
                self.card_image_dict[list(self.card_image_dict.keys())[i]][j] = pygame.transform.smoothscale(self.master_card_image_dict[list(self.card_image_dict.keys())[i]][j],(card_x,card_y))
        self.card_back = pygame.transform.smoothscale(self.master_card_back,(card_x,card_y))
        self.bonus_back = pygame.transform.smoothscale(self.master_bonus_back,(card_x,card_y))

    def next_turn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0

    def start_draft_phase(self):
        if self.prebake_order != []:
            self.main_deck.arrange(self.prebake_order)
        else:
            self.main_deck.shuffle()
        self.bonus_deck.shuffle()
        print([card.card_id for card in self.main_deck.deck])
        for i in range(6):
            self.draft_options.append(self.main_deck.deal())

        self.p_zero_bonus.append(self.bonus_deck.deal(self.p_zero_bonus_id))
        self.p_one_bonus.append(self.bonus_deck.deal(self.p_one_bonus_id))

    def draft_card(self, pos_x, player):
        if player == 0:
            self.p_zero_hand.append(self.draft_options.pop(pos_x))
        else:
            self.p_one_hand.append(self.draft_options.pop(pos_x))
        self.draft_options.append(self.main_deck.deal())

    def start_play_phase(self):
        for i in range(6):
            self.discard_pile.append(self.draft_options.pop(0))

    def draw(self, player):
        if player == 0:
            self.p_zero_hand.append(self.main_deck.deal())
        else:
            self.p_one_hand.append(self.main_deck.deal())

    def replace(self, player, pos_x, pos_y):
        if player == 0:
            self.discard_pile.append(self.p_zero_grid[pos_x].pop(pos_y))
            self.p_zero_grid[pos_x].insert(pos_y, self.main_deck.deal())
        else:
            self.discard_pile.append(self.p_one_grid[pos_x].pop(pos_y))
            self.p_one_grid[pos_x].insert(pos_y, self.main_deck.deal())
        self.update_B7()

    def deal_temp(self):
        self.draft_options.append(self.main_deck.deal())

    def draft_temp(self, pos_x, player):
        if player == 0:
            self.p_zero_hand.append(self.draft_options.pop(pos_x))
        else:
            self.p_one_hand.append(self.draft_options.pop(pos_x))

    def discard(self, player, place, pos_x, pos_y):
        if player == 0:
            if place == 'grid':
                self.discard_pile.append(self.p_zero_grid[pos_x].pop(pos_y))
                self.p_zero_grid[pos_x].insert(pos_y, 0)
            elif place == 'hand':
                self.discard_pile.append(self.p_zero_hand.pop(pos_x))
            else:
                self.discard_pile.append(self.draft_options.pop(pos_x))
        else:
            if place == 'grid':
                self.discard_pile.append(self.p_one_grid[pos_x].pop(pos_y))
                self.p_one_grid[pos_x].insert(pos_y, 0)
            elif place == 'hand':
                self.discard_pile.append(self.p_one_hand.pop(pos_x))
            else:
                self.discard_pile.append(self.draft_options.pop(pos_x))

    def flip_card(self, player, pos_x, pos_y):
        if player == 0:
            self.p_zero_grid[pos_x][pos_y].flip()
        else:
            self.p_one_grid[pos_x][pos_y].flip()
        self.update_B7()

    def copy_card(self, player, pos_x, pos_y):
        if player == 0:
            self.p_zero_grid[pos_x][pos_y].g3_copy(
                self.p_zero_grid[pos_x][pos_y+1])
        else:
            self.p_one_grid[pos_x][pos_y].g3_copy(
                self.p_one_grid[pos_x][pos_y+1])
        self.update_B7()

    def un_copy_card(self, player, pos_x, pos_y):
        if player == 0:
            self.p_zero_grid[pos_x][pos_y].un_copy()
        else:
            self.p_one_grid[pos_x][pos_y].un_copy()
        self.update_B7()

    def play_card(self, player, hand_pos_x, pos_x, pos_y):
        if player == 0:
            self.p_zero_grid[pos_x] = self.p_zero_grid[pos_x][:pos_y] + \
                [self.p_zero_hand.pop(hand_pos_x)] + \
                self.p_zero_grid[pos_x][pos_y+1:]
        else:
            self.p_one_grid[pos_x] = self.p_one_grid[pos_x][:pos_y] + \
                [self.p_one_hand.pop(hand_pos_x)] + \
                self.p_one_grid[pos_x][pos_y+1:]
        self.update_B7()

    def move_card(self, player, pos_x, pos_y, target_pos_x, target_pos_y):
        if player == 0:
            moving_card = self.p_zero_grid[pos_x].pop(pos_y)
            self.p_zero_grid[pos_x].insert(pos_y, 0)
            self.p_zero_grid[target_pos_x] = self.p_zero_grid[target_pos_x][:target_pos_y] + [
                moving_card] + self.p_zero_grid[target_pos_x][target_pos_y+1:]
        else:
            moving_card = self.p_one_grid[pos_x].pop(pos_y)
            self.p_one_grid[pos_x].insert(pos_y, 0)
            self.p_one_grid[target_pos_x] = self.p_one_grid[target_pos_x][:target_pos_y] + [
                moving_card] + self.p_one_grid[target_pos_x][target_pos_y+1:]

    def update_B7(self):
        hands_sum = 0
        for i in range(3):
            for j in range(3):
                if self.p_zero_grid[i][j] != 0:
                    hands_sum += self.p_zero_grid[i][j].hands
                if self.p_one_grid[i][j] != 0:
                    hands_sum += self.p_one_grid[i][j].hands
        old_points = self.B7_card.points
        if hands_sum < 8:
            self.B7_card.base_points = 1
            self.B7_card.changepoints(1-old_points)
        elif hands_sum < 12:
            self.B7_card.base_points = 5
            self.B7_card.changepoints(5-old_points)
        else:
            self.B7_card.base_points = 8
            self.B7_card.changepoints(8-old_points)
