from main import usurperGame
import pandas as pd
import numpy as np
import itertools

x = 100


bonus_id_list = ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10']

card_id_list = ['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11',
                'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'Y9', 'Y10', 'Y11',
                'G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9', 'G10', 'G11',
                'B1', 'B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B9', 'B10', 'B11']

#cross_reference_1 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_1 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_2 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_2 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_3 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_3 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_4 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_4 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_5 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_5 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_6 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_6 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_7 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_7 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_8 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_8 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_9 = pd.DataFrame(columns=card_id_list,
#                                 index=card_id_list,
#                                 data=np.zeros((44, 44)))
#cross_reference_instances_9 = pd.DataFrame(columns=card_id_list,
#                                           index=card_id_list,
#                                           data=np.zeros((44, 44)))

#cross_reference_10 = pd.DataFrame(columns=card_id_list,
#                                  index=card_id_list,
#                                  data=np.zeros((44, 44)))
#cross_reference_instances_10 = pd.DataFrame(columns=card_id_list,
#                                            index=card_id_list,
#                                            data=np.zeros((44, 44)))

#CR_list = [cross_reference_1,
#           cross_reference_2,
#           cross_reference_3,
#           cross_reference_4,
#           cross_reference_5,
#           cross_reference_6,
#           cross_reference_7,
#           cross_reference_8,
#           cross_reference_9,
#           cross_reference_10]

#CRI_list = [cross_reference_instances_1,
#            cross_reference_instances_2,
#            cross_reference_instances_3,
#            cross_reference_instances_4,
#            cross_reference_instances_5,
#            cross_reference_instances_6,
#            cross_reference_instances_7,
#            cross_reference_instances_8,
#            cross_reference_instances_9,
#            cross_reference_instances_10]

#cross_reference_opp_1 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_1 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_2 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_2 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                              data=np.zeros((44, 44)))

#cross_reference_opp_3 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_3 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_4 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_4 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_5 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_5 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_6 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_6 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_7 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_7 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_8 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_8 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_9 = pd.DataFrame(columns=card_id_list,
#                                     index=card_id_list,
#                                     data=np.zeros((44, 44)))
#cross_reference_instances_opp_9 = pd.DataFrame(columns=card_id_list,
#                                               index=card_id_list,
#                                               data=np.zeros((44, 44)))

#cross_reference_opp_10 = pd.DataFrame(columns=card_id_list,
#                                      index=card_id_list,
#                                      data=np.zeros((44, 44)))
#cross_reference_instances_opp_10 = pd.DataFrame(columns=card_id_list,
#                                                index=card_id_list,
#                                                data=np.zeros((44, 44)))

#CR_list_opp = [cross_reference_opp_1,
#               cross_reference_opp_2,
#               cross_reference_opp_3,
#               cross_reference_opp_4,
#               cross_reference_opp_5,
#               cross_reference_opp_6,
#               cross_reference_opp_7,
#               cross_reference_opp_8,
#               cross_reference_opp_9,
#               cross_reference_opp_10]

#CRI_list_opp = [cross_reference_instances_opp_1,
#                cross_reference_instances_opp_2,
#                cross_reference_instances_opp_3,
#                cross_reference_instances_opp_4,
#                cross_reference_instances_opp_5,
#                cross_reference_instances_opp_6,
#                cross_reference_instances_opp_7,
#                cross_reference_instances_opp_8,
#                cross_reference_instances_opp_9,
#                cross_reference_instances_opp_10]

#for i in range(10):
#    CR_list[i].to_csv('./cross_references/cross_references_X'+str(i+1)+'.csv')
#    CRI_list[i].to_csv('./cross_references_instances/cross_references_X'+str(i+1)+'_instances.csv')
#    CR_list_opp[i].to_csv('./cross_references_opp/cross_references_X'+str(i+1)+'_opp.csv')
#    CRI_list_opp[i].to_csv('./cross_references_instances_opp/cross_references_X'+str(i+1)+'_instances_opp.csv')


for i in range(x):

    CR_list = []
    CRI_list = []
    CR_list_opp = []
    CRI_list_opp = []

    for l in range(10):
        CR_list.append(pd.read_csv('./cross_references/cross_references_X'+str(l+1)+'.csv').set_index('Unnamed: 0'))
        CRI_list.append(pd.read_csv('./cross_references_instances/cross_references_X'+str(l+1)+'_instances.csv').set_index('Unnamed: 0'))
        CR_list_opp.append(pd.read_csv('./cross_references_opp/cross_references_X'+str(l+1)+'_opp.csv').set_index('Unnamed: 0'))
        CRI_list_opp.append(pd.read_csv('./cross_references_instances_opp/cross_references_X'+str(l+1)+'_instances_opp.csv').set_index('Unnamed: 0'))
    print('STARTING ROUND '+str(i))
    for combo in itertools.combinations(bonus_id_list, 2):
        
        combo_list = list(combo)
        print('STARTING GAME IN ROUND '+str(i))
        game = usurperGame("UsurperBot1", "UsurperBot2", 'AI','AI', 'full', 'full', combo_list[0], combo_list[1])
        p_zero_score, p_one_score, p_zero_draft, p_one_draft = game.mainLoop()
        print('ENDING GAME IN ROUND '+str(i))

        for j in range(9):
            CR_list[bonus_id_list.index(
                combo_list[0])][p_zero_draft[j]][p_zero_draft[j]] += p_zero_score-p_one_score
            CRI_list[bonus_id_list.index(
                combo_list[0])][p_zero_draft[j]][p_zero_draft[j]] += 1

            CR_list[bonus_id_list.index(
                combo_list[1])][p_one_draft[j]][p_one_draft[j]] += p_one_score-p_zero_score
            CRI_list[bonus_id_list.index(
                combo_list[1])][p_one_draft[j]][p_one_draft[j]] += 1

            for k in range(9):
                if k >= j+1:
                    CR_list[bonus_id_list.index(
                        combo_list[0])][p_zero_draft[j]][p_zero_draft[k]] += p_zero_score-p_one_score
                    CR_list[bonus_id_list.index(
                        combo_list[0])][p_zero_draft[k]][p_zero_draft[j]] += p_zero_score-p_one_score
                    CRI_list[bonus_id_list.index(
                        combo_list[0])][p_zero_draft[j]][p_zero_draft[k]] += 1
                    CRI_list[bonus_id_list.index(
                        combo_list[0])][p_zero_draft[k]][p_zero_draft[j]] += 1

                    CR_list[bonus_id_list.index(
                        combo_list[1])][p_one_draft[j]][p_one_draft[k]] += p_one_score-p_zero_score
                    CR_list[bonus_id_list.index(
                        combo_list[1])][p_one_draft[k]][p_one_draft[j]] += p_one_score-p_zero_score
                    CRI_list[bonus_id_list.index(
                        combo_list[1])][p_one_draft[j]][p_one_draft[k]] += 1
                    CRI_list[bonus_id_list.index(
                        combo_list[1])][p_one_draft[k]][p_one_draft[j]] += 1

                CR_list_opp[bonus_id_list.index(
                    combo_list[0])][p_zero_draft[j]][p_one_draft[k]] += p_zero_score-p_one_score
                CRI_list_opp[bonus_id_list.index(
                    combo_list[0])][p_zero_draft[j]][p_one_draft[k]] += 1

                CR_list_opp[bonus_id_list.index(
                    combo_list[1])][p_one_draft[j]][p_zero_draft[k]] += p_one_score-p_zero_score
                CRI_list_opp[bonus_id_list.index(
                    combo_list[1])][p_one_draft[j]][p_zero_draft[k]] += 1
        
        print(dir())


    for m in range(10):
        CR_list[m].to_csv('./cross_references/cross_references_X'+str(m+1)+'.csv')
        CRI_list[m].to_csv('./cross_references_instances/cross_references_X'+str(m+1)+'_instances.csv')
        CR_list_opp[m].to_csv('./cross_references_opp/cross_references_X'+str(m+1)+'_opp.csv')
        CRI_list_opp[m].to_csv('./cross_references_instances_opp/cross_references_X'+str(m+1)+'_instances_opp.csv')

        CR_avg = CR_list[m].div(CRI_list[m])
        CR_avg_opp = CR_list_opp[m].div(CRI_list_opp[m])
        CR_avg.to_csv('./cross_references_averages/cross_references_X'+str(m+1)+'_avg.csv')
        CR_avg_opp.to_csv('./cross_references_averages_opp/cross_references_X'+str(m+1)+'_avg_opp.csv')