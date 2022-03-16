from pygame import draw
from pygame.time import wait
from Deck import Deck
import pygame, os, sys
from pygame.locals import *


# Setuo pygame Window
mainClock = pygame.time.Clock()

programIcon = pygame.image.load('png/icon.png')

pygame.display.set_icon(programIcon)

pygame.init()

# TITLE OF screen
pygame.display.set_caption("Blackjack v.0.1")

# CREATE screen
screen = pygame.display.set_mode((500,500), 5, 32)

# CREATE terminal
terminal = pygame.Rect(140, 240, 180, 50)
terminalfont = pygame.font.SysFont('monofonto', 20)
    
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
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                click = True    

        pygame.display.update()
        mainClock.tick(60)

def game():
    running = True
    deck = Deck()
    deck_copy = deck.cards
    deck.shuffle()
    dealt = 0
    bet = 1
    chips = 100
    earnings = 0
    player_deck = []
    dealer_deck = []
    player_score = 0
    dealer_score = 0

    draw_gui(bet, chips, earnings, [], [], dealt)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_w: 
                    if chips <= 0:
                        print("You lost!")
                        # TODO: Track user money and when out of money display lose screen
                    elif dealt == 0:
                        player_deck = deck.deal()
                        dealer_deck = deck.deal()  
                        for card in player_deck:
                            player_score += card.value
                        for card in dealer_deck:
                            dealer_score += card.value                          
                        print(dealer_score)
                        print(player_score)
                        dealt = 1
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                        draw_player_cards(player_deck)
                        draw_dealer_cards(dealer_deck, False)
                        # Player drew over 21 (busted) -> Player loses
                        if player_score > 21:
                            chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "bust")
                            dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score, deck_copy)    
                        # Player got a blackjack reward chips and print blackjack special win
                        elif player_score == 21:
                            chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "blackjack")
                            dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score, deck_copy)    
                        # Dealer drew over 21 (busted) -> Player wins
                        elif dealer_score > 21:
                            chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "win")
                            dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score, deck_copy)    
                        #Dealer got 
                        elif dealer_score == 21:
                            chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "lose")
                            dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score, deck_copy)
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                    # else Double Down
                
                # hit me
                if event.key == K_f:
                    if dealt == 0:
                        break
                    player_deck.append(deck.hit())
                    draw_player_cards(player_deck)
                    pygame.display.update() 
                    player_score += player_deck[-1].value
                    if player_score > 21:
                        chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "bust")
                        dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score, deck_copy)    
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                
                # increase bet
                if event.key == K_e:
                    if bet < 10 and bet < chips:
                        bet+=1
                    elif bet >= 10 and bet < 25 and bet < chips:
                        bet+=5
                    elif bet >= 25 and bet < 100 and bet < chips:
                        bet+=25
                    elif bet >= 100 and bet < chips:
                        bet+=100
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)

                # decrease bet
                if event.key == K_q:
                    if bet == 1:
                        break
                    elif bet <= 10:
                        bet-=1
                    elif bet >= 10 and bet <= 25:
                        bet-=5
                    elif bet >= 50 and bet <= 100:
                        bet-=25
                    elif bet > 200:
                        bet-=100
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)

                if event.key == K_s and dealt == 0 and chips > 0:
                    bet = chips
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                if event.key == K_r:
                    # Cards not dealt so exit to main menu
                    if dealt == 0:
                        running = 0
                    # User chooses to stay
                    else:
                        # Check if dealer is at 16 if not then add cards to his hand until he is at or passed that value
                        if dealer_score <= 16:
                            while dealer_score <= 16:
                                dealer_deck.append(deck.hit())
                                draw_dealer_cards(dealer_deck, True)
                                dealer_score += int(dealer_deck[-1].value)
                        draw_dealer_cards(dealer_deck, True)
                        winner = calc_winner(player_score, dealer_score)
                        # TODO: add print in top left to say who won and how much
                        # TODO: here is where dealer will draw cards until stand limit or draw_game_event 
                        # clear board and set values
                        # Player won
                        if winner == 1:
                            chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "win")
                        # Breakeven
                        elif winner == 0:
                            chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "breakeven")
                        # Player lose
                        elif winner == -1:
                            chips, earnings, bet = draw_game_event(chips, earnings, bet, player_deck, dealer_deck, "lose")
                        dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, deck, player_score, dealer_score, deck_copy)
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
        
        pygame.display.update()   
        mainClock.tick(60)

def draw_game_event(chips, earnings, bet, player_deck, dealer_deck, action):
    s_bet = str(bet)
    if action == "bust":
        chips -= bet
        earnings -= bet
        action = "Bust! You lost " + s_bet + " chip(s)"
    elif action == "win":
        chips += bet
        earnings += bet
        action = "You win " + s_bet + " chip(s)!"
    elif action == "lose":
        chips -= bet
        print(chips)
        earnings -= bet
        action = "You lose " + s_bet + " chip(s)"
    elif action == "blackjack":
        bet += 100
        chips += bet
        earnings += bet
        action = "Blackjack! You win " + s_bet + " chip(s)!"

    bet = 1
    draw_player_cards(player_deck)
    draw_dealer_cards(dealer_deck, True)
    pygame.draw.rect(screen, (0, 0, 0), terminal, border_radius=5)
    #pygame.draw.rect(surface, color, pygame.Rect(
    #30, 30, 60, 60),  2,  border_bottom_right_radius=5)
    draw_text("> ", terminalfont, (255,255,0), screen, 150, 265)
    draw_text(action, terminalfont, (255,255,0), screen, 240, 265)
    screen.blit(screen, (0,0))
    pygame.display.update()
    wait(1000)
    return chips, earnings, bet

def draw_player_cards(cards):
    i = 0
    for card in cards:
        card_img = pygame.image.load("png/cards/" + card.print())
        card_img = pygame.transform.scale(card_img, (150, 200))
        cardbox = pygame.Rect(140+30*i, 340, 150, 200)
        cardbox_shadow = pygame.Rect(138+30*i, 340, 150, 200)
        pygame.draw.rect(screen, (0, 0, 0), cardbox_shadow, 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), cardbox, 100, 10)
        pygame.display.flip()
        screen.blit(card_img, (140+30*i,340))
        pygame.display.update()
        i += 1

def draw_dealer_cards(cards, final):
    i = 0
    for card in cards:
        if i == 0 and final == False:
            card_img = pygame.image.load("png/cards/back.png")
            card_img = pygame.transform.scale(card_img, (150, 200))
        else:
            card_img = pygame.image.load("png/cards/" + card.print())
            card_img = pygame.transform.scale(card_img, (150, 200))
        cardbox = pygame.Rect(140+30*i, 0, 150, 200)
        cardbox_shadow = pygame.Rect(138+30*i, 0, 150, 200)
        pygame.draw.rect(screen, (0, 0, 0), cardbox_shadow, 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), cardbox, 100, 10)
        pygame.display.flip()
        screen.blit(card_img, (140+30*i,0))
        pygame.display.update()
        i += 1
    
def draw_gui(bet, chips, earnings, player_cards=[], dealer_cards=[], dealt=0):
    screen.fill((0,0,0))
    table_bg = pygame.image.load('png/tops_logo.png').convert()
    screen.blit(table_bg, (-250,-60))

    draw_text("Current Bet: ", font, (255,255,0), screen, 56, 420)
    draw_text(str(bet), font, (255,255,0), screen, 110, 420)
    draw_text("Chips: ", font, (255,255,0), screen, 37, 440)
    draw_text(str(chips), font, (255,255,0), screen, 110, 440)
    draw_text("Earnings: ", font, (255,255,0), screen, 47, 460)
    draw_text(str(earnings), font, (255,255,0), screen, 110, 460)
    
    # =Deal Menu=
    # Deal W)
    # Increase Bet E)
    # Decrease Bet Q)
    # Bet Max S)
    # Exit R)

    # =Play Menu= 
    # Hit F)
    # Double Down W)
    # Split E)
    # Switch Hands Q)
    # Surrender S)
    # Stay R)

    if dealt == 1:
        draw_text("Hit F)", font, (255,255,0), screen, 460, 380)
        draw_text("Double Down W)", font, (255,255,0), screen, 424, 400)
        draw_text("Split E)", font, (255,255,0), screen, 455, 420)
        draw_text("Switch Hands Q)", font, (255,255,0), screen, 425, 440)
        draw_text("Surrender S)", font, (255,255,0), screen, 437, 460)
        draw_text("Stay R)", font, (255,255,0), screen, 454, 480)
    else:
        draw_text("Deal W)", font, (255,255,0), screen, 460, 380)
        draw_text("Increase Bet E)", font, (255,255,0), screen, 439, 400)
        draw_text("Decrease Bet Q)", font, (255,255,0), screen, 435, 420)
        draw_text("Bet Max S)", font, (255,255,0), screen, 450, 440)
        draw_text("Exit R)", font, (255,255,0), screen, 465, 460)

    if len(player_cards) > 0:
        draw_player_cards(player_cards)
        draw_dealer_cards(dealer_cards, False)

def calc_winner(player_score, dealer_score):
    if player_score > 21:
        return -1
    elif dealer_score > 21:
        return 1
    elif player_score > dealer_score:
        return 1
    elif player_score == dealer_score:
        return 0
    else:
        return -1

def reset_game(player_deck, dealer_deck, deck, p_score, d_score, deck_copy):
    for card in player_deck:
        player_deck.pop()
    for card in dealer_deck:
        dealer_deck.pop()
    p_score = 0
    d_score = 0
    player_deck.clear()
    dealer_deck.clear()
    deck.cards = deck_copy
    deck.shuffle()
    return 0, p_score, d_score

main_menu()