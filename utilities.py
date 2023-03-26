from gameBonus import gameBonus
from gameBonusDeck import gameBonusDeck
from gameCard import gameCard
from gameDeck import gameDeck
from gameSetup import gameSetup
import constraint

pair_list = []
for i in range(2):
    for j in range(3):
        pair_list.append(((i, j), (i+1, j)))
for i in range(3):
    for j in range(2):
        pair_list.append(((i, j), (i, j+1)))

N0 = gameCard('dummy', 'N0', 0, '', 0, 0, 0,
              [[1, 1, 1],
               [1, 1, 1],
               [1, 1, 1]], False, '', True)

def grid_deep_copy(grid,fill_card=0):
    new_grid = [[0,0,0],[0,0,0],[0,0,0]]
    fill_count = 0
    for i in range(3):
        for j in range(3):
            if grid[i][j] == 0:
                if fill_card==0:
                    new_grid[i][j] = grid[i][j]
                else:
                    new_grid[i][j] = fill_card.__copy__()
                fill_count+=1
            else:
                new_grid[i][j] = grid[i][j].__copy__()
    return new_grid, fill_count
                

def evaluation(player_grid_original, opponent_grid_original, player_bonus, exp_dict={}, avg_card=N0, d_exp_dict={}, extra_flipped = 0, individuals = False):
    
    player_grid, _ = grid_deep_copy(player_grid_original)
    opponent_grid, _ = grid_deep_copy(opponent_grid_original)

    d_avg_card_count = 0
    avg_card_count = 0

    for i in range(3):
        for j in range(3):
            if player_grid[i][j] == 0:
                player_grid[i][j] = N0
            elif player_grid[i][j].card_id in ['dA0','A0']:
                d_avg_card_count += 1
            if opponent_grid[i][j] == 0:
                if exp_dict != {}:
                    opponent_grid[i][j] = avg_card
                    avg_card_count += 1
                else:
                    opponent_grid[i][j] = N0
            elif opponent_grid[i][j].card_id in ['dA0','A0']:
                avg_card_count += 1
    if d_exp_dict != {}:
        d_extra_red = d_exp_dict['red'] * d_avg_card_count
        d_extra_blue = d_exp_dict['blue'] * d_avg_card_count
        d_extra_green = d_exp_dict['green'] * d_avg_card_count
        d_extra_yellow = d_exp_dict['yellow'] * d_avg_card_count
        d_extra_zero = d_exp_dict['zero'] * d_avg_card_count
        d_extra_one = d_exp_dict['one'] * d_avg_card_count
    else:
        d_extra_red = 0
        d_extra_blue = 0
        d_extra_green = 0
        d_extra_yellow = 0
        d_extra_zero = 0
        d_extra_one = 0


    if exp_dict != {}:
        extra_red = exp_dict['red'] * avg_card_count
        extra_blue = exp_dict['blue'] * avg_card_count
        extra_green = exp_dict['green'] * avg_card_count
        extra_yellow = exp_dict['yellow'] * avg_card_count
        extra_zero = exp_dict['zero'] * avg_card_count
        extra_one = exp_dict['one'] * avg_card_count
    else:
        extra_red = 0
        extra_blue = 0
        extra_green = 0
        extra_yellow = 0
        extra_zero = 0
        extra_one = 0
    
    for i in range(3):
        for j in range(3):
            current_card = player_grid[i][j]
            if current_card.flipped:
                continue
            current_id = current_card.card_id
            if current_card.color == 'R':
                if current_id == 'R1':
                    flat_grid = [
                        item.color == 'G' for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.color == 'G' for sublist in opponent_grid for item in sublist]
                    green_sum = sum(flat_grid)+sum(flat_opponent_grid) + extra_green + d_extra_green
                    current_card.changepoints(green_sum)
                elif current_id == 'R2':
                    pass
                elif current_id == 'R3':
                    pass
                elif current_id == 'R4':
                    pass
                elif current_id == 'R5':
                    flat_grid = [
                        item.eyes for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.eyes for sublist in opponent_grid for item in sublist]
                    eyes_sum = sum(flat_grid)+sum(flat_opponent_grid)
                    current_card.changepoints(eyes_sum)
                elif current_id == 'R6':
                    for adj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if adj[0] >= 0 and adj[0] <= 2 and adj[1] >= 0 and adj[1] <= 2:
                            current_card.changepoints(
                                (player_grid[adj[0]][adj[1]].color == 'R')*3)
                elif current_id == 'R7':
                    pass
                elif current_id == 'R8':
                    pass
                elif current_id == 'R9':
                    pass
                elif current_id == 'R10':
                    pass
                else:
                    flat_grid = [
                        item.flipped*6 for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.flipped*6 for sublist in opponent_grid for item in sublist]
                    flipped_sum = sum(flat_grid)+sum(flat_opponent_grid) + extra_flipped
                    current_card.changepoints(flipped_sum)
            elif current_card.color == 'Y':
                if current_id == 'Y1':
                    pass
                elif current_id == 'Y2':
                    flat_grid = [(item.base_points == 1 and not item.flipped)
                                 * 3 for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [(item.base_points == 1 and not item.flipped)
                                          * 3 for sublist in opponent_grid for item in sublist]
                    one_sum = sum(flat_grid)+sum(flat_opponent_grid) + extra_one + d_extra_one
                    current_card.changepoints(one_sum)
                elif current_id == 'Y3':
                    if current_card.placement_grid[i][j] == 2:
                        flat_grid = [
                            item.bags for sublist in player_grid for item in sublist]
                        bags_sum = sum(flat_grid)
                        current_card.changepoints(bags_sum)
                elif current_id == 'Y4':
                    red_sum = 0 - \
                        sum([player_grid[row][j].color == 'R' for row in range(3)]) - d_extra_red
                    current_card.changepoints(red_sum)
                elif current_id == 'Y5':
                    pass
                elif current_id == 'Y6':
                    for adj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if adj[0] >= 0 and adj[0] <= 2 and adj[1] >= 0 and adj[1] <= 2:
                            current_card.changepoints(
                                (player_grid[adj[0]][adj[1]].color in ['B', 'Y'])*2)
                elif current_id == 'Y7':
                    yellow_sum = sum(
                        [(player_grid[i][column].color == 'Y')*2 for column in range(3)]) + d_extra_yellow
                    current_card.changepoints(yellow_sum)
                elif current_id == 'Y8':
                    pass
                elif current_id == 'Y9':
                    flat_grid = [
                        item.color == 'B' for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.color == 'B' for sublist in opponent_grid for item in sublist]
                    blue_sum = sum(flat_grid)+sum(flat_opponent_grid) + extra_blue + d_extra_blue
                    current_card.changepoints(blue_sum)
                elif current_id == 'Y10':
                    flat_grid = [(item.og_base_points == 0 and not item.flipped and not item.dummy)
                                 * 2 for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [(item.og_base_points == 0 and not item.flipped and not item.dummy)
                                          * 2 for sublist in opponent_grid for item in sublist]
                    zero_sum = sum(flat_grid)+sum(flat_opponent_grid) + extra_zero + d_extra_zero
                    current_card.changepoints(zero_sum)
                else:
                    flat_grid = [
                        item.color == 'R' for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.color == 'R' for sublist in opponent_grid for item in sublist]
                    red_sum = 0-sum(flat_grid)-sum(flat_opponent_grid) - extra_red - d_extra_red
                    current_card.changepoints(red_sum)
            elif current_card.color == 'G':
                if current_id == 'G1':
                    flat_grid = [
                        item.color == 'G' for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.color == 'G' for sublist in opponent_grid for item in sublist]
                    green_sum = sum(flat_grid)+sum(flat_opponent_grid) + extra_green + d_extra_green
                    current_card.changepoints(green_sum)
                elif current_id == 'G2':
                    for adj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if adj[0] >= 0 and adj[0] <= 2 and adj[1] >= 0 and adj[1] <= 2:
                            current_card.changepoints(
                                (player_grid[adj[0]][adj[1]].color in ['R', 'G'])*3)
                elif current_id == 'G3':
                    pass
                elif current_id == 'G4':
                    pass
                elif current_id == 'G5':
                    pass
                elif current_id == 'G6':
                    pass
                elif current_id == 'G7':
                    pass
                elif current_id == 'G8':
                    eyes_sum = sum(
                        [player_grid[row][j].eyes*2 for row in range(3)])
                    current_card.changepoints(eyes_sum)
                elif current_id == 'G9':
                    flat_grid = [
                        item.hands for sublist in player_grid for item in sublist]
                    hands_sum = sum(flat_grid)
                    current_card.changepoints(hands_sum)
                elif current_id == 'G10':
                    for pair in pair_list:
                        if set([player_grid[pair[0][0]][pair[0][1]].color, player_grid[pair[1][0]][pair[1][1]].color]) == {'R', 'G'}:
                            current_card.changepoints(3)
                else:
                    pass
            else:
                if current_id == 'B1':
                    flat_grid = [
                        item.bags for sublist in player_grid for item in sublist]
                    bags_sum = sum(flat_grid)
                    current_card.changepoints(bags_sum)
                elif current_id == 'B2':
                    pass
                elif current_id == 'B3':
                    for adj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if adj[0] >= 0 and adj[0] <= 2 and adj[1] >= 0 and adj[1] <= 2:
                            current_card.changepoints(
                                (player_grid[adj[0]][adj[1]].color == 'B')*1)
                elif current_id == 'B4':
                    pass
                elif current_id == 'B5':
                    flat_grid = [
                        item.hands for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.hands for sublist in opponent_grid for item in sublist]
                    hands_sum = (sum(flat_grid)+sum(flat_opponent_grid))//2
                    current_card.changepoints(hands_sum)
                elif current_id == 'B6':
                    for adj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if adj[0] >= 0 and adj[0] <= 2 and adj[1] >= 0 and adj[1] <= 2:
                            current_card.changepoints(
                                (player_grid[adj[0]][adj[1]].color == 'R')*-1)
                elif current_id == 'B7':
                    flat_grid = [
                        item.hands for sublist in player_grid for item in sublist]
                    flat_opponent_grid = [
                        item.hands for sublist in opponent_grid for item in sublist]
                    hands_sum = sum(flat_grid)+sum(flat_opponent_grid)
                    if hands_sum < 8:
                        current_card.base_points = 1
                        current_card.changepoints(1-current_card.points)
                    elif hands_sum < 12:
                        current_card.base_points = 5
                        current_card.changepoints(5-current_card.points)
                    else:
                        current_card.base_points = 8
                        current_card.changepoints(8-current_card.points)
                elif current_id == 'B8':
                    if current_card.placement_grid[i][j] == 2:
                        flat_grid = [(item.base_points == 1 and not item.flipped)
                                     * 1 for sublist in player_grid for item in sublist]
                        one_sum = sum(flat_grid) + d_extra_one
                        current_card.changepoints(one_sum)
                elif current_id == 'B9':
                    flat_grid = [
                        (item.color == 'B')*2 for sublist in player_grid for item in sublist]
                    blue_sum = sum(flat_grid) + d_extra_blue
                    current_card.changepoints(blue_sum)
                elif current_id == 'B10':
                    pass
                elif current_id == 'B11':
                    hands_sum = sum(
                        [player_grid[i][column].hands for column in range(3)])
                    current_card.changepoints(hands_sum)
    
    bonus_points = 0
    for bonus in player_bonus:
        bonus_id = bonus.card_id
        if bonus_id == 'X1':
            player_grid[1][1].changepoints(player_grid[1][1].base_points)
            player_grid[1][1].base_points = player_grid[1][1].base_points*2
        elif bonus_id == 'X2':
            for i in range(3):
                for j in range(3):
                    for adj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                        if adj[0] >= 0 and adj[0] <= 2 and adj[1] >= 0 and adj[1] <= 2:
                            if player_grid[i][j].color == player_grid[adj[0]][adj[1]].color:
                                bonus_points += 2
                                break
        elif bonus_id == 'X3':
            flat_grid_hands = [
                item.hands for sublist in player_grid for item in sublist]
            flat_opponent_grid_hands = [
                item.hands for sublist in opponent_grid for item in sublist]
            flat_grid_eyes = [
                item.eyes for sublist in player_grid for item in sublist]
            flat_opponent_grid_eyes = [
                item.eyes for sublist in opponent_grid for item in sublist]
            flat_grid_bags = [
                item.bags for sublist in player_grid for item in sublist]
            flat_opponent_grid_bags = [
                item.bags for sublist in opponent_grid for item in sublist]
            bonus_points += 6*(sum(flat_grid_hands) >
                            sum(flat_opponent_grid_hands))
            bonus_points += 6*(sum(flat_grid_eyes) > sum(flat_opponent_grid_eyes))
            bonus_points += 6*(sum(flat_grid_bags) > sum(flat_opponent_grid_bags))
        elif bonus_id == 'X4':
            flat_grid = [(item.og_base_points < 3 and not item.flipped and not item.dummy)
                         * 2 for sublist in player_grid for item in sublist]
            bonus_points += sum(flat_grid)
        elif bonus_id == 'X5':
            flat_grid = [(item.color == 'R') *
                         2 for sublist in player_grid for item in sublist]
            bonus_points += sum(flat_grid)
        elif bonus_id == 'X6':
            flat_grid = [item.color for sublist in player_grid for item in sublist]
            bonus_points += len(list(set(flat_grid)-set([''])))*3
        elif bonus_id == 'X7':
            flat_grid = [item.hands for sublist in player_grid for item in sublist]
            flat_opponent_grid = [
                item.hands for sublist in opponent_grid for item in sublist]
            bonus_points += (sum(flat_grid)+sum(flat_opponent_grid))//2
        elif bonus_id == 'X8':
            flat_grid = [(item.color == 'G') *
                         2 for sublist in player_grid for item in sublist]
            bonus_points += sum(flat_grid)
        elif bonus_id == 'X9':
            flat_grid = [
                item.flipped for sublist in player_grid for item in sublist]
            flat_opponent_grid = [
                item.flipped for sublist in opponent_grid for item in sublist]
            flipped_sum = sum(flat_grid)+sum(flat_opponent_grid) + extra_flipped
            if flipped_sum > 1:
                bonus_points += flipped_sum*4
            else:
                bonus_points += 6
        elif bonus_id == 'X10':
            for pair in pair_list:
                if set([player_grid[pair[0][0]][pair[0][1]].color, player_grid[pair[1][0]][pair[1][1]].color]) == {'B', 'Y'}:
                    bonus_points += 4

    done = False
    for i in range(3):
        for j in range(2):
            if player_grid[i][j].g3_stored_data != {}:
                old_base = player_grid[i][j].base_points
                new_base = player_grid[i][j+1].base_points
                player_grid[i][j].base_points = new_base
                player_grid[i][j].changepoints(new_base-old_base)
                done = True
                break
        if done:
            break

    bonus_points = bonus_points / len(player_bonus)
    indiv_points = [item.points for sublist in player_grid for item in sublist]

    total = sum(indiv_points)

    for i in range(3):
        for j in range(3):
            player_grid[i][j].reset()
            opponent_grid[i][j].reset()
    if individuals:
        return total + bonus_points, indiv_points, bonus_points
    else:
        return total + bonus_points


def print_card_list(card_list):
    if len(card_list) == 0:
        return print("No cards!")
    list_of_lines = []
    for card in card_list:
        if card == 0:
            list_of_lines.append([" "*15 for i in range(10)])
        else:
            list_of_lines.append(str(card).split("\n"))
    if len(card_list) > 5:
        list_of_lines_0 = list_of_lines[0:5]
        list_of_lines_1 = list_of_lines[5:]
        max_height_0 = max([len(card) for card in list_of_lines_0])
        max_height_1 = max([len(card) for card in list_of_lines_1])
        for i in range(len(list_of_lines_0)):
            max_length = max([len(line) for line in list_of_lines_0[i]])
            for j in range(len(list_of_lines_0[i])):
                if len(list_of_lines_0[i][j]) > 0 and list_of_lines_0[i][j][0] in ['⬛', '⬜', '➕']:
                    list_of_lines_0[i][j] = "|" + list_of_lines_0[i][j] + \
                        " "*(max_length - len(list_of_lines_0[i][j])*2) + "|"
                else:
                    list_of_lines_0[i][j] = "|" + list_of_lines_0[i][j] + \
                        " "*(max_length - len(list_of_lines_0[i][j])) + "|"
            list_of_lines_0[i].insert(0, " "+"_"*max_length+" ")
            for x in range(max_height_0+1-len(list_of_lines_0[i])):
                list_of_lines_0[i].append("|"+" "*max_length+"|")
            list_of_lines_0[i].append("|"+"_"*max_length+"|")
        for i in range(len(list_of_lines_1)):
            max_length = max([len(line) for line in list_of_lines_1[i]])
            for j in range(len(list_of_lines_1[i])):
                if len(list_of_lines_1[i][j]) > 0 and list_of_lines_1[i][j][0] in ['⬛', '⬜', '➕']:
                    list_of_lines_1[i][j] = "|" + list_of_lines_1[i][j] + \
                        " "*(max_length - len(list_of_lines_1[i][j])*2) + "|"
                else:
                    list_of_lines_1[i][j] = "|" + list_of_lines_1[i][j] + \
                        " "*(max_length - len(list_of_lines_1[i][j])) + "|"
            list_of_lines_1[i].insert(0, " "+"_"*max_length+" ")
            for x in range(max_height_1+1-len(list_of_lines_1[i])):
                list_of_lines_1[i].append("|"+" "*max_length+"|")
            list_of_lines_1[i].append("|"+"_"*max_length+"|")
        for i in range(len(list_of_lines_0[0])):
            print("".join([card[i] for card in list_of_lines_0]))
        for i in range(len(list_of_lines_1[0])):
            print("".join([card[i] for card in list_of_lines_1]))
    else:
        max_height = max([len(card) for card in list_of_lines])
        for i in range(len(list_of_lines)):
            max_length = max([len(line) for line in list_of_lines[i]])
            for j in range(len(list_of_lines[i])):
                if len(list_of_lines[i][j]) > 0 and list_of_lines[i][j][0] in ['⬛', '⬜', '➕']:
                    list_of_lines[i][j] = "|" + list_of_lines[i][j] + \
                        " "*(max_length - len(list_of_lines[i][j])*2) + "|"
                else:
                    list_of_lines[i][j] = "|" + list_of_lines[i][j] + \
                        " "*(max_length - len(list_of_lines[i][j])) + "|"
            list_of_lines[i].insert(0, " "+"_"*max_length+" ")
            for x in range(max_height+1-len(list_of_lines[i])):
                list_of_lines[i].append("|"+" "*max_length+"|")
            list_of_lines[i].append("|"+"_"*max_length+"|")
        for i in range(len(list_of_lines[0])):
            print("".join([card[i] for card in list_of_lines]))


def execute_instant(setup, player, ai, p_zero_name, p_one_name, p_zero_type, p_one_type, pos_x, pos_y, test=False):
    if player == 0:
        player_grid = setup.p_zero_grid
        opponent_grid = setup.p_one_grid
        player_name = p_zero_name
        opponent_name = p_one_name
        human = p_zero_type == 'Human'
        opp_human = p_one_type == 'Human'
        player_hand = setup.p_zero_hand
        opponent = 1
    else:
        player_grid = setup.p_one_grid
        opponent_grid = setup.p_zero_grid
        player_name = p_one_name
        opponent_name = p_zero_name
        human = p_one_type == 'Human'
        opp_human = p_zero_type == 'Human'
        player_hand = setup.p_one_hand
        opponent = 0
    player_ai = ai[player]
    opp_ai = ai[opponent]
    instant_id = player_grid[pos_x][pos_y].card_id

    if instant_id == 'R2':
        if not test:
            print_card_list(player_grid[0])
            print_card_list(player_grid[1])
            print_card_list(player_grid[2])
            print(f"{player_name}, select a card to discard and replace from the deck")
        if human:
            replacement_x = -1
            replacement_y = -1
            while (not (replacement_x in range(3) and replacement_y in range(3))) or player_grid[replacement_x][replacement_y] == 0:
                print("Input valid coords from 0 to 2")
                replacement_x = int(input())
                replacement_y = int(input())
        else:
            replacement_x, replacement_y = player_ai.instant_decision(setup, instant_id,test=test)
        setup.replace(player, replacement_x, replacement_y)

        player_ai.deck_to_board(player_grid[replacement_x][replacement_y])
        opp_ai.deck_to_board(player_grid[replacement_x][replacement_y])

        if player_grid[replacement_x][replacement_y].instant:
            execute_instant(setup, player, ai, p_zero_name, p_one_name, p_zero_type, p_one_type, replacement_x, replacement_y, test=test)

        if opponent_grid == [[0,0,0],[0,0,0],[0,0,0]]:
            return print(f"{opponent_name} has no cards to replace!")
        
        if not test:
            print_card_list(opponent_grid[0])
            print_card_list(opponent_grid[1])
            print_card_list(opponent_grid[2])
            print(f"{opponent_name}, select a card to discard and replace from the deck")
        if opp_human:
            replacement_x = -1
            replacement_y = -1
            while (not (replacement_x in range(3) and replacement_y in range(3))) or opponent_grid[replacement_x][replacement_y] == 0:
                print("Input valid coords from 0 to 2")
                replacement_x = int(input())
                replacement_y = int(input())
        else:
            replacement_x, replacement_y = opp_ai.instant_decision(setup, instant_id,test=test)
        setup.replace(opponent, replacement_x, replacement_y)

        player_ai.deck_to_board(opponent_grid[replacement_x][replacement_y])
        opp_ai.deck_to_board(opponent_grid[replacement_x][replacement_y])

        if opponent_grid[replacement_x][replacement_y].instant:
            execute_instant(setup, opponent, ai, p_zero_name, p_one_name, p_zero_type, p_one_type, replacement_x, replacement_y, test=test)

    elif instant_id == 'R4':
        if pos_x == 1 or pos_y != 1:
            return
        if not test:
            print_card_list(player_grid[0])
            print_card_list(player_grid[1])
            print_card_list(player_grid[2])
        if human:
            decision = ""
            while decision not in ['y', 'n']:
                print(f"{player_name}, do you want to flip a card y/n")
                decision = input()
            if decision == 'n':
                return
            print(f"{player_name}, select a card to flip")
            flip_x = -1
            flip_y = -1
            while (not (flip_x in range(3) and flip_y in range(3))) or player_grid[flip_x][flip_y] == 0:
                print("Input valid coords from 0 to 2")
                flip_x = int(input())
                flip_y = int(input())
        else:
            decision, flip_x, flip_y = player_ai.instant_decision(setup, instant_id,test=test)
            if decision == 'n':
                return
        setup.flip_card(player, flip_x, flip_y)
    elif instant_id == 'R7':
        if pos_x != 1 or pos_y != 1:
            return
        if not test:
            print_card_list(player_grid[0])
            print_card_list(player_grid[1])
            print_card_list(player_grid[2])
        if human:
            decision = ""
            while decision not in ['y', 'n']:
                print(
                    f"{player_name}, do you want to discard and replace a card y/n")
                decision = input()
            if decision == 'n':
                return
            print(
                f"{player_name}, select a card to discard and replace from the deck")
            replacement_x = -1
            replacement_y = -1
            while (not (replacement_x in range(3) and replacement_y in range(3))) or player_grid[replacement_x][replacement_y] == 0:
                print("Input valid coords from 0 to 2")
                replacement_x = int(input())
                replacement_y = int(input())
        else:
            decision, replacement_x, replacement_y = player_ai.instant_decision(setup, instant_id,test=test)
            if decision == 'n':
                return
        setup.replace(player, replacement_x, replacement_y)

        player_ai.deck_to_board(player_grid[replacement_x][replacement_y])
        opp_ai.deck_to_board(player_grid[replacement_x][replacement_y])

        if player_grid[replacement_x][replacement_y].instant:
            execute_instant(setup, player, ai, p_zero_name, p_one_name, p_zero_type, p_one_type, replacement_x, replacement_y, test=test)

    elif instant_id == 'R8':
        if pos_x != 1 or pos_y == 1:
            return
        if opponent_grid == [[0,0,0],[0,0,0],[0,0,0]]:
            if not test:
                print(f"{opponent_name} has no cards to replace!")
            return 
        if not test:
            print_card_list(opponent_grid[0])
            print_card_list(opponent_grid[1])
            print_card_list(opponent_grid[2])
            print(f"{player_name}, select a card from your opponent's grid to flip")
        if human:
            flip_x = -1
            flip_y = -1
            while (not (flip_x in range(3) and flip_y in range(3))) or player_grid[flip_x][flip_y] == 0:
                print("Input valid coords from 0 to 2")
                flip_x = int(input())
                flip_y = int(input())
        else:
            flip_x, flip_y = player_ai.instant_decision(setup, instant_id,test=test)
        setup.flip_card(opponent, flip_x, flip_y)
        opp_ai.new_plan = True
    elif instant_id == 'R9':
        if not test:
            print("Both players draw a card!")
        setup.draw(player)
        setup.draw(opponent)
    elif instant_id == 'R10':
        for i in range(4):
            setup.deal_temp()
            player_ai.player_see_card(setup.draft_options[-1])
        if not test:
            print(
                f"{player_name}, select a card to draw into your hand (the rest will be discarded)")
        if human:
            print_card_list(setup.draft_options)
            selection_x = -1
            while not selection_x in range(4):
                print("Input valid index from 0 to 3")
                selection_x = int(input())
        else:
            selection_x = player_ai.instant_decision(setup, instant_id,test=test)
        setup.draft_temp(selection_x, player)
        opp_ai.opp_draw_card()
        for i in range(3):
            setup.discard(player, 'draft', 0, 0)
            opp_ai.opp_discard(setup.discard_pile[-1])
    elif instant_id == 'Y1':
        if not test:
            print("All cards of base power (4) or more have been flipped!")
        for i in range(3):
            for j in range(3):
                if player_grid[i][j] != 0 and player_grid[i][j].base_points > 3 and not player_grid[i][j].flipped:
                    setup.flip_card(player, i, j)
                if opponent_grid[i][j] != 0 and opponent_grid[i][j].base_points > 3 and not opponent_grid[i][j].flipped:
                    setup.flip_card(opponent, i, j)
        player_ai.new_plan = True
        opp_ai.new_plan = True
    elif instant_id == 'Y5':
        if not test:
            print(f"{player_name} draws two cards!")
        for i in range(2):
            setup.draw(player)
            opp_ai.opp_draw_card()
    elif instant_id == 'Y8':
        if pos_x != 2 or pos_y != 1:
            return
        if not test:
            print_card_list(player_grid[0])
            print_card_list(player_grid[1])
            print_card_list(player_grid[2])
        for i in range(3):
            for j in range(3):
                if player_grid[i][j] != 0 and player_grid[i][j].flipped:
                    if human:
                        print_card_list([player_grid[i][j]])
                        decision = ""
                        while decision not in ['y', 'n']:
                            print(
                                f"{player_name}, do you want to flip this card so that it is face up y/n")
                            decision = input()
                        if decision == 'y':
                            setup.flip_card(player, i, j)
                    else:
                        if player_ai.instant_decision(setup,instant_id,i,j,test=test) == 'y':
                            setup.flip_card(player, i, j)
    elif instant_id == 'G4':
        if (pos_x, pos_y) not in [(0,2),(2,0)] or len(player_hand) == 0:
            return
        if not test:
            print(f"{player_name}, select a card to discard")
        if human:
            print_card_list(player_hand)
            selection_x = -1
            while not selection_x in range(len(player_hand)):
                print(f"Input valid index from 0 to {len(player_hand)-1}")
                selection_x = int(input())
        else:
            selection_x = player_ai.instant_decision(setup,instant_id,test=test)
        setup.discard(player, 'hand', selection_x, 0)
        opp_ai.opp_discard(setup.discard_pile[-1],True)
        for i in range(3):
            setup.deal_temp()
            player_ai.player_see_card(setup.draft_options[-1])
        if not test:
            print(
                f"{player_name}, select a card to draw into your hand (the rest will be discarded)")
        if human:
            print_card_list(setup.draft_options)
            selection_x = -1
            while not selection_x in range(3):
                print("Input valid index from 0 to 2")
                selection_x = int(input())
        else:
            selection_x = player_ai.instant_decision(setup,instant_id,test=test)
        setup.draft_temp(selection_x, player)
        opp_ai.opp_draw_card()
        for i in range(2):
            setup.discard(player, 'draft', 0, 0)
            opp_ai.opp_discard(setup.discard_pile[-1])
    elif instant_id == 'G7':
        if (pos_x, pos_y) not in [(1,2),(2,0)]:
            return
        if not test:
            print_card_list(player_grid[0])
            print_card_list(player_grid[1])
            print_card_list(player_grid[2])
        if human:
            decision = ""
            while decision not in ['y', 'n']:
                print(
                    f"{player_name}, do you want to move a card to another open position y/n")
                decision = input()
            if decision == 'n':
                return
            print(f"{player_name}, select a card to move")
            move_x = -1
            move_y = -1
            while (not (move_x in range(3) and move_y in range(3))) or player_grid[move_x][move_y] == 0:
                print("Input valid coords from 0 to 2")
                move_x = int(input())
                move_y = int(input())
            print(f"{player_name}, select a destination")
            target_x = -1
            target_y = -1
            while (not (target_x in range(3) and target_y in range(3))) or player_grid[target_x][target_y] != 0:
                print("Input valid coords from 0 to 2")
                target_x = int(input())
                target_y = int(input())
        else:
            decision, move_x, move_y, target_x, target_y = player_ai.instant_decision(setup,instant_id,test=test)
            if decision == 'n':
                return
        setup.move_card(player, move_x, move_y, target_x, target_y)


def execute_pre_scoring(setup, player_ai, name, type, coords = [-1,-1], test = False):
    human = type == "Human"
    if setup.turn == 0:
        player_grid = setup.p_zero_grid
    else:
        player_grid = setup.p_one_grid
    green_count = 0
    for i in range(3):
        for j in range(3):
            if player_grid[i][j] == 0:
                player_grid[i][j] = N0
            if player_grid[i][j].color == "G":
                green_count += 1
    g3_coords = [-1,-1]
    for i in range(3):
        for j in range(3):
            if coords != [-1,-1] and (i!=coords[0] or j!=coords[1]):
                continue
            if player_grid[i][j].flipped:
                continue
            if player_grid[i][j].card_id == 'G3' and green_count > 2 and j < 2 and player_grid[i][j+1].card_id != 'N0':
                g3_coords = [i,j]
            elif player_grid[i][j].card_id == 'G5':
                if not test:
                    print_card_list(player_grid[0])
                    print_card_list(player_grid[1])
                    print_card_list(player_grid[2])
                if human:
                    decision = ""
                    while decision not in ['y', 'n']:
                        print(f"{name}, do you want to flip {player_grid[i][j].name} y/n")
                        decision = input()
                else:
                    decision = player_ai.pre_score_decision(setup,player_grid[i][j].card_id,i,j,test=test)
                if decision == 'y':
                    setup.flip_card(setup.turn, i, j)
            elif player_grid[i][j].card_id == 'G6' and i < 2 and player_grid[i+1][j].card_id != 'N0':
                if i > 0:
                    upper_points = player_grid[i-1][j].base_points
                    player_grid[i-1][j].changepoints(upper_points)
                    player_grid[1-1][j].base_points = player_grid[1][j-1].base_points*2
                if not test:
                    print_card_list(player_grid[0])
                    print_card_list(player_grid[1])
                    print_card_list(player_grid[2])
                if human:
                    decision = ""
                    while decision not in ['y', 'n']:
                        print(
                            f"{name}, do you want to flip {player_grid[i+1][j].name} y/n")
                        decision = input()
                else:
                    decision = player_ai.pre_score_decision(setup,player_grid[i][j].card_id,i,j,test=test)
                if decision == 'y':
                    setup.flip_card(setup.turn, i+1, j)
            elif player_grid[i][j].card_id == 'G11':
                for adj in [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]:
                    if adj[0] >= 0 and adj[0] <= 2 and adj[1] >= 0 and adj[1] <= 2:
                        if player_grid[adj[0]][adj[1]].color in ['B', 'Y'] and not player_grid[adj[0]][adj[1]].flipped and player_grid[adj[0]][adj[1]].card_id != 'N0':
                            setup.flip_card(setup.turn, adj[0], adj[1])
            elif player_grid[i][j].card_id == 'R3' and j>0 and player_grid[i][j-1].card_id != 'N0':
                left_points = player_grid[i][j-1].base_points
                player_grid[i][j-1].changepoints(left_points)
                player_grid[1][j -1].base_points = player_grid[1][j-1].base_points*2
    if g3_coords != [-1,-1]:
        if not test:
            print_card_list(player_grid[0])
            print_card_list(player_grid[1])
            print_card_list(player_grid[2])
        if human:
            decision = ""
            while decision not in ['y', 'n']:
                print(
                    f"{name}, do you want Bear Bear to copy {player_grid[g3_coords[0]][g3_coords[1]+1].name} y/n")
                decision = input()
        else:
            decision = player_ai.pre_score_decision(setup,player_grid[g3_coords[0]][g3_coords[1]].card_id,g3_coords[0],g3_coords[1],test=test)
        if decision == 'y':
            setup.copy_card(setup.turn, g3_coords[0], g3_coords[1])
            if player_grid[g3_coords[0]][g3_coords[1]+1].card_id in ['G5','G6','G11']:
                execute_pre_scoring(setup, player_ai, name, type, g3_coords,test)
    else:
        for i in range(3):
            for j in range(3):
                if player_grid[i][j].card_id == 'N0':
                    player_grid[i][j] = 0

def check_possible_placement(player_grid,player_hand,single=False,hand_index=0):

    if len(player_hand) == 0:
        return False

    if single:
        holes = [item for sublist in player_hand[hand_index].placement_grid for item in sublist]
    else:
        flattened_cards = [[item for sublist in x.placement_grid for item in sublist] for x in player_hand]
        holes = [sum([x[i] for x in flattened_cards]) for i in range(9)]
    flattened_grid = [item for sublist in player_grid for item in sublist]
    possible = False
    for i in range(9):
        if holes[i] != 0 and (flattened_grid[i] == 0 or flattened_grid[i].card_id == 'N0'):
            possible = True
            break
    
    return possible

def check_if_legal(player_grid,player_hand):
    not_allowed = []
    for i in range(9):
        if player_grid[i//3][i%3] != 0:
            not_allowed.append(i)
        elif isinstance(player_grid[i//3][i%3], gameCard) and player_grid[i//3][i%3].card_id != 'N0':
            not_allowed.append(i)
    
    if 'G7' in [card.card_id for card in player_hand] and len(not_allowed) < 8 and (5 not in not_allowed or 6 not in not_allowed):
        for moving_card in player_hand:
            if moving_card.card_id =='G7':
                continue
            elif set(moving_card.placement_indices) - set(not_allowed) != set([]):
                hand_copy = list(player_hand).copy()
                hand_copy.remove(moving_card)
                problem = constraint.Problem(constraint.RecursiveBacktrackingSolver())
                for card in player_hand:
                    if card.card_id == 'G7':
                        problem.addVariable(card.card_id,[5,6])
                    else:
                        problem.addVariable(card.card_id,card.placement_indices)
                problem.addConstraint(constraint.AllDifferentConstraint(),[card.card_id for card in hand_copy])
                problem.addConstraint(constraint.AllDifferentConstraint(),['G7',moving_card.card_id])
                problem.addConstraint(constraint.NotInSetConstraint(not_allowed))
                solution = problem.getSolution()
                if solution:
                    return True
    
    problem = constraint.Problem(constraint.RecursiveBacktrackingSolver())
    for card in player_hand:
        problem.addVariable(card.card_id,card.placement_indices)
    problem.addConstraint(constraint.AllDifferentConstraint())
    problem.addConstraint(constraint.NotInSetConstraint(not_allowed))
    solution = problem.getSolution()
    if solution:
        return True
    else:
        return False