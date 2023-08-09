from utilities import *
from input_utilities import *


def execute_instant(setup, player, ai, p_zero_name, p_one_name, p_zero_type, p_one_type, pos_x, pos_y, test=False , display = False, screen = 0, game_width = 0, game_height = 0):
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
            if display:
                replacement_x, replacement_y = input_waiter_draw_discard(screen,setup,game_width,game_height,instant_id)
            else:
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
            execute_instant(setup, player, ai, p_zero_name, p_one_name, p_zero_type, p_one_type, replacement_x, replacement_y, test=test, display = display, screen = screen, game_width = game_width, game_height = game_height)

        if opponent_grid == [[0,0,0],[0,0,0],[0,0,0]]:
            return print(f"{opponent_name} has no cards to replace!")
        
        if not test:
            print_card_list(opponent_grid[0])
            print_card_list(opponent_grid[1])
            print_card_list(opponent_grid[2])
            print(f"{opponent_name}, select a card to discard and replace from the deck")
        if opp_human:
            if display:
                replacement_x, replacement_y = input_waiter_draw_discard(screen,setup,game_width,game_height,instant_id)
            else:
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
            execute_instant(setup, opponent, ai, p_zero_name, p_one_name, p_zero_type, p_one_type, replacement_x, replacement_y, test=test, display = display, screen = screen, game_width = game_width, game_height = game_height)

    elif instant_id == 'R4':
        if pos_x == 1 or pos_y != 1:
            return
        if not test:
            print_card_list(player_grid[0])
            print_card_list(player_grid[1])
            print_card_list(player_grid[2])
        if human:
            if display:
                decision = input_waiter_yesno(screen,setup,game_width,game_height,instant_id)
            else:
                decision = ""
                while decision not in ['y', 'n']:
                    print(f"{player_name}, do you want to flip a card y/n")
                    decision = input()
            if decision == 'n':
                return
            if display:
                flip_x,flip_y = input_waiter_flip(screen,setup,game_width,game_height,instant_id)
            else:
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
            if display:
                decision = input_waiter_yesno(screen,setup,game_width,game_height,instant_id)
            else:
                decision = ""
                while decision not in ['y', 'n']:
                    print(
                        f"{player_name}, do you want to discard and replace a card y/n")
                    decision = input()
            if decision == 'n':
                return
            if display:
                replacement_x, replacement_y = input_waiter_draw_discard(screen,setup,game_width,game_height,instant_id)
            else:
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
            if display:
                flip_x,flip_y = input_waiter_flip(screen,setup,game_width,game_height,instant_id)
            else:
                flip_x = -1
                flip_y = -1
                while (not (flip_x in range(3) and flip_y in range(3))) or opponent_grid[flip_x][flip_y] == 0:
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
        player_ai.new_plan = True
        opp_ai.new_plan = True
    elif instant_id == 'R10':
        for i in range(4):
            setup.deal_temp()
            player_ai.player_see_card(setup.draft_options[-1])
        if not test:
            print(
                f"{player_name}, select a card to draw into your hand (the rest will be discarded)")
        if human:
            if display:
                selection_x, _ = input_waiter_draw_discard(screen,setup,game_width,game_height,instant_id)
            else:
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
                        if display:
                            decision = input_waiter_yesno(screen,setup,game_width,game_height,instant_id,i,j)
                        else:
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
            if display:
                selection_x, _ = input_waiter_draw_discard(screen,setup,game_width,game_height,instant_id)
            else:
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
            if display:
                selection_x, _ = input_waiter_draw_discard(screen,setup,game_width,game_height,instant_id)
            else:
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
            if display:
                decision = input_waiter_yesno(screen,setup,game_width,game_height,instant_id)
            else:
                decision = ""
                while decision not in ['y', 'n']:
                    print(
                        f"{player_name}, do you want to move a card to another open position y/n")
                    decision = input()
            if decision == 'n':
                return
            if display:
                move_x,move_y,target_x,target_y = input_waiter_g7(screen,setup,game_width,game_height)
            else:
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


def execute_pre_scoring(setup, player_ai, name, type, coords = [-1,-1], test = False, display = False, screen = 0, game_width = 0, game_height = 0):
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
                    if display:
                        decision = input_waiter_yesno(screen,setup,game_width,game_height,'G5',i,j)
                    else:
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
                    if display:
                        decision = input_waiter_yesno(screen,setup,game_width,game_height,'G6',i+1,j)
                    else:
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
            if display:
                decision = input_waiter_yesno(screen,setup,game_width,game_height,'G3',g3_coords[0],g3_coords[1]+1)
            else:
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
                execute_pre_scoring(setup, player_ai, name, type, g3_coords,test,display,screen,game_width,game_height)
    else:
        for i in range(3):
            for j in range(3):
                if player_grid[i][j].card_id == 'N0':
                    player_grid[i][j] = 0