from main import usurperGame
import pandas as pd
import numpy as np
import itertools
import random

competitors = {
    "Aiden": ['full', 'points'],
    "Andrew": ['full', 'points_reverse'],
    "Keiran": ['full', 'single_card_averages'],
    "Spencer": ['full', 'pair_averages'],
    "Doni": ['full', 'opp_pair_averages'],
    "Lilly": ['full', 'overall_pair_averages'],
    "Lisa": ['full', 'overall_pair_averages_reverse'],
    "Corwin": ['full', 'wifes_boyfriend'],
    "Rando": ['random', 'random'],
    "Phineas": ['full', 'random'],
    "Mumu": ['random', 'overall_pair_averages']
}

bonus_id_list = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10']
card_id_list = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11',
                'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Y10', 'Y11',
                'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11',
                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11']
starters = [0]*45+[1]*45

competitor_data = pd.DataFrame(columns=['wins', 'ties', 'losses', 'first', 'second']+list(competitors.keys())+bonus_id_list+card_id_list,
                               index=list(competitors.keys()),
                               data=np.zeros((11, 70)))

game_data = pd.DataFrame(columns=['p1', 'p2', 'winner', 'loser', 'first', 'second', 'p1score', 'p2score',
                         'p1bonus', 'p2bonus']+['p1_draft_'+str(i) for i in range(1, 10)]+['p2_draft_'+str(i) for i in range(1, 10)])

for comp_combo in itertools.combinations(list(competitors.keys()), 2):
    random.shuffle(starters)
    s_index = 0
    for combo in itertools.combinations(bonus_id_list, 2):
        comp_combo_list = list(comp_combo)
        combo_list = list(combo)
        for x in range(2):
            if x == 0:
                bonuses = combo_list
            else:
                bonuses = [combo_list[1], combo_list[0]]
            game = usurperGame(comp_combo_list[0], comp_combo_list[1], 'AI', 'AI',
                               competitors[comp_combo_list[0]
                                           ][0], competitors[comp_combo_list[1]][0],
                               competitors[comp_combo_list[0]
                                           ][1], competitors[comp_combo_list[1]][1],
                               bonuses[0], bonuses[1],
                               prebake_starter=starters[s_index])

            p_zero_score, p_one_score, p_zero_draft, p_one_draft, p_zero_indivs, p_one_indivs, p_zero_grid, p_one_grid, p_zero_bonus_score, p_one_bonus_score = game.mainLoop()

            if p_zero_score > p_one_score:
                winner = comp_combo_list[0]
                winning_bonus = bonuses[0]
                loser = comp_combo_list[1]
            elif p_zero_score < p_one_score:
                winner = comp_combo_list[1]
                winning_bonus = bonuses[1]
                loser = comp_combo_list[0]
            else:
                winner = "tie"
            game_data.loc[len(game_data)] = [comp_combo_list[0], comp_combo_list[1], winner, loser, comp_combo_list[starters[s_index]],
                                             comp_combo_list[abs(starters[s_index]-1)], p_zero_score, p_one_score]+bonuses+p_zero_draft+p_one_draft

            for card in p_zero_draft:
                competitor_data[card][comp_combo_list[0]] += 1
            for card in p_one_draft:
                competitor_data[card][comp_combo_list[1]] += 1

            if winner == "tie":
                competitor_data['ties'][comp_combo_list[0]] += 1
                competitor_data['ties'][comp_combo_list[1]] += 1
            else:
                competitor_data['wins'][winner] += 1
                competitor_data['losses'][loser] += 1
                competitor_data[winning_bonus][winner] += 1
                competitor_data[loser][winner] += 1

                if comp_combo_list[starters[s_index]] == winner:
                    competitor_data['first'][winner] += 1
                else:
                    competitor_data['second'][winner] += 1

            print('ROUND:')
            print(comp_combo_list)
            print(s_index)
            s_index += 1
    game_data.to_csv('game_data'+comp_combo[0]+comp_combo[1]+'.csv')
    competitor_data.to_csv('competitor_data'+comp_combo[0]+comp_combo[1]+'.csv')

game_data.to_csv('game_data.csv')
competitor_data.to_csv('competitor_data.csv')
