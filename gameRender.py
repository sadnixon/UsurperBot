import pygame
from pygame.locals import *
from gameCard import gameCard

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def renderGame(window,game_width,game_height,setup):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 1/10)
    card_y = round(max_surface_y * 1/4)

    pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x,card_y*3,card_x*9,card_y),10)
    placement_rect = pygame.Rect(card_x,card_y*3,card_x*9,card_y)

    img_list = []
    rect_list = []
    topleft_list = []
    for i in range(len(setup.draft_options)):
        draft_options_image = setup.card_image_dict[setup.draft_options[i].color][int(setup.draft_options[i].card_id[1:])-1]
        draft_options_image.convert()
        rect = draft_options_image.get_rect()
        rect.topleft = ((card_x*2) + card_x*i, (round(card_y*1.5)))
        window.blit(draft_options_image,rect)
        img_list.append(draft_options_image)
        rect_list.append(rect)
        topleft_list.append(((card_x*2) + card_x*i, (round(card_y*1.5))))
    
    for i in range(len(setup.p_zero_hand)):
        p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
        window.blit(p_zero_hand_image, (card_x + card_x*i,(card_y*3)))
    
    for i in range(len(setup.p_one_hand)):
        #p_one_hand_image = card_image_dict[setup.p_one_hand[i].color][int(setup.p_one_hand[i].card_id[1])-1]
        if i == len(setup.p_one_hand)-1:
            p_one_hand_image = setup.card_image_dict[setup.p_one_hand[i].color][int(setup.p_one_hand[i].card_id[1:])-1]
            window.blit(p_one_hand_image, (card_x + card_x*i,0))
        else:
            window.blit(setup.card_back, (card_x + card_x*i,0))

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,(0,(card_y*3)))

    window.blit(setup.bonus_back,(0,0))

    return img_list,rect_list,topleft_list, placement_rect

def renderGame_update(window,game_width,game_height,setup,img_list,rect_list,topleft_list,moving_index):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 1/10)
    card_y = round(max_surface_y * 1/4)

    pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x,card_y*3,card_x*9,card_y),10)
    placement_rect = pygame.Rect(card_x,card_y*3,card_x*9,card_y)

    for i in range(len(img_list)):
        if i!=moving_index:
            draft_options_image = img_list[i]
            #window.blit(p_zero_hand_image, (1135 + card_x*(i%2), 0 + card_y*(i//2)))
            rect = rect_list[i]
            window.blit(draft_options_image,rect)
    
    for i in range(len(setup.p_zero_hand)):
        p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
        window.blit(p_zero_hand_image, (card_x + card_x*i,(card_y*3)))
    
    for i in range(len(setup.p_one_hand)):
        #p_one_hand_image = card_image_dict[setup.p_one_hand[i].color][int(setup.p_one_hand[i].card_id[1])-1]
        if i == len(setup.p_one_hand)-1:
            p_one_hand_image = setup.card_image_dict[setup.p_one_hand[i].color][int(setup.p_one_hand[i].card_id[1:])-1]
            window.blit(p_one_hand_image, (card_x + card_x*i,0))
        else:
            window.blit(setup.card_back, (card_x + card_x*i,0))

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,(0,(card_y*3)))

    window.blit(setup.bonus_back,(0,0))

    if moving_index != -1:
        moving_card_image = img_list[moving_index]
        rect = rect_list[moving_index]
        window.blit(moving_card_image,rect)

    return img_list,rect_list,topleft_list, placement_rect

def renderGameNext2(window,game_width,game_height,setup):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)
    notch_y = round(max_surface_y * 1/17)

    placement_rect_list = []
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y),10)
            placement_rect = pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),placement_rect,10)
            placement_rect_list.append(placement_rect)

    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    window.blit(setup.card_back, (card_x + card_x*j, 0 + card_y*i))
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    window.blit(p_one_image, (card_x + card_x*j, 0 + card_y*i))
            if setup.p_zero_grid[i][j] != 0 and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_zero_grid[i][j].flipped:
                    window.blit(setup.card_back, ((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
                else:
                    p_zero_image = setup.card_image_dict[setup.p_zero_grid[i][j].color][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                    window.blit(p_zero_image, ((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
    
    img_list = []
    rect_list = []
    topleft_list = []
    for i in range(len(setup.p_zero_hand)):
        p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
        p_zero_hand_image.convert()
        rect = p_zero_hand_image.get_rect()
        if i>8:
            rect.topleft = ((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3))
            topleft_list.append(((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3)))
        else:
            rect.topleft = ((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3))
            topleft_list.append(((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3)))
        window.blit(p_zero_hand_image,rect)
        img_list.append(p_zero_hand_image)
        rect_list.append(rect)

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,((round(card_x*8.5)),(card_y*3)))

    window.blit(setup.card_back,(0,0))
    window.blit(setup.bonus_back,(0,card_y))

    window.blit(setup.card_back,(0,(notch_y+card_y*3)))
    discard_pile_image = setup.card_image_dict[setup.discard_pile[-1].color][int(setup.discard_pile[-1].card_id[1:])-1]
    window.blit(discard_pile_image,(card_x,(notch_y+card_y*3)))

    return img_list,rect_list,topleft_list,placement_rect_list


def renderGameNext2_update(window,game_width,game_height,setup,img_list,rect_list,topleft_list,moving_index):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)
    notch_y = round(max_surface_y * 1/17)
    
    for i in range(3):
        for j in range(3):
            pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y),10)
            placement_rect = pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),placement_rect,10)

    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0'] and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    window.blit(setup.card_back, (card_x + card_x*j, 0 + card_y*i))
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    window.blit(p_one_image, (card_x + card_x*j, 0 + card_y*i))
            if setup.p_zero_grid[i][j] != 0 and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0'] and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_zero_grid[i][j].flipped:
                    window.blit(setup.card_back, ((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
                else:
                    p_zero_image = setup.card_image_dict[setup.p_zero_grid[i][j].color][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                    window.blit(p_zero_image, ((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
    
    for i in range(len(img_list)):
        if i!=moving_index:
            p_zero_hand_image = img_list[i]
            #window.blit(p_zero_hand_image, (1135 + card_x*(i%2), 0 + card_y*(i//2)))
            rect = rect_list[i]
            window.blit(p_zero_hand_image,rect)

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,((round(card_x*8.5)),(card_y*3)))

    window.blit(setup.card_back,(0,0))
    window.blit(setup.bonus_back,(0,card_y))

    window.blit(setup.card_back,(0,(notch_y+card_y*3)))
    discard_pile_image = setup.card_image_dict[setup.discard_pile[-1].color][int(setup.discard_pile[-1].card_id[1:])-1]
    window.blit(discard_pile_image,(card_x,(notch_y+card_y*3)))

    if moving_index != -1:
        moving_card_image = img_list[moving_index]
        rect = rect_list[moving_index]
        window.blit(moving_card_image,rect)

    return img_list,rect_list,topleft_list

def renderYesNo(window,game_width,game_height,instant_id,highlight_x=-1,highlight_y=-1,mouse_over='n/a'):

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)

    font = pygame.font.Font(None,100)
    font_small = pygame.font.Font(None,30)
    yes_text = font.render("YES",True,(89,141,81))
    no_text = font.render("NO",True,(198,56,72))
    yes_text_rect = yes_text.get_rect(center = (round(card_x*4.5),round(card_y*3.5)) )
    no_text_rect = no_text.get_rect(center = (round(card_x*4.5),round(card_y*4)) )

    if instant_id == 'R4':
        question = "Would you like to flip a card on your grid?"
    elif instant_id == 'R7':
        question = "Would you like to discard and replace a card?"
    elif instant_id in ['Y8','G5','G6']:
        question = "Would you like to flip the highlighted card?"
    elif instant_id == 'G3':
        question = "Would you like to copy the highlighted card?"
    elif instant_id == 'G7':
        question = "Would you like to move a card on your grid?"
    question_surface = pygame.Surface((card_x-20,card_y))
    question_surface.fill((25, 25, 25))
    blit_text(question_surface,question,(20,20),font_small,(255,255,255))
    window.blit(question_surface,(card_x*3,round(card_y*3.25)))
    

    yes_rect = pygame.Rect(card_x*4,round(card_y*3.25),card_x,round(card_y*0.5))
    no_rect = pygame.Rect(card_x*4,round(card_y*3.75),card_x,round(card_y*0.5))

    if mouse_over == 'y':
        pygame.draw.rect(window,(150,150,150),yes_rect,0)
    else:
        pygame.draw.rect(window,(50,50,50),yes_rect,0)
    pygame.draw.rect(window,(89,141,81),yes_rect,10)
    window.blit(yes_text,yes_text_rect)

    if mouse_over == 'n':
        pygame.draw.rect(window,(150,150,150),no_rect,0)
    else:
        pygame.draw.rect(window,(50,50,50),no_rect,0)
    pygame.draw.rect(window,(198,56,72),no_rect,10)
    window.blit(no_text,no_text_rect)

    if highlight_x!=-1 and highlight_y!=-1:
        #yes X and Y are mixed up for the card thingies. rip me
        card_highlight_rect = pygame.Rect((round(card_x*7.5))+card_x*highlight_y,0+card_y*highlight_x,card_x,card_y)
        pygame.draw.rect(window,(150,150,150),card_highlight_rect,10)

    return yes_rect,no_rect

def renderGameG7(window,game_width,game_height,setup):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)
    notch_y = round(max_surface_y * 1/17)

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y),10)
            placement_rect = pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),placement_rect,10)

    img_list = []
    rect_list = []
    topleft_list = []
    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    window.blit(setup.card_back, (card_x + card_x*j, 0 + card_y*i))
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    window.blit(p_one_image, (card_x + card_x*j, 0 + card_y*i))
            if setup.p_zero_grid[i][j] != 0 and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_zero_grid[i][j].flipped:
                    p_zero_image = setup.card_back
                else:
                    p_zero_image = setup.card_image_dict[setup.p_zero_grid[i][j].color][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                p_zero_image.convert()
                rect = p_zero_image.get_rect()
                rect.topleft = ((round(card_x*7.5)) + card_x*j, 0 + card_y*i)
                window.blit(p_zero_image,rect)
                img_list.append(p_zero_image)
                rect_list.append(rect)
                topleft_list.append(((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
            else:
                img_list.append(0)
                rect_list.append(pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y))
                topleft_list.append(((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
    
    for i in range(len(setup.p_zero_hand)):
        p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
        p_zero_hand_image.convert()
        rect = p_zero_hand_image.get_rect()
        if i>8:
            rect.topleft = ((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3))
        else:
            rect.topleft = ((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3))
        window.blit(p_zero_hand_image,rect)

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,((round(card_x*8.5)),(card_y*3)))

    window.blit(setup.card_back,(0,0))
    window.blit(setup.bonus_back,(0,card_y))

    window.blit(setup.card_back,(0,(notch_y+card_y*3)))
    discard_pile_image = setup.card_image_dict[setup.discard_pile[-1].color][int(setup.discard_pile[-1].card_id[1:])-1]
    window.blit(discard_pile_image,(card_x,(notch_y+card_y*3)))

    return img_list,rect_list,topleft_list


def renderGameG7_update(window,game_width,game_height,setup,img_list,rect_list,topleft_list,moving_index):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)
    notch_y = round(max_surface_y * 1/17)

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y),10)
            placement_rect = pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),placement_rect,10)

    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    window.blit(setup.card_back, (card_x + card_x*j, 0 + card_y*i))
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    window.blit(p_one_image, (card_x + card_x*j, 0 + card_y*i))
    
    for i in range(len(img_list)):
        if i!=moving_index and img_list[i]!=0:
            p_zero_image = img_list[i]
            rect = rect_list[i]
            window.blit(p_zero_image,rect)
    
    for i in range(len(setup.p_zero_hand)):
        p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
        p_zero_hand_image.convert()
        rect = p_zero_hand_image.get_rect()
        if i>8:
            rect.topleft = ((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3))
        else:
            rect.topleft = ((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3))
        window.blit(p_zero_hand_image,rect)

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,((round(card_x*8.5)),(card_y*3)))

    window.blit(setup.card_back,(0,0))
    window.blit(setup.bonus_back,(0,card_y))

    window.blit(setup.card_back,(0,(notch_y+card_y*3)))
    discard_pile_image = setup.card_image_dict[setup.discard_pile[-1].color][int(setup.discard_pile[-1].card_id[1:])-1]
    window.blit(discard_pile_image,(card_x,(notch_y+card_y*3)))

    if moving_index != -1:
        moving_card_image = img_list[moving_index]
        rect = rect_list[moving_index]
        window.blit(moving_card_image,rect)

    return img_list,rect_list,topleft_list

def renderGameDiscardDraw(window,game_width,game_height,setup,instant_id):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)
    notch_y = round(max_surface_y * 1/17)

    if instant_id in ['R2','R7'] or (instant_id=='G4' and len(setup.draft_options)==0):
        placement_rect = pygame.Rect(card_x,(notch_y+card_y*3),card_x,card_y)
    elif instant_id in ['G4','R10']:
        placement_rect = pygame.Rect((round(card_x*5.25)), 0,card_x*3,card_y*4)

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y),10)
            grid_rect = pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),grid_rect,10)

    img_list = []
    rect_list = []
    topleft_list = []
    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    window.blit(setup.card_back, (card_x + card_x*j, 0 + card_y*i))
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    window.blit(p_one_image, (card_x + card_x*j, 0 + card_y*i))
            if setup.p_zero_grid[i][j] != 0 and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_zero_grid[i][j].flipped:
                    p_zero_image = setup.card_back
                else:
                    p_zero_image = setup.card_image_dict[setup.p_zero_grid[i][j].color][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                p_zero_image.convert()
                rect = p_zero_image.get_rect()
                rect.topleft = ((round(card_x*7.5)) + card_x*j, 0 + card_y*i)
                window.blit(p_zero_image,rect)

                if instant_id in ['R2','R7']:
                    img_list.append(p_zero_image)
                    rect_list.append(rect)
                    topleft_list.append(((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
            elif instant_id in ['R2','R7']:
                img_list.append(0)
                rect_list.append(pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y))
                topleft_list.append(((round(card_x*7.5)) + card_x*j, 0 + card_y*i))
    
    for i in range(len(setup.p_zero_hand)):
        p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
        p_zero_hand_image.convert()
        rect = p_zero_hand_image.get_rect()
        if i>8:
            rect.topleft = ((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3))

            if instant_id=='G4' and len(setup.draft_options)==0:
                topleft_list.append(((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3)))
        else:
            rect.topleft = ((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3))

            if instant_id=='G4' and len(setup.draft_options)==0:
                topleft_list.append(((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3)))
        window.blit(p_zero_hand_image,rect)

        if instant_id=='G4' and len(setup.draft_options)==0:
            img_list.append(p_zero_hand_image)
            rect_list.append(rect)

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,((round(card_x*8.5)),(card_y*3)))

    window.blit(setup.card_back,(0,0))
    window.blit(setup.bonus_back,(0,card_y))

    if len(setup.draft_options)>0:
        for i in range(len(setup.draft_options)):
            draft_options_image = setup.card_image_dict[setup.draft_options[i].color][int(setup.draft_options[i].card_id[1:])-1]
            draft_options_image.convert()
            rect = draft_options_image.get_rect()
            rect.topleft = (0 + card_x*i,(notch_y+card_y*3))
            window.blit(draft_options_image,rect)
            img_list.append(draft_options_image)
            rect_list.append(rect)
            topleft_list.append((0 + card_x*i,(notch_y+card_y*3)))
    else:
        window.blit(setup.card_back,(0,(notch_y+card_y*3)))
        discard_pile_image = setup.card_image_dict[setup.discard_pile[-1].color][int(setup.discard_pile[-1].card_id[1:])-1]
        window.blit(discard_pile_image,(card_x,(notch_y+card_y*3)))

    pygame.draw.rect(window,(150,150,150),placement_rect,10)

    return img_list,rect_list,topleft_list,placement_rect

def renderGameDiscardDraw_update(window,game_width,game_height,setup,instant_id,img_list,rect_list,topleft_list,moving_index):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)
    notch_y = round(max_surface_y * 1/17)

    if instant_id in ['R2','R7'] or (instant_id=='G4' and len(setup.draft_options)==0):
        placement_rect = pygame.Rect(card_x,(notch_y+card_y*3),card_x,card_y)
    elif instant_id in ['G4','R10']:
        placement_rect = pygame.Rect((round(card_x*5.25)), 0,card_x*3,card_y*4)

    for i in range(3):
        for j in range(3):
            pygame.draw.rect(window,(255,255,255),pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y),10)
            grid_rect = pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),grid_rect,10)

    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    window.blit(setup.card_back, (card_x + card_x*j, 0 + card_y*i))
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    window.blit(p_one_image, (card_x + card_x*j, 0 + card_y*i))
            if instant_id not in ['R2','R7'] and setup.p_zero_grid[i][j] != 0 and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_zero_grid[i][j].flipped:
                    p_zero_image = setup.card_back
                else:
                    p_zero_image = setup.card_image_dict[setup.p_zero_grid[i][j].color][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                p_zero_image.convert()
                rect = p_zero_image.get_rect()
                rect.topleft = ((round(card_x*7.5)) + card_x*j, 0 + card_y*i)
                window.blit(p_zero_image,rect)
    
    if not (instant_id=='G4' and len(setup.draft_options)==0):
        for i in range(len(setup.p_zero_hand)):
            p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
            p_zero_hand_image.convert()
            rect = p_zero_hand_image.get_rect()
            if i>8:
                rect.topleft = ((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3))
            else:
                rect.topleft = ((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3))
            window.blit(p_zero_hand_image,rect)

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,((round(card_x*8.5)),(card_y*3)))

    window.blit(setup.card_back,(0,0))
    window.blit(setup.bonus_back,(0,card_y))

    if len(setup.draft_options)==0:
        window.blit(setup.card_back,(0,(notch_y+card_y*3)))
        discard_pile_image = setup.card_image_dict[setup.discard_pile[-1].color][int(setup.discard_pile[-1].card_id[1:])-1]
        window.blit(discard_pile_image,(card_x,(notch_y+card_y*3)))

    for i in range(len(img_list)):
        if i!=moving_index and img_list[i]!=0:
            p_zero_image = img_list[i]
            rect = rect_list[i]
            window.blit(p_zero_image,rect)

    pygame.draw.rect(window,(150,150,150),placement_rect,10)

    if moving_index != -1:
        moving_card_image = img_list[moving_index]
        rect = rect_list[moving_index]
        window.blit(moving_card_image,rect)

    return img_list,rect_list,topleft_list,placement_rect

def renderGameFlip(window,game_width,game_height,setup,instant_id,highlight=-1):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 2/21)
    card_y = round(max_surface_y * 4/17)
    notch_y = round(max_surface_y * 1/17)

    for i in range(3):
        for j in range(3):
            placement_rect_opp = pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),placement_rect_opp,10)
            placement_rect = pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y)
            pygame.draw.rect(window,(255,255,255),placement_rect,10)

    rect_list = []
    flip_img_list = []
    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    p_one_image = setup.card_back
                    p_one_flip_image = setup.card_image_dict[setup.p_one_grid[i][j].card_id[:1]][int(setup.p_one_grid[i][j].card_id[1:])-1]
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    p_one_flip_image = setup.card_back
                p_one_image.convert()
                rect = p_one_image.get_rect()
                rect.topleft = (card_x + card_x*j, 0 + card_y*i)
                window.blit(p_one_image,rect)
                if instant_id=='R8':
                    flip_img_list.append(p_one_flip_image)
                    rect_list.append(rect)
            elif instant_id=='R8':
                flip_img_list.append(0)
                rect_list.append(pygame.Rect(card_x+card_x*j,0+card_y*i,card_x,card_y))
            
            if setup.p_zero_grid[i][j] != 0 and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_zero_grid[i][j].flipped:
                    p_zero_image = setup.card_back
                    p_zero_flip_image = setup.card_image_dict[setup.p_zero_grid[i][j].card_id[:1]][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                else:
                    p_zero_image = setup.card_image_dict[setup.p_zero_grid[i][j].color][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                    p_zero_flip_image = setup.card_back
                p_zero_image.convert()
                rect = p_zero_image.get_rect()
                rect.topleft = ((round(card_x*7.5)) + card_x*j, 0 + card_y*i)
                window.blit(p_zero_image,rect)
                if instant_id=='R4':
                    flip_img_list.append(p_zero_flip_image)
                    rect_list.append(rect)
            elif instant_id=='R4':
                flip_img_list.append(0)
                rect_list.append(pygame.Rect((round(card_x*7.5))+card_x*j,0+card_y*i,card_x,card_y))
    
    for i in range(len(setup.p_zero_hand)):
        p_zero_hand_image = setup.card_image_dict[setup.p_zero_hand[i].color][int(setup.p_zero_hand[i].card_id[1:])-1]
        p_zero_hand_image.convert()
        rect = p_zero_hand_image.get_rect()
        if i>8:
            rect.topleft = ((round(card_x*5.25)) + card_x*(i%3), 0 + card_y*(i//3))
        else:
            rect.topleft = ((round(card_x*4.25)) + card_x*(i%3), 0 + card_y*(i//3))
        window.blit(p_zero_hand_image,rect)

    player_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(player_bonus_image,((round(card_x*8.5)),(card_y*3)))

    window.blit(setup.card_back,(0,0))
    window.blit(setup.bonus_back,(0,card_y))

    window.blit(setup.card_back,(0,(notch_y+card_y*3)))
    discard_pile_image = setup.card_image_dict[setup.discard_pile[-1].color][int(setup.discard_pile[-1].card_id[1:])-1]
    window.blit(discard_pile_image,(card_x,(notch_y+card_y*3)))

    if highlight!=-1:
        window.blit(flip_img_list[highlight],rect_list[highlight])
        pygame.draw.rect(window,(150,150,150),rect_list[highlight],10)

    return rect_list

def renderGameResults(window,game_width,game_height,setup,p_zero_name,p_one_name,p_zero_score,p_one_score,p_zero_bonus_score,p_one_bonus_score,mouse_over='n/a'):
    window.fill((25, 25, 25))

    window_height = window.get_height()
    window_width = window.get_width()

    if  game_width/game_height < window_width/window_height:
        max_surface_x = round(window_height*(game_width/game_height))
        max_surface_y = window_height
    else:
        max_surface_x = window_width
        max_surface_y = round(window_width*(game_height/game_width))

    card_x = round(max_surface_x * 1/9)
    card_y = round(max_surface_y * 1/4)

    for i in range(3):
        for j in range(3):
            if setup.p_one_grid[i][j] != 0 and setup.p_one_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_one_grid[i][j].flipped:
                    window.blit(setup.card_back, (0 + card_x*j, 0 + card_y*i))
                else:
                    p_one_image = setup.card_image_dict[setup.p_one_grid[i][j].color][int(setup.p_one_grid[i][j].card_id[1:])-1]
                    window.blit(p_one_image, (0 + card_x*j, 0 + card_y*i))
            if setup.p_zero_grid[i][j] != 0 and setup.p_zero_grid[i][j].card_id not in ['A0','dA0','N0']:
                if setup.p_zero_grid[i][j].flipped:
                    window.blit(setup.card_back, (card_x*6 + card_x*j, 0 + card_y*i))
                else:
                    p_zero_image = setup.card_image_dict[setup.p_zero_grid[i][j].color][int(setup.p_zero_grid[i][j].card_id[1:])-1]
                    window.blit(p_zero_image, (card_x*6 + card_x*j, 0 + card_y*i))

    p_zero_bonus_image = setup.card_image_dict[setup.p_zero_bonus[0].card_id[0]][int(setup.p_zero_bonus[0].card_id[1:])-1]
    window.blit(p_zero_bonus_image,((card_x*7),(card_y*3)))

    p_one_bonus_image = setup.card_image_dict[setup.p_one_bonus[0].card_id[0]][int(setup.p_one_bonus[0].card_id[1:])-1]
    window.blit(p_one_bonus_image,((card_x*1),(card_y*3)))

    font = pygame.font.Font(None,50)
    font_small = pygame.font.Font(None,30)
    yes_text = font.render("RESTART",True,(89,141,81))
    no_text = font.render("QUIT",True,(198,56,72))
    yes_text_rect = yes_text.get_rect(center = (round(card_x*4.5),round(card_y*0.25)) )
    no_text_rect = no_text.get_rect(center = (round(card_x*4.5),round(card_y*0.75)) )

    yes_rect = pygame.Rect(card_x*4,0,card_x,round(card_y*0.5))
    no_rect = pygame.Rect(card_x*4,round(card_y*0.5),card_x,round(card_y*0.5))

    if mouse_over == 'y':
        pygame.draw.rect(window,(150,150,150),yes_rect,0)
    else:
        pygame.draw.rect(window,(50,50,50),yes_rect,0)
    pygame.draw.rect(window,(89,141,81),yes_rect,10)
    window.blit(yes_text,yes_text_rect)

    if mouse_over == 'n':
        pygame.draw.rect(window,(150,150,150),no_rect,0)
    else:
        pygame.draw.rect(window,(50,50,50),no_rect,0)
    pygame.draw.rect(window,(198,56,72),no_rect,10)
    window.blit(no_text,no_text_rect)

    if p_zero_score>p_one_score:
        winner=p_zero_name+" WINS!"
    elif p_one_score>p_zero_score:
        winner=p_one_name+" WINS!"
    else:
        winner="IT'S A TIE!"

    p_zero_score_text = str(p_zero_score-p_zero_bonus_score)+" + "+str(p_zero_bonus_score)+"\n\n   "+str(p_zero_score)
    p_one_score_text = str(p_one_score-p_one_bonus_score)+" + "+str(p_one_bonus_score)+"\n\n   "+str(p_one_score)

    results_text = font.render("Results:",True,(255,255,255))
    results_text_rect = results_text.get_rect(center = (round(card_x*4.5),round(card_y*1.5)) )
    window.blit(results_text,results_text_rect)

    winner_text = font.render(winner,True,(255,255,255))
    winner_text_rect = winner_text.get_rect(center = (round(card_x*4.5),round(card_y*3.5)) )
    window.blit(winner_text,winner_text_rect)

    p_zero_surface = pygame.Surface((card_x,card_y))
    p_zero_surface.fill((25, 25, 25))
    blit_text(p_zero_surface,p_zero_score_text,(0,0),font_small,(255,255,255))
    window.blit(p_zero_surface,(card_x*5,card_y*2))

    p_one_surface = pygame.Surface((card_x-20,card_y))
    p_one_surface.fill((25, 25, 25))
    blit_text(p_one_surface,p_one_score_text,(20,0),font_small,(255,255,255))
    window.blit(p_one_surface,(card_x*3,card_y*2))

    return yes_rect,no_rect