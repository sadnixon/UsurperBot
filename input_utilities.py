import pygame
from gameRender import *
from utilities import check_possible_placement
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

def input_waiter_xy(game_width,game_height,game_surface,screen,setup,card_selection_index,player=True):
    card_placement_x = -1
    card_placement_y = -1

    screen_height = screen.get_height()
    screen_width = screen.get_width()
    if  game_width/game_height < screen_width/screen_height:
        max_surface_x = round(screen_height*(game_width/game_height))
        max_surface_y = screen_height
    else:
        max_surface_x = screen_width
        max_surface_y = round(screen_width*(game_height/game_width))

    while (not (card_placement_x in range(3) and card_placement_y in range(3))) or [setup.p_zero_grid, setup.p_one_grid][setup.turn][card_placement_x][card_placement_y] != 0 or [setup.p_zero_hand, setup.p_one_hand][setup.turn][card_selection_index].placement_grid[card_placement_x][card_placement_y] == 0:
        #print("Input valid coords from 0 to 2")
        
        

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                setup.set_card_sizes(event.size[0],event.size[1],game_width,game_height)
            elif event.type == KEYDOWN:
                if int(event.key) in keys_to_coords:
                    card_placement_x,card_placement_y = keys_to_coords[int(event.key)]
            elif event.type == MOUSEBUTTONDOWN:
                bottom_cards = max_surface_y*0.594375
                if player:
                    left_cards = max_surface_x*(8/11)
                else:
                    left_cards = max_surface_x*(1/11)
                cards_divisor = max_surface_x*(3/11)
                mouse_x, mouse_y = event.pos
                #YES I KNOW THIS IS STUPID, BUT I DIDNT THINK ABOUT THE X AND Y THING WHEN I INVENTED GRID NOTATION
                card_placement_x = math.floor((mouse_y/bottom_cards)*3)
                card_placement_y = math.floor(((mouse_x-left_cards)/cards_divisor)*3)
                print(card_placement_x,card_placement_y)

        #renderGameNext(game_surface,setup)

        screen_height = screen.get_height()
        screen_width = screen.get_width()
        if  game_width/game_height < screen_width/screen_height:
            max_surface_x = round(screen_height*(game_width/game_height))
            max_surface_y = screen_height
        else:
            max_surface_x = screen_width
            max_surface_y = round(screen_width*(game_height/game_width))
        screen_surface = pygame.Surface((max_surface_x, max_surface_y))
        pygame.transform.smoothscale(game_surface, (max_surface_x, max_surface_y),screen_surface)
        screen.blit(screen_surface,(0, 0))
        pygame.display.update()
    return card_placement_x,card_placement_y



def input_waiter_play(screen,setup,game_width,game_height,player=True):
    card_placement_x = -1
    card_placement_y = -1
    card_selection_index = -1

    img_list,rect_list,topleft_list,placement_rect_list = renderGameNext2(screen,game_width,game_height,setup)

    moving = False
    moving_index = -1

    while (not (card_placement_x in range(3) and card_placement_y in range(3))) or [setup.p_zero_grid, setup.p_one_grid][setup.turn][card_placement_x][card_placement_y] != 0 or [setup.p_zero_hand, setup.p_one_hand][setup.turn][card_selection_index].placement_grid[card_placement_x][card_placement_y] == 0:
        #print("Input valid coords from 0 to 2")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                print('resized')
                setup.set_card_sizes(event.size[0],event.size[1],game_width,game_height)
                img_list,rect_list,topleft_list,placement_rect_list = renderGameNext2(screen,game_width,game_height,setup)
            elif event.type == MOUSEBUTTONDOWN:
                print(event.pos)
                for rect in rect_list:
                    if rect.collidepoint((event.pos[0],event.pos[1])):
                        moving = True
                        moving_index = rect_list.index(rect)
                        print(moving_index)
            elif event.type == MOUSEBUTTONUP:
                for placement_rect in placement_rect_list:
                    if placement_rect.collidepoint(event.pos):
                        rect_index = placement_rect_list.index(placement_rect)
                        card_placement_x = rect_index//3
                        card_placement_y = rect_index%3
                        card_selection_index = moving_index
                if card_selection_index == -1:
                    rect_list[moving_index].topleft = topleft_list[moving_index]
                moving = False
                moving_index = -1
            elif event.type == MOUSEMOTION and moving:
                rect_list[moving_index].move_ip(event.rel)

        renderGameNext2_update(screen,game_width,game_height,setup,img_list,rect_list,topleft_list,moving_index)

        pygame.display.update()
    return card_selection_index,card_placement_x,card_placement_y


def input_waiter_draft(screen,setup,game_width,game_height,player=True):
    draft_selection_index = -1

    img_list,rect_list,topleft_list,placement_rect = renderGame(screen,game_width,game_height,setup)

    moving = False
    moving_index = -1

    while draft_selection_index not in range(6):

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                print('resized')
                setup.set_card_sizes(event.size[0],event.size[1],game_width,game_height)
                img_list,rect_list,topleft_list,placement_rect = renderGame(screen,game_width,game_height,setup)
            elif event.type == MOUSEBUTTONDOWN:
                print(event.pos)
                for rect in rect_list:
                    if rect.collidepoint((event.pos[0],event.pos[1])):
                        moving = True
                        moving_index = rect_list.index(rect)
                        print(moving_index)
            elif event.type == MOUSEBUTTONUP:
                if placement_rect.collidepoint(event.pos):
                    draft_selection_index = moving_index
                if draft_selection_index == -1:
                    rect_list[moving_index].topleft = topleft_list[moving_index]
                moving = False
                moving_index = -1
            elif event.type == MOUSEMOTION and moving:
                rect_list[moving_index].move_ip(event.rel)
            elif event.type == KEYDOWN:
                draft_selection_index = int(event.key)-49

        renderGame_update(screen,game_width,game_height,setup,img_list,rect_list,topleft_list,moving_index)

        pygame.display.update()
    return draft_selection_index

def input_waiter_yesno(screen,setup,game_width,game_height,instant_id,highlight_x=-1,highlight_y=-1):

    decision = 'n/a'
    mouse_over = 'n/a'

    renderGameNext2(screen,game_width,game_height,setup)
    yes_rect, no_rect = renderYesNo(screen,game_width,game_height,instant_id,highlight_x,highlight_y,mouse_over)

    while decision == 'n/a':

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.display.quit()
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                print('resized')
                setup.set_card_sizes(event.size[0],event.size[1],game_width,game_height)
                renderGameNext2(screen,game_width,game_height,setup)
                yes_rect, no_rect = renderYesNo(screen,game_width,game_height,instant_id,highlight_x,highlight_y,mouse_over)
            elif event.type == MOUSEBUTTONUP:
                if yes_rect.collidepoint(event.pos):
                    decision = 'y'
                elif no_rect.collidepoint(event.pos):
                    decision = 'n'
            elif event.type == KEYDOWN:
                if event.key == 121:
                    decision = 'y'
                elif event.key == 110:
                    decision = 'n'
        if yes_rect.collidepoint(pygame.mouse.get_pos()):
            mouse_over = 'y'
        elif no_rect.collidepoint(pygame.mouse.get_pos()):
            mouse_over = 'n'
        else:
            mouse_over = 'n/a'

        renderYesNo(screen,game_width,game_height,instant_id,highlight_x,highlight_y,mouse_over)

        pygame.display.update()
    return decision