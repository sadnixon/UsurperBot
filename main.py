from gameBonus import gameBonus
from gameBonusDeck import gameBonusDeck
from gameCard import gameCard
from gameDeck import gameDeck
from gameSetup import gameSetup
from gameAI import gameAI
from utilities import print_card_list
from utilities import evaluation
from utilities import execute_instant
from utilities import execute_pre_scoring
from utilities import check_possible_placement
from utilities import grid_deep_copy
import random


class usurperGame:
    def __init__(self, p_zero_name, p_one_name, p_zero_type, p_one_type, p_zero_ai_level='random', p_one_ai_level='random',p_zero_bonus_id='',p_one_bonus_id='',prebake_order=[], prebake_starter=-1):
        self.p_zero_name = p_zero_name
        self.p_one_name = p_one_name
        self.p_zero_type = p_zero_type
        self.p_one_type = p_one_type
        self.setup = gameSetup(p_zero_bonus_id,p_one_bonus_id,prebake_order,prebake_starter)
        self.p_ai = [gameAI(0, p_zero_ai_level), gameAI(1, p_one_ai_level)]

    def mainLoop(self):
        print("Begin draft phase.")
        self.setup.start_draft_phase()

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
                draft_selection_index = -1
                while draft_selection_index not in range(6):
                    print("Input valid index from 0 to 5")
                    draft_selection_index = int(input())
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
                print("Select a card to place:")
                card_selection_index = -1
                while card_selection_index not in range(len([self.setup.p_zero_hand, self.setup.p_one_hand][self.setup.turn])) or not check_possible_placement([self.setup.p_zero_grid, self.setup.p_one_grid][self.setup.turn], [self.setup.p_zero_hand, self.setup.p_one_hand][self.setup.turn], True, card_selection_index):
                    print(
                        f"Input valid index from 0 to {len([self.setup.p_zero_hand, self.setup.p_one_hand][self.setup.turn])-1}")
                    card_selection_index = int(input())
                print("Select an x and y coordinate to place the card in")
                card_placement_x = -1
                card_placement_y = -1
                while (not (card_placement_x in range(3) and card_placement_y in range(3))) or [self.setup.p_zero_grid, self.setup.p_one_grid][self.setup.turn][card_placement_x][card_placement_y] != 0:
                    print("Input valid coords from 0 to 2")
                    card_placement_x = int(input())
                    card_placement_y = int(input())
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
                                self.p_zero_type, self.p_one_type, card_placement_x, card_placement_y)

            self.setup.next_turn()

        if self.setup.turn == 0:
            execute_pre_scoring(
                self.setup, self.p_ai[0], self.p_zero_name, self.p_zero_type)
            self.setup.next_turn()
            execute_pre_scoring(
                self.setup, self.p_ai[1], self.p_one_name, self.p_one_type)
        else:
            execute_pre_scoring(
                self.setup, self.p_ai[1], self.p_one_name, self.p_one_type)
            self.setup.next_turn()
            execute_pre_scoring(
                self.setup, self.p_ai[0], self.p_zero_name, self.p_zero_type)

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
        
        return p_zero_score, p_one_score, p_zero_draft, p_one_draft, p_zero_indivs, p_one_indivs, self.setup.p_zero_grid, self.setup.p_one_grid, p_zero_bonus_score, p_one_bonus_score


#game = usurperGame("UsurperBot1", "UsurperBot2", 'AI', 'AI','full','full',
#                   'X2','X8',
#                   ['B10', 'Y7', 'Y1', 'G3', 'R2', 'G2', 'R7', 'G6', 'G4', 'R11', 'Y8', 'Y4', 'B2', 'G1', 'R8', 'Y6', 'Y11', 'B8', 'Y2', 'B5', 'Y10', 'B9', 'B1', 'B7', 'G8', 'R6', 'Y3', 'B11', 'R1', 'G9', 'B4', 'Y5', 'Y9', 'R3', 'B3', 'R5', 'B6', 'R4', 'G7', 'G11', 'G5', 'R10', 'R9', 'G10'],
#                   1)
#game.mainLoop()
