from gameBonus import gameBonus
from gameBonusDeck import gameBonusDeck
from gameCard import gameCard
from gameDeck import gameDeck
from gameSetup import gameSetup
from utilities import evaluation
from utilities import check_possible_placement
from utilities import check_if_legal
from utilities import grid_deep_copy
from utilities import execute_instant
from utilities import execute_pre_scoring
import random
import numpy as np
import itertools
import scipy.stats

instant_priority = {'Y5': 0, 'G4': 1, 'R10': 2, 'R9': 3,
                    'R2': 4, 'R7': 5, 'R4': 6, 'R8': 7, 'Y8': 8,'N0': 9}
for color in ['R', 'G', 'Y', 'B']:
    for num in range(1, 12):
        if color+str(num) not in instant_priority:
            instant_priority[color+str(num)] = 3.5
N0 = gameCard('dummy', 'N0', 0, '', 0, 0, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, '', True)


class gameAI:
    def __init__(self, player_num, mode, order_cutoff = False):
        self.mode = mode
        self.order_cutoff = order_cutoff
        self.player_num = player_num
        deck_inst = gameDeck()
        self.possible_opp_cards = deck_inst.deck.copy()
        self.confirmed_opp_cards = []
        self.max_unknown = 0
        bonus_deck_inst = gameBonusDeck()
        self.possible_opp_bonus_cards = bonus_deck_inst.deck.copy()
        self.last_plan = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.last_order = []
        self.last_cpx_order = []
        self.last_cpy_order = []
        self.g7_plan = {'decision': 'n', 'move_x': -1,
                        'move_y': -1, 'target_x': -1, 'target_y': -1}
        self.flip_ids = [['', '', ''], ['', '', ''], ['', '', '']]
        self.new_plan = True

    def player_see_card(self, card):
        if card.card_id in ['N0', 'A0', 'dA0']:
            return
        equiv_card = self.possible_opp_cards[[
            c.card_id for c in self.possible_opp_cards].index(card.card_id)]
        self.possible_opp_cards.remove(equiv_card)

    def player_see_bonus(self, card):
        equiv_card = self.possible_opp_bonus_cards[[
            c.card_id for c in self.possible_opp_bonus_cards].index(card.card_id)]
        self.possible_opp_bonus_cards.remove(equiv_card)

    def opp_draft_card(self, card):
        if card.card_id in ['N0', 'A0', 'dA0']:
            return
        equiv_card_idx = [
            c.card_id for c in self.possible_opp_cards].index(card.card_id)
        self.confirmed_opp_cards.append(
            self.possible_opp_cards.pop(equiv_card_idx))

    def opp_draw_card(self):
        self.max_unknown += 1

    def opp_discard(self, card, g4=False):
        if card.card_id in ['N0', 'A0', 'dA0']:
            return
        if card.card_id in [c.card_id for c in self.possible_opp_cards]:
            equiv_card = self.possible_opp_cards[[
                c.card_id for c in self.possible_opp_cards].index(card.card_id)]
            self.possible_opp_cards.remove(equiv_card)
            if g4:
                self.max_unknown -= 1
        else:
            equiv_card = self.confirmed_opp_cards[[
                c.card_id for c in self.confirmed_opp_cards].index(card.card_id)]
            self.confirmed_opp_cards.remove(equiv_card)

    def opp_play_card(self, card):
        if card.card_id in ['N0', 'A0', 'dA0']:
            return
        if card.card_id in [c.card_id for c in self.possible_opp_cards]:
            equiv_card = self.possible_opp_cards[[
                c.card_id for c in self.possible_opp_cards].index(card.card_id)]
            self.possible_opp_cards.remove(equiv_card)
            self.max_unknown -= 1
        else:
            equiv_card = self.confirmed_opp_cards[[
                c.card_id for c in self.confirmed_opp_cards].index(card.card_id)]
            self.confirmed_opp_cards.remove(equiv_card)

    def deck_to_board(self, card):
        if card.card_id in ['N0', 'A0', 'dA0']:
            return
        equiv_card = self.possible_opp_cards[[
            c.card_id for c in self.possible_opp_cards].index(card.card_id)]
        self.possible_opp_cards.remove(equiv_card)

    def average_card(self, deck=False):
        unknown_sum_red = sum(
            [card.color == 'R' for card in self.possible_opp_cards])
        unknown_sum_green = sum(
            [card.color == 'G' for card in self.possible_opp_cards])
        unknown_sum_blue = sum(
            [card.color == 'B' for card in self.possible_opp_cards])
        unknown_sum_yellow = sum(
            [card.color == 'Y' for card in self.possible_opp_cards])
        unknown_sum_hands = sum(
            [card.hands for card in self.possible_opp_cards])
        unknown_sum_eyes = sum([card.eyes for card in self.possible_opp_cards])
        unknown_sum_bags = sum([card.bags for card in self.possible_opp_cards])
        unknown_sum_ones = sum([(card.base_points == 1)
                               for card in self.possible_opp_cards])
        unknown_sum_zeroes = sum([(card.base_points == 0)
                                 for card in self.possible_opp_cards])
        unknown_sum_four_pluses = sum(
            [(card.base_points > 3) for card in self.possible_opp_cards])
        unknown_sum_points = sum(
            [card.base_points for card in self.possible_opp_cards])

        if deck:
            dA0 = gameCard('average', 'dA0', unknown_sum_points/len(self.possible_opp_cards), '', unknown_sum_hands/len(self.possible_opp_cards), unknown_sum_eyes/len(self.possible_opp_cards), unknown_sum_bags/len(self.possible_opp_cards), [
                [1, 1, 1], [1, 1, 1], [1, 1, 1]], False, '')

            d_exp_dict = {'red': unknown_sum_red/len(self.possible_opp_cards), 'blue': unknown_sum_blue/len(self.possible_opp_cards), 'yellow': unknown_sum_yellow/len(
                self.possible_opp_cards), 'green': unknown_sum_green/len(self.possible_opp_cards), 'zero': unknown_sum_zeroes/len(self.possible_opp_cards), 'one': unknown_sum_ones/len(self.possible_opp_cards), 'four_plus': unknown_sum_four_pluses/len(self.possible_opp_cards)}

            return d_exp_dict, dA0

        known_sum_red = sum(
            [card.color == 'R' for card in self.confirmed_opp_cards])
        known_sum_green = sum(
            [card.color == 'G' for card in self.confirmed_opp_cards])
        known_sum_blue = sum(
            [card.color == 'B' for card in self.confirmed_opp_cards])
        known_sum_yellow = sum(
            [card.color == 'Y' for card in self.confirmed_opp_cards])
        known_sum_hands = sum(
            [card.hands for card in self.confirmed_opp_cards])
        known_sum_eyes = sum([card.eyes for card in self.confirmed_opp_cards])
        known_sum_bags = sum([card.bags for card in self.confirmed_opp_cards])
        known_sum_ones = sum([(card.base_points == 1)
                             for card in self.confirmed_opp_cards])
        known_sum_zeroes = sum([(card.base_points == 0)
                               for card in self.confirmed_opp_cards])
        known_sum_four_pluses = sum(
            [(card.base_points > 3) for card in self.confirmed_opp_cards])
        known_sum_points = sum(
            [card.base_points for card in self.confirmed_opp_cards])

        hand_size = len(self.possible_opp_cards) + \
            len(self.confirmed_opp_cards)
        unknown_proportion = self.max_unknown / len(self.possible_opp_cards)

        exp_red = (known_sum_red + (unknown_sum_red *
                   unknown_proportion)) / hand_size
        exp_green = (known_sum_green + (unknown_sum_green *
                     unknown_proportion)) / hand_size
        exp_blue = (known_sum_blue + (unknown_sum_blue *
                    unknown_proportion)) / hand_size
        exp_yellow = (known_sum_yellow + (unknown_sum_yellow *
                      unknown_proportion)) / hand_size
        exp_zeroes = (known_sum_zeroes + (unknown_sum_zeroes *
                      unknown_proportion)) / hand_size
        exp_ones = (known_sum_ones + (unknown_sum_ones *
                    unknown_proportion)) / hand_size
        exp_four_pluses = (known_sum_four_pluses +
                           (unknown_sum_four_pluses * unknown_proportion)) / hand_size

        exp_hands = (known_sum_hands + (unknown_sum_hands *
                     unknown_proportion)) / hand_size
        exp_eyes = (known_sum_eyes + (unknown_sum_eyes *
                    unknown_proportion)) / hand_size
        exp_bags = (known_sum_bags + (unknown_sum_bags *
                    unknown_proportion)) / hand_size
        exp_points = (known_sum_points + (unknown_sum_points *
                      unknown_proportion)) / hand_size

        A0 = gameCard('average', 'A0', exp_points, '', exp_hands, exp_eyes, exp_bags, [
                      [1, 1, 1], [1, 1, 1], [1, 1, 1]], False, '')

        exp_dict = {'red': exp_red, 'blue': exp_blue, 'yellow': exp_yellow,
                    'green': exp_green, 'zero': exp_zeroes, 'one': exp_ones, 'four_plus': exp_four_pluses}

        return exp_dict, A0

    def draft_decision(self, setup):
        if self.player_num == 0:
            player_hand = setup.p_zero_hand
            player_grid = setup.p_zero_grid
        else:
            player_hand = setup.p_one_hand
            player_grid = setup.p_one_grid

        if self.mode == 'full':
            # TODO MAKE DRAFT DECISION
            for i in range(6):
                if check_if_legal(player_grid,player_hand+[setup.draft_options[i]]):
                    return i
            return 0
        elif self.mode == 'random':
            for i in range(6):
                if check_if_legal(player_grid,player_hand+[setup.draft_options[i]]):
                    return i
            return random.choice(range(6))

    def play_decision(self, setup):
        if self.player_num == 0:
            player_hand = setup.p_zero_hand
            player_bonus = setup.p_zero_bonus
            player_grid = setup.p_zero_grid
            opponent_grid = setup.p_one_grid
        else:
            player_hand = setup.p_one_hand
            player_bonus = setup.p_one_bonus
            player_grid = setup.p_one_grid
            opponent_grid = setup.p_zero_grid

        if self.mode == 'full':
            if self.new_plan == False or (self.g7_plan['decision'] == 'y' and self.last_order[0].name == 'G7'):
                print([card.card_id for card in player_hand])
                print([card.card_id for card in self.last_order])
                card_selection_index = [card.name for card in player_hand].index(
                    self.last_order[0].name)
                self.last_order = self.last_order[1:]
                return card_selection_index, self.last_cpx_order.pop(0), self.last_cpy_order.pop(0)

            best_score = -50
            best_plan = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            best_order = []
            best_g7_plan = {'decision': 'n', 'move_x': -1,
                            'move_y': -1, 'target_x': -1, 'target_y': -1}
            best_next_card_name = ''
            best_cpx_order = []
            best_cpy_order = []
            best_flip_ids = [['', '', ''], ['', '', ''], ['', '', '']]

            player_fill_dict, player_fill_card = self.average_card(True)
            opponent_fill_dict, opponent_fill_card = self.average_card()

            master_test_grid, open_spot_count = grid_deep_copy(player_grid)

            combo_length = open_spot_count
            found_possible_combo = False
            while not found_possible_combo:
                all_combos = list(itertools.combinations(
                    player_hand, combo_length))
                random.Random(4).shuffle(all_combos)
                for combo_base in all_combos:
                    if check_if_legal(player_grid, combo_base):
                        found_possible_combo = True
                    else:
                        continue
                    
                    combo = list(combo_base)
                    for i in range(open_spot_count-combo_length):
                        combo.append(N0.__copy__())

                    grid_sum = 0
                    for i in range(len(combo)):
                        grid_sum += sum(
                            [item != 0 for sublist in combo[i].placement_grid for item in sublist])

                    if sum([card.activation for card in combo]) > 0 and grid_sum > 54 and check_if_legal(player_grid,combo,True):
                        pluses_floor = 1
                    else:
                        pluses_floor = 0

                    all_scores = []
                    all_orders = list(itertools.permutations(combo))
                    random.Random(4).shuffle(all_orders)
                    num_orders = len(all_orders)
                    tested_orders = 0
                    valid_orders = 0
                    for order in all_orders:
                        tested_orders += 1
                        order_list = list(order)
                        out_of_place = 0
                        if 'G7' in [card.card_id for card in order_list] and open_spot_count>2 and (master_test_grid[1][2] == 0 or master_test_grid[2][0] == 0):
                            out_of_place_limit = 2
                        else:
                            out_of_place_limit = 1
                        order_list = [card.__copy__() for card in order_list]
                        order_distributor = order_list.copy()
                        test_grid, _ = grid_deep_copy(player_grid)
                        
                        pluses = 0
                        g7_target_x = -1
                        g7_target_y = -1
                        g7_placement_x = -1
                        g7_placement_y = -1
                        g7_move_options = []
                        for i in range(3):
                            if out_of_place == out_of_place_limit:
                                break
                            for j in range(3):
                                if test_grid[i][j] == 0:
                                    if order_distributor[0].placement_grid[i][j] == 0:
                                        out_of_place += 1
                                        if out_of_place == out_of_place_limit:
                                            break
                                        possible = False
                                        for k in range(9):
                                            if order_distributor[0].placement_grid[k//3][k%3] != 0 and master_test_grid[k//3][k%3] == 0 and set([(k//3 , k%3), (i, j)]) != set([(2,0),(1,2)]):
                                                possible = True
                                                g7_move_options.append((k//3,k%3))
                                        if possible:
                                            g7_card_id = order_distributor[0].card_id
                                            g7_target_x = i
                                            g7_target_y = j
                                        else:
                                            out_of_place = out_of_place_limit
                                            break
                                    elif order_distributor[0].placement_grid[i][j] == 2:
                                        pluses += 1
                                    if order_distributor[0].card_id == 'G7':
                                        g7_placement_x = i
                                        g7_placement_y = j
                                    test_grid[i][j] = order_distributor.pop(0)
                        if out_of_place == out_of_place_limit or pluses < pluses_floor:
                            continue
                        if out_of_place == 1 and out_of_place_limit == 2 and (('G7' not in [test_grid[1][2].card_id, test_grid[2][0].card_id]) or (g7_placement_x, g7_placement_y) == (g7_target_x, g7_target_y) or (len(g7_move_options)==1 and g7_move_options[0] == (g7_placement_x,g7_placement_y))):
                            continue

                        valid_orders += 1
                        sorted_order = order_list.copy()
                        sorted_order.sort(
                            key=lambda x: instant_priority[x.card_id])
                        order_ids = [card.card_id for card in sorted_order]
                        g7_bloc = [0, 0]
                        if 'G7' in order_ids and out_of_place == 1:
                            if order_ids.index('G7') > order_ids.index(g7_card_id):
                                g7_bloc[1] = sorted_order.pop(
                                    order_ids.index('G7'))
                                g7_bloc[0] = sorted_order.pop(
                                    order_ids.index(g7_card_id))
                            else:
                                g7_bloc[0] = sorted_order.pop(
                                    order_ids.index(g7_card_id))
                                g7_bloc[1] = sorted_order.pop(
                                    order_ids.index('G7'))
                            order_ids = [card.card_id for card in sorted_order]

                        if 'Y1' in order_ids:
                            y1_bloc = [sorted_order.pop(order_ids.index('Y1'))]
                        if 'R11' in order_ids:
                            cutoff = 6
                        else:
                            cutoff = 4
                        less_than_cut = list(filter(
                            lambda x: x.base_points < cutoff and x.card_id not in ['B7','N0'], sorted_order))
                        cut_or_more = list(filter(
                            lambda x: x.base_points > cutoff - 1 or x.card_id == 'B7', sorted_order))
                        filler_cards = list(filter(lambda x: x.card_id == 'N0', sorted_order))
                        if 'Y1' in order_ids:
                            sorted_order = less_than_cut + y1_bloc + cut_or_more + filler_cards
                        else:
                            sorted_order = less_than_cut + cut_or_more + filler_cards
                        order_ids = [card.card_id for card in sorted_order]

                        if g7_bloc != [0, 0]:
                            g7_test_sorted_order = sorted_order.copy()
                            g7_test_grid = master_test_grid.copy()
                            flat_grid_ids = [item.card_id for sublist in test_grid for item in sublist]
                            g7_test_grid[g7_placement_x][g7_placement_y] = g7_bloc[1]
                            insert_idx = 0
                            Y1_or_N0_found = False
                            g7_move_x = -1
                            g7_move_y = -1
                            for x in range(len(g7_test_sorted_order)):
                                grid_index = flat_grid_ids.index(g7_test_sorted_order[0].card_id)
                                i = grid_index//3
                                j = grid_index%3
                                if g7_test_sorted_order[0].card_id in ['Y1','N0']:
                                    Y1_or_N0_found = True
                                else:
                                    g7_test_grid[i][j] = g7_test_sorted_order.pop(0)
                                if g7_bloc[0].placement_grid[i][j] != 0:
                                    g7_move_x = i
                                    g7_move_y = j
                                if not check_possible_placement(g7_test_grid, g7_bloc, True, 0) or Y1_or_N0_found or (g7_bloc[0].instant and g7_bloc[0].placement_grid[i][j] == 2) or len(g7_test_sorted_order) == 0:
                                    sorted_order = sorted_order[:insert_idx] + \
                                        g7_bloc + \
                                        sorted_order[insert_idx:]
                                    if (g7_move_x, g7_move_y) == (-1,-1):
                                        for k in range(3):
                                            for l in range(3):
                                                if g7_test_grid[k][l] == 0 and g7_bloc[0].placement_grid[k][l] != 0:
                                                    g7_move_x = k
                                                    g7_move_y = l
                                    break
                                insert_idx += 1
                            order_ids = [card.card_id for card in sorted_order]
                        # REMOVE LATER, JUST FOR SHOW
                        # print_card_list(test_grid[0])
                        # print_card_list(test_grid[1])
                        # print_card_list(test_grid[2])
                        test_setup = gameSetup()
                        test_setup.main_deck.deck = []
                        for i in range(len(setup.main_deck.deck)):
                            test_setup.main_deck.deck.append(
                                player_fill_card.__copy__())
                        test_setup.possible_opp_cards = self.possible_opp_cards.copy()
                        test_setup.confirmed_opp_cards = self.confirmed_opp_cards.copy()
                        test_setup.max_unknown = self.max_unknown
                        test_setup.possible_bonus_cards = self.possible_opp_bonus_cards.copy()
                        self.last_plan, _ = grid_deep_copy(test_grid)
                        self.flip_ids = [['', '', ''], ['', '', ''], ['', '', '']]

                        if self.player_num == 0:
                            test_setup.p_zero_grid, _ = grid_deep_copy(player_grid)
                            test_setup.p_one_grid, fill_card_count = grid_deep_copy(
                                opponent_grid)
                            test_setup.p_zero_bonus = player_bonus
                            test_setup.p_one_bonus = self.possible_opp_bonus_cards
                            test_setup.p_zero_hand = sorted_order.copy()
                            for i in range(fill_card_count):
                                test_setup.p_one_hand.append(
                                    opponent_fill_card.__copy__())
                            test_setup.turn = 0
                        else:
                            test_setup.p_one_grid, _ = grid_deep_copy(player_grid)
                            test_setup.p_zero_grid, fill_card_count = grid_deep_copy(
                                opponent_grid)
                            test_setup.p_one_bonus = player_bonus
                            test_setup.p_zero_bonus = self.possible_opp_bonus_cards
                            test_setup.p_one_hand = sorted_order.copy()
                            for i in range(fill_card_count):
                                test_setup.p_zero_hand.append(
                                    opponent_fill_card.__copy__())
                            test_setup.turn = 1

                        extra_flipped = 0
                        cpx_list = []
                        cpy_list = []
                        for i in range(len(sorted_order)):
                            found = False
                            for x in range(3):
                                for y in range(3):
                                    if test_grid[x][y].card_id == sorted_order[i].card_id:
                                        test_setup.play_card(
                                            self.player_num, 0, x, y)
                                        if g7_bloc != [0, 0] and sorted_order[i].card_id == g7_bloc[0].card_id:
                                            cpx_list.append(g7_move_x)
                                            cpy_list.append(g7_move_y)
                                        else:
                                            cpx_list.append(x)
                                            cpy_list.append(y)
                                        found = True
                                        break
                                if found:
                                    break
                            if (sorted_order[i].card_id in ['R7', 'R4', 'R8', 'Y8'] and sorted_order[i].placement_grid[x][y] == 2) or sorted_order[i].card_id == 'Y1':
                                execute_instant(test_setup, self.player_num, [
                                                self, self], 'filler', 'filler', 'AI', 'AI', x, y, True)
                                if sorted_order[i].card_id == 'R4':
                                    extra_flipped = i * \
                                        opponent_fill_dict['four_plus']
                            if sum([item == 0 for sublist in [test_setup.p_zero_grid, test_setup.p_one_grid][abs(self.player_num - 1)] for item in sublist]) > 0:
                                test_setup.next_turn()
                                found = False
                                for x in range(3):
                                    for y in range(3):
                                        if [test_setup.p_zero_grid, test_setup.p_one_grid][abs(self.player_num - 1)][x][y] == 0:
                                            test_setup.play_card(
                                                abs(self.player_num - 1), 0, x, y)
                                            found = True
                                            break
                                    if found:
                                        break
                                test_setup.next_turn()
                        execute_pre_scoring(
                            test_setup, self, 'filler', 'AI', test=True)
                        test_setup.next_turn()
                        execute_pre_scoring(
                            test_setup, self, 'filler', 'AI', test=True)

                        if self.player_num == 0:
                            test_score = evaluation(test_setup.p_zero_grid, test_setup.p_one_grid, test_setup.p_zero_bonus,
                                                    opponent_fill_dict, opponent_fill_card, player_fill_dict, extra_flipped=extra_flipped)
                            test_final_grid = test_setup.p_zero_grid
                        else:
                            test_score = evaluation(test_setup.p_one_grid, test_setup.p_zero_grid, test_setup.p_one_bonus,
                                                    opponent_fill_dict, opponent_fill_card, player_fill_dict, extra_flipped=extra_flipped)
                            test_final_grid = test_setup.p_one_grid

                        all_scores.append(test_score)

                        if test_score > best_score:
                            best_score = test_score
                            best_plan, _ = grid_deep_copy(test_final_grid)
                            best_order = sorted_order
                            best_next_card_name = sorted_order[0].name
                            best_cpx_order = cpx_list
                            best_cpy_order = cpy_list
                            best_flip_ids = self.flip_ids.copy()
                            if g7_bloc != [0, 0]:
                                best_g7_plan = {'decision': 'y', 'move_x': g7_move_x,
                                                'move_y': g7_move_y, 'target_x': g7_target_x, 'target_y': g7_target_y}
                            else:
                                best_g7_plan = {
                                    'decision': 'n', 'move_x': -1, 'move_y': -1, 'target_x': -1, 'target_y': -1}
                                
                        if self.order_cutoff and num_orders > 2000 and tested_orders > num_orders/2 and valid_orders % 5 == 0:
                            curr_mean = np.mean(all_scores)
                            curr_std = np.std(all_scores)
                            remaining_orders = round(
                                valid_orders/tested_orders * (num_orders-tested_orders))
                            chance_of_better = scipy.stats.norm.sf(
                                best_score+5, curr_mean, curr_std)
                            chance_over_time = scipy.stats.binom.sf(
                                k=0, n=remaining_orders, p=chance_of_better)
                            if chance_over_time < 0.10:
                                print('saved:')
                                print(remaining_orders)
                                break
                if not found_possible_combo:
                    combo_length -= 1

            self.last_plan = best_plan
            self.last_order = list(filter(lambda x: x.card_id != 'N0', best_order[1:]))
            self.g7_plan = best_g7_plan
            self.last_cpx_order = best_cpx_order
            self.last_cpy_order = best_cpy_order
            self.flip_ids = best_flip_ids
            self.new_plan = False

            card_selection_index = [
                card.name for card in player_hand].index(best_next_card_name)
            
            print([card.card_id for card in self.last_order])
            print(self.g7_plan)

            return card_selection_index, self.last_cpx_order.pop(0), self.last_cpy_order.pop(0)

        elif self.mode == 'random':
            card_selection_index = -1
            while card_selection_index == -1 or not check_possible_placement(player_grid, player_hand, True, card_selection_index):
                card_selection_index = random.choice(range(len(player_hand)))
            card_placement_x = -1
            card_placement_y = -1
            while -1 in [card_placement_x, card_placement_y] or player_grid[card_placement_x][card_placement_y] != 0 or player_hand[card_selection_index].placement_grid[card_placement_x][card_placement_y] == 0:
                card_placement_x = random.choice(range(3))
                card_placement_y = random.choice(range(3))
            return card_selection_index, card_placement_x, card_placement_y

    def instant_decision(self, setup, instant_id, i=0, j=0, test=False):
        if self.player_num == 0:
            player_hand = setup.p_zero_hand
            player_bonus = setup.p_zero_bonus
            player_grid = setup.p_zero_grid
            opponent_grid = setup.p_one_grid
        else:
            player_hand = setup.p_one_hand
            player_bonus = setup.p_one_bonus
            player_grid = setup.p_one_grid
            opponent_grid = setup.p_zero_grid
        if instant_id == 'R2':
            self.new_plan = True
            if self.mode == 'full':
                replacement_dict, replacement_card = self.average_card(True)
                opponent_fill_dict, opponent_fill_card = self.average_card()
                card_placement_x = -1
                card_placement_y = -1
                best = 0
                for x in range(3):
                    for y in range(3):
                        if player_grid[x][y] != 0:
                            test_grid, _ = grid_deep_copy(self.last_plan)
                            if test_grid[x][y].name != player_grid[x][y].name:
                                continue
                            test_grid[x][y] = replacement_card
                            player_score_xy = evaluation(
                                test_grid, opponent_grid, player_bonus, opponent_fill_dict, opponent_fill_card, replacement_dict)
                            if player_score_xy > best:
                                best = player_score_xy
                                card_placement_x = x
                                card_placement_y = y
                return card_placement_x, card_placement_y
            elif self.mode == 'random':
                card_placement_x = -1
                card_placement_y = -1
                while -1 in [card_placement_x, card_placement_y] or player_grid[card_placement_x][card_placement_y] == 0:
                    card_placement_x = random.choice(range(3))
                    card_placement_y = random.choice(range(3))
                return card_placement_x, card_placement_y
        elif instant_id == 'R4':
            if self.mode == 'full':
                if not test:
                    for x in range(3):
                        for y in range(3):
                            if self.flip_ids[x][y] == instant_id:
                                return 'y', x, y
                    return 'n', -1, -1
                opponent_fill_dict, opponent_fill_card = self.average_card()
                card_placement_x = -1
                card_placement_y = -1
                best = evaluation(self.last_plan, opponent_grid,
                                  player_bonus, opponent_fill_dict, opponent_fill_card)
                decision = 'n'

                for x in range(3):
                    for y in range(3):
                        if player_grid[x][y] != 0:
                            test_grid, _ = grid_deep_copy(self.last_plan)
                            test_grid[x][y].flip()
                            player_score_xy = evaluation(
                                test_grid, opponent_grid, player_bonus, opponent_fill_dict, opponent_fill_card)
                            if player_score_xy > best:
                                decision = 'y'
                                self.new_plan = True
                                best = player_score_xy
                                card_placement_x = x
                                card_placement_y = y
                if decision == 'y':
                    self.flip_ids[card_placement_x][card_placement_y] = instant_id
                return decision, card_placement_x, card_placement_y
            elif self.mode == 'random':
                decision = random.choice(['y', 'n'])
                flip_x = -1
                flip_y = -1
                if decision == 'n':
                    return decision, flip_x, flip_y
                while -1 in [flip_x, flip_y] or player_grid[flip_x][flip_y] == 0:
                    flip_x = random.choice(range(3))
                    flip_y = random.choice(range(3))
                self.new_plan = True
                return decision, flip_x, flip_y
        elif instant_id == 'R7':
            if self.mode == 'full':
                replacement_dict, replacement_card = self.average_card(True)
                opponent_fill_dict, opponent_fill_card = self.average_card()
                replacement_x = -1
                replacement_y = -1
                best = evaluation(self.last_plan, opponent_grid,
                                  player_bonus, opponent_fill_dict, opponent_fill_card)
                decision = 'n'
                for x in range(3):
                    for y in range(3):
                        if player_grid[x][y] != 0:
                            test_grid, _ = grid_deep_copy(self.last_plan)
                            test_grid[x][y] = replacement_card
                            player_score_xy = evaluation(
                                test_grid, opponent_grid, player_bonus, opponent_fill_dict, opponent_fill_card, replacement_dict)
                            if player_score_xy > best:
                                decision = 'y'
                                self.new_plan = True
                                best = player_score_xy
                                replacement_x = x
                                replacement_y = y
                return decision, replacement_x, replacement_y
            elif self.mode == 'random':
                decision = random.choice(['y', 'n'])
                replacement_x = -1
                replacement_y = -1
                if decision == 'n':
                    return decision, replacement_x, replacement_y
                while -1 in [replacement_x, replacement_y] or player_grid[replacement_x][replacement_y] == 0:
                    replacement_x = random.choice(range(3))
                    replacement_y = random.choice(range(3))
                self.new_plan = True
                return decision, replacement_x, replacement_y
        elif instant_id == 'R8':
            if self.mode == 'full':
                opponent_fill_dict, opponent_fill_card = self.average_card()
                flip_x = -1
                flip_y = -1
                best = 999

                master_test_opp_grid = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
                for x in range(3):
                    for y in range(3):
                        if opponent_grid[x][y] == 0:
                            master_test_opp_grid[x][y] = opponent_fill_card.__copy__(
                            )
                        else:
                            master_test_opp_grid[x][y] = opponent_grid[x][y].__copy__(
                            )

                for x in range(3):
                    for y in range(3):
                        if opponent_grid[x][y] != 0:
                            test_grid, _ = grid_deep_copy(master_test_opp_grid)
                            test_grid[x][y].flip()
                            opp_score_xy = evaluation(
                                test_grid, self.last_plan, self.possible_opp_bonus_cards, d_exp_dict=opponent_fill_dict)
                            if opp_score_xy < best:
                                best = opp_score_xy
                                flip_x = x
                                flip_y = y
                return flip_x, flip_y
            elif self.mode == 'random':
                flip_x = -1
                flip_y = -1
                while -1 in [flip_x, flip_y] or opponent_grid[flip_x][flip_y] == 0:
                    flip_x = random.choice(range(3))
                    flip_y = random.choice(range(3))
                return flip_x, flip_y
        elif instant_id == 'R10':
            self.new_plan = True
            if self.mode == 'full':
                # TODO UPDATE WITH DRAFTING WEIGHTS
                return 0
            elif self.mode == 'random':
                return 0
        elif instant_id == 'Y8':
            if self.mode == 'full':
                if not test:
                    if self.flip_ids[i][j] == instant_id:
                        return 'y'
                    else:
                        return 'n'
                test_grid, _ = grid_deep_copy(self.last_plan)
                player_score_n = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_n = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                n_avg = player_score_n - opp_score_n
                test_grid[i][j].flip()
                player_score_y = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_y = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                y_avg = player_score_y - opp_score_y
                if y_avg > n_avg:
                    self.flip_ids[i][j] == instant_id
                    return 'y'
                else:
                    return 'n'
            elif self.mode == 'random':
                return random.choice(['y', 'n'])
        elif instant_id == 'G4':
            self.new_plan = True
            if self.mode == 'full':
                if len(setup.draft_options) == 0:
                    replacement_dict, replacement_card = self.average_card(
                        True)
                    opponent_fill_dict, opponent_fill_card = self.average_card()
                    card_selection_x = -1
                    best = 0
                    for x in range(len(player_hand)):
                        test_grid, _ = grid_deep_copy(self.last_plan)
                        flat_test_grid = [
                            item.name for sublist in test_grid for item in sublist]
                        if player_hand[x].name not in flat_test_grid:
                            return x
                        flat_index = flat_test_grid.index(
                            player_hand[x].name)
                        test_grid[flat_index//3][flat_index %
                                                 3] = replacement_card
                        player_score_x = evaluation(
                            test_grid, opponent_grid, player_bonus, opponent_fill_dict, opponent_fill_card, replacement_dict)
                        if player_score_x > best:
                            best = player_score_x
                            card_placement_x = x
                    return card_selection_x
                else:
                    # TODO UPDATE WITH DRAFTING WEIGHTS
                    for card_selection_x in range(3):
                        if check_if_legal(player_grid,player_hand+[setup.draft_options[card_selection_x]]):
                            return card_selection_x
                    return 0
                        
            elif self.mode == 'random':
                if len(setup.draft_options) == 0:
                    return random.choice(range(len(player_hand)))
                else:
                    for card_selection_x in range(3):
                        if check_if_legal(player_grid,player_hand+[setup.draft_options[card_selection_x]]):
                            return card_selection_x
                    return 0
        elif instant_id == 'G7':
            if self.mode == 'full':
                return self.g7_plan['decision'], self.g7_plan['move_x'], self.g7_plan['move_y'], self.g7_plan['target_x'], self.g7_plan['target_y']
            elif self.mode == 'random':
                decision = random.choice(['y', 'n'])
                move_x = -1
                move_y = -1
                target_x = -1
                target_y = -1
                if decision == 'n':
                    return decision, move_x, move_y, target_x, target_y
                while -1 in [move_x, move_y] or player_grid[move_x][move_y] == 0:
                    move_x = random.choice(range(3))
                    move_y = random.choice(range(3))
                while -1 in [target_x, target_y] or player_grid[target_x][target_y] != 0:
                    target_x = random.choice(range(3))
                    target_y = random.choice(range(3))
                return decision, move_x, move_y, target_x, target_y

    def pre_score_decision(self, setup, pre_score_id, i, j, test=False):
        if setup.turn==0:
            player_bonus = setup.p_zero_bonus
            player_grid = setup.p_zero_grid
            opponent_grid = setup.p_one_grid
        else:
            player_bonus = setup.p_one_bonus
            player_grid = setup.p_one_grid
            opponent_grid = setup.p_zero_grid
        if pre_score_id == 'G3':
            if self.mode == 'full':
                test_grid, _ = grid_deep_copy(player_grid)
                player_score_n = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_n = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                n_avg = player_score_n - opp_score_n
                test_grid[i][j].g3_copy(test_grid[i][j+1])
                player_score_y = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_y = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                y_avg = player_score_y - opp_score_y
                if y_avg > n_avg:
                    return 'y'
                else:
                    return 'n'
            elif self.mode == 'random':
                return random.choice(['y', 'n'])
        elif pre_score_id == 'G5':
            if self.mode == 'full':
                if not test and self.player_num == setup.turn:
                    if self.flip_ids[i][j] == pre_score_id:
                        return 'y'
                    else:
                        return 'n'
                test_grid, _ = grid_deep_copy(player_grid)
                player_score_n = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_n = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                n_avg = player_score_n - opp_score_n
                test_grid[i][j].flip()
                player_score_y = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_y = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                y_avg = player_score_y - opp_score_y
                if y_avg > n_avg:
                    if self.player_num == setup.turn:
                        self.flip_ids[i][j] = pre_score_id
                    return 'y'
                else:
                    return 'n'
            elif self.mode == 'random':
                return random.choice(['y', 'n'])
        elif pre_score_id == 'G6':
            if self.mode == 'full':
                if not test and self.player_num == setup.turn:
                    if self.flip_ids[i+1][j] == pre_score_id:
                        return 'y'
                    else:
                        return 'n'
                test_grid, _ = grid_deep_copy(player_grid)
                player_score_n = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_n = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                n_avg = player_score_n - opp_score_n
                test_grid[i+1][j].flip()
                player_score_y = evaluation(
                    test_grid, opponent_grid, player_bonus)
                opp_score_y = evaluation(
                    opponent_grid, test_grid, self.possible_opp_bonus_cards)
                y_avg = player_score_y - opp_score_y
                if y_avg > n_avg:
                    if self.player_num == setup.turn:
                        self.flip_ids[i][j] = pre_score_id
                    return 'y'
                else:
                    return 'n'
            elif self.mode == 'random':
                return random.choice(['y', 'n'])
