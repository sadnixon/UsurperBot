from gameBonus import gameBonus
from gameBonusDeck import gameBonusDeck
from gameCard import gameCard
from gameDeck import gameDeck
from gameSetup import gameSetup
import constraint

#pair_list = []
#for i in range(2):
#    for j in range(3):
#        pair_list.append(((i, j), (i+1, j)))
#for i in range(3):
#    for j in range(2):
#        pair_list.append(((i, j), (i, j+1)))

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
                    flat_grid = [item.color == 'R' for sublist in player_grid for item in sublist]
                    flat_grid_2 = [item.color == 'G' for sublist in player_grid for item in sublist]
                    gr_pairs_sum = min(sum(flat_grid),sum(flat_grid_2))
                    current_card.changepoints(gr_pairs_sum)
                    #for pair in pair_list:
                    #    if set([player_grid[pair[0][0]][pair[0][1]].color, player_grid[pair[1][0]][pair[1][1]].color]) == {'R', 'G'}:
                    #        current_card.changepoints(3)
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
                    if i < 2 and player_grid[i+1][j].card_id == 'G6':
                        current_card.changepoints(current_card.base_points)
                        current_card.base_points = current_card.base_points * 2
                    if j < 2 and player_grid[i][j+1].card_id == 'R3':
                        current_card.changepoints(current_card.base_points)
                        current_card.base_points = current_card.base_points * 2
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
            flat_grid = [item.color == 'B' for sublist in player_grid for item in sublist]
            flat_grid_2 = [item.color == 'Y' for sublist in player_grid for item in sublist]
            by_pairs_sum = min(sum(flat_grid),sum(flat_grid_2))
            bonus_points += by_pairs_sum*4
            #for pair in pair_list:
            #    if set([player_grid[pair[0][0]][pair[0][1]].color, player_grid[pair[1][0]][pair[1][1]].color]) == {'B', 'Y'}:
            #        bonus_points += 4

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
    if len(card_list) > 6:
        list_of_lines_0 = list_of_lines[0:6]
        list_of_lines_1 = list_of_lines[6:]
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

def check_if_legal(player_grid,player_hand,activation_req=False):
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
    activation_pairs = []
    for card in player_hand:
        problem.addVariable(card.card_id,card.placement_indices)
        if activation_req and card.activation:
            problem.addVariable(card.card_id+"_2",card.activation_indices)
            activation_pairs.extend([card.card_id,card.card_id+"_2"])
    problem.addConstraint(constraint.AllDifferentConstraint(),[card.card_id for card in player_hand])
    if activation_req:
        def at_least_one(*var_list):
            return sum([var_list[i]==var_list[i+1] for i in range(len(var_list)//2)])>0
        problem.addConstraint(at_least_one,activation_pairs)
    problem.addConstraint(constraint.NotInSetConstraint(not_allowed))
    solution = problem.getSolution()
    if solution:
        return True
    else:
        return False
    
def combo_narrower(player_grid,player_hand):
    special_cards = ['R3','G6','G10','R6','Y4','B6','G2','Y7','B3','Y6','B11','G8','G11']
    distincts = {}
    def grid_string(grid):
        return ''.join([str(item) for sublist in grid for item in sublist])
    
    existing_ids = []
    for i in range(len(player_hand)):
        adjusted_string = grid_string(player_hand[i].placement_grid)
        for j in range(9):
            if player_grid[j//3][j%3] != 0:
                adjusted_string = adjusted_string[:j]+"0"+adjusted_string[j+1:]
                if i==0:
                    existing_ids.append(player_grid[j//3][j%3].card_id)
        if player_hand[i].card_id in special_cards:
            distincts[player_hand[i].card_id] = [player_hand[i]]
        else:
            if adjusted_string not in distincts:
                distincts[grid_string(adjusted_string)] = [player_hand[i]]
            else:
                distincts[grid_string(adjusted_string)] = distincts[adjusted_string] + [player_hand[i]]
    
    hand_ids = [card.card_id for card in player_hand]
    all_ids = existing_ids + hand_ids
    if 'G3' in all_ids or len(distincts.keys()) == len(player_hand):
        return False, False
    
    if 'R3' in all_ids or 'G6' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            for item in group:
                if key+'_'+str(item.og_base_points) not in distincts:
                    distincts[key+'_'+str(item.og_base_points)] = [item]
                else:
                    distincts[key+'_'+str(item.og_base_points)] = distincts[key+'_'+str(item.og_base_points)] + [item]

    if 'G10' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            distincts[key+'_R']  = list(filter(lambda x: x.color=='R', group))
            distincts[key+'_G']  = list(filter(lambda x: x.color=='G', group))
            distincts[key+'_nRG']  = list(filter(lambda x: x.color not in ['G','R'], group))
    elif 'R6' in all_ids or 'Y4' in all_ids or 'B6' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            distincts[key+'_R']  = list(filter(lambda x: x.color=='R', group))
            distincts[key+'_nR']  = list(filter(lambda x: x.color != 'R', group))
    elif 'G2' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            distincts[key+'_RG']  = list(filter(lambda x: x.color in ['G','R'], group))
            distincts[key+'_nRG']  = list(filter(lambda x: x.color not in ['G','R'], group))

    if 'Y7' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            distincts[key+'_Y']  = list(filter(lambda x: x.color=='Y', group))
            distincts[key+'_nY']  = list(filter(lambda x: x.color != 'Y', group))
    if 'B3' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            distincts[key+'_B']  = list(filter(lambda x: x.color=='B', group))
            distincts[key+'_nB']  = list(filter(lambda x: x.color != 'B', group))
    elif 'Y6' in all_ids and 'Y7' not in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            distincts[key+'_BY']  = list(filter(lambda x: x.color in ['B','Y'], group))
            distincts[key+'_nBY']  = list(filter(lambda x: x.color not in ['B','Y'], group))
            
    if 'B11' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            for item in group:
                if key+'_'+str(item.hands) not in distincts:
                    distincts[key+'_'+str(item.hands)] = [item]
                else:
                    distincts[key+'_'+str(item.hands)] = distincts[key+'_'+str(item.hands)] + [item]

    if 'G8' in all_ids:
        for key in list(filter(lambda x: x not in special_cards,distincts.keys())):
            group = distincts.pop(key)
            for item in group:
                if key+'_'+str(item.eyes) not in distincts:
                    distincts[key+'_'+str(item.eyes)] = [item]
                else:
                    distincts[key+'_'+str(item.eyes)] = distincts[key+'_'+str(item.eyes)] + [item]
    
    key_correspondance = []
    for key in list(distincts.keys()):
        if distincts[key] == []:
            distincts.pop(key)
        else:
            for item in distincts[key]:
                key_correspondance.append(key)
    if len(distincts.keys()) == len(player_hand):
        return False, False
    else:
        return distincts, key_correspondance