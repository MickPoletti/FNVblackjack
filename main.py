from pygame import draw
from pygame.time import wait
from Deck import Deck
import pygame, os, sys
from pygame.locals import *


# Setuo pygame Window
mainClock = pygame.time.Clock()

pygame.init()

# TITLE OF screen
pygame.display.set_caption("Blackjack v.0.1")

# CREATE screen
screen = pygame.display.set_mode((500,500), 5, 32)
    
if pygame.font:
    font = pygame.font.SysFont('segoeuiemoji', 14)
    titleFont = pygame.font.SysFont('segoeuiemoji', 52)
    text = font.render("Placeholder", True, (0,0,0))
    textRect = text.get_rect()
    textRect.center = (500 // 2, 500 // 2)    

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.center = (x , y)
    surface.blit(textobj, textrect)
    return textrect

def main_menu():
    exit = False
    click = False
    while not exit:
        screen.fill((0,0,0))
        draw_text("♠ Blackjack ♦", titleFont, (255,255,255), screen, 250, 100)
        
        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(150, 200, 200, 50)
        quit_button = pygame.Rect(150, 275, 200, 50)
        if play_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, (255, 255, 255), play_button, 2)
            draw_text("Play", font, (255,255,0), screen, 250, 225)
            if click:
                game()
        else:
            pygame.draw.rect(screen, (255, 255, 255), play_button)
            draw_text("Play", font, (0,0,0), screen, 250, 225)
        
        if quit_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, (255, 255, 255), quit_button, 2)
            draw_text("Quit", font, (255,255,0), screen, 250, 300)
            if click:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, (255, 255, 255), quit_button)
            draw_text("Quit", font, (0,0,0), screen, 250, 300)
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True    

        pygame.display.update()
        mainClock.tick(60)

def game():
    running = True
    deck = Deck()
    deck.shuffle()
    dealt = 0
    bet = 1
    chips = 100
    earnings = 0
    player_deck = []
    dealer_deck = []
    player_score = 0
    dealer_score = 0

    # Deal W)
    # Increase Bet E)
    # Decrease Bet Q)
    # Bet Max S)
    # Exit R)
    draw_gui(bet, chips, earnings, [], [], dealt)

    
    # TODO: 
    # Dealer stays at some limit no matter what
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_w: 
                    if dealt == 0:
                        player_deck = deck.deal()
                        dealer_deck = deck.deal()  
                        for card in player_deck:
                            player_score += card.value
                        for card in dealer_deck:
                            dealer_score += card.value                          
                        dealt += 1
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                    # else Double Down
                if event.key == K_f:
                    # hit me
                    if dealt == 0:
                        break
                    player_deck.append(deck.hit())
                    draw_player_cards(player_deck)
                    pygame.display.update() 
                    player_score += player_deck[-1].value
                    print(player_score)
                    if player_score > 21:
                        chips -= bet
                        earnings -= bet
                        bet = 1
                        dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score)
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                if event.key == K_e:
                    # increase bet
                    if bet < 10 and bet < chips:
                        bet+=1
                    elif bet >= 10 and bet < 25 and bet < chips:
                        bet+=5
                    elif bet >= 25 and bet < 100 and bet < chips:
                        bet+=25
                    elif bet >= 100 and bet < chips:
                        bet+=100
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                if event.key == K_q:
                    # decrease bet
                    if bet == 1:
                        break
                    elif bet <= 10:
                        bet-=1
                    elif bet > 10:
                        bet-=5
                    elif bet > 25:
                        bet-=25
                    elif bet > 100:
                        bet-=100
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                if event.key == K_s:
                    if dealt == 0:
                        bet = 10000
                if event.key == K_r:
                    if dealt == 0:
                        running = 0
                    else:
                        # stay
                        winner = calc_winner(player_score, dealer_score)
                        # TODO: add print in top left to say who won and how much
                        # TODO: here is where dealer will draw cards until stand limit or bust 
                        # clear board and set values
                        if winner == 1:
                            print("you win")
                            chips += bet
                            earnings += bet
                        elif winner == 0:
                            print("breakeven")
                        elif winner == -1:
                            chips -= bet
                            earnings -= bet
                            print("you lost")
                        dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score)                     
                        bet = 1
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
        #TODO: Need to update control text after dealing



        
        pygame.display.update()   
        mainClock.tick(60)

def draw_player_cards(cards):
    i = 0
    for card in cards:
        card_img = pygame.image.load("png/" + card.print())
        card_img = pygame.transform.scale(card_img, (150, 200))
        cardbox = pygame.Rect(140+30*i, 340, 150, 200)
        cardbox_shadow = pygame.Rect(138+30*i, 340, 150, 200)
        pygame.draw.rect(screen, (0, 0, 0), cardbox_shadow, 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), cardbox, 100, 10)
        pygame.display.flip()
        screen.blit(card_img, (140+30*i,340))
        i += 1

def draw_dealer_cards(cards):
    i = 0
    for card in cards:
        if i == 0:
            card_img = pygame.image.load("png/back.png")
            card_img = pygame.transform.scale(card_img, (150, 200))
        else:
            card_img = pygame.image.load("png/" + card.print())
            card_img = pygame.transform.scale(card_img, (150, 200))
        cardbox = pygame.Rect(140+30*i, 0, 150, 200)
        cardbox_shadow = pygame.Rect(138+30*i, 0, 150, 200)
        pygame.draw.rect(screen, (0, 0, 0), cardbox_shadow, 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), cardbox, 100, 10)
        pygame.display.flip()
        screen.blit(card_img, (140+30*i,0))
        i += 1
    
def draw_gui(bet, chips, earnings, player_cards=[], dealer_cards=[], dealt=0):
    screen.fill((0,0,0))
    table_bg = pygame.image.load('tops_logo.png').convert()
    screen.blit(table_bg, (-250,-60))

    draw_text("Current Bet: ", font, (255,255,0), screen, 56, 420)
    draw_text(str(bet), font, (255,255,0), screen, 110, 420)
    draw_text("Chips: ", font, (255,255,0), screen, 37, 440)
    draw_text(str(chips), font, (255,255,0), screen, 110, 440)
    draw_text("Earnings: ", font, (255,255,0), screen, 47, 460)
    draw_text(str(earnings), font, (255,255,0), screen, 110, 460)

    if dealt == 1:
        draw_text("Hit F)", font, (255,255,0), screen, 460, 380)
        draw_text("Double Down W)", font, (255,255,0), screen, 439, 400)
        draw_text("Split E)", font, (255,255,0), screen, 435, 420)
        draw_text("Switch Hands Q)", font, (255,255,0), screen, 450, 440)
        draw_text("Surrender S)", font, (255,255,0), screen, 465, 460)
        draw_text("Stay R)", font, (255,255,0), screen, 465, 480)
    else:
        draw_text("Deal W)", font, (255,255,0), screen, 460, 380)
        draw_text("Increase Bet E)", font, (255,255,0), screen, 439, 400)
        draw_text("Decrease Bet Q)", font, (255,255,0), screen, 435, 420)
        draw_text("Bet Max S)", font, (255,255,0), screen, 450, 440)
        draw_text("Exit R)", font, (255,255,0), screen, 465, 460)

    if len(player_cards) > 0:
        draw_player_cards(player_cards)
        draw_dealer_cards(dealer_cards)

def calc_winner(player_score, dealer_score):
    if player_score > dealer_score:
        return 1
    elif player_score == dealer_score:
        return 0
    else:
        return -1

def reset_game(player_deck, dealer_deck, deck, player_score, dealer_score):
    for card in player_deck:
        c = player_deck.pop()
        deck.cards.append(c)
    for card in dealer_deck:
        c = dealer_deck.pop()
        deck.cards.append(c)
        deck.shuffle()
    player_score = 0
    dealer_score = 0
    player_deck.clear()
    dealer_deck.clear()
    wait(1000)
    return 0, player_score, dealer_score

main_menu()