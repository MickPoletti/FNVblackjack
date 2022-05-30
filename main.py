from pygame import draw
from pygame.time import wait
from Deck import Deck
import PySimpleGUI as sg
import pygame, os, sys
from pygame.locals import *


# Setup pygame Window
mainClock = pygame.time.Clock()

# SET ICON IMAGE
programIcon = pygame.image.load("./png/blackjack.png")

pygame.display.set_icon(programIcon)

pygame.init()

# TITLE OF screen
pygame.display.set_caption("Blackjack v.0.5")

# CREATE screen
screen = pygame.display.set_mode((500,500), 5, 32)

# GLOBALS
streak = 0
volume = 0.5
fx_volume = 0.5
hit = 0
use_unpause = False
deck = Deck()

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
    global use_unpause
    exit = False
    click = False
    while not exit:
        screen.fill((0,0,0))
        draw_text("♠ Blackjack ♦", titleFont, (255,255,255), screen, 250, 100)
        
        mx, my = pygame.mouse.get_pos()

        play_button = pygame.Rect(150, 200, 200, 50)
        settings_button = pygame.Rect(150, 275, 200, 50)
        quit_button = pygame.Rect(150, 350, 200, 50)
        if play_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, (255, 255, 255), play_button, 2)
            draw_text("Play", font, (255,255,0), screen, 250, 225)
            if click:
                if use_unpause:
                    pygame.mixer.Channel(0).unpause()
                    use_unpause = False
                else:
                    play_music()
                game()
        else:
            pygame.draw.rect(screen, (255, 255, 255), play_button)
            draw_text("Play", font, (0,0,0), screen, 250, 225)
        if settings_button.collidepoint((mx,my)):
            pygame.draw.rect(screen, (255, 255, 255), settings_button, 2)
            draw_text("Settings", font, (255,255,0), screen, 250, 300)
            if click:
                settings()
        else:
            pygame.draw.rect(screen, (255, 255, 255), settings_button)
            draw_text("Settings", font, (0,0,0), screen, 250, 300)        
        if quit_button.collidepoint((mx, my)):
            pygame.draw.rect(screen, (255, 255, 255), quit_button, 2)
            draw_text("Quit", font, (255,255,0), screen, 250, 375)
            if click:
                pygame.quit()
                sys.exit()
        else:
            pygame.draw.rect(screen, (255, 255, 255), quit_button)
            draw_text("Quit", font, (0,0,0), screen, 250, 375)
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

def play_music():
    pygame.mixer.init()
    pygame.mixer.music.load("./music/rnv.wav")
    pygame.mixer.Channel(0).set_volume(volume)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound('./music/rnv.wav'))

def play_chips():
    pygame.mixer.init()
    pygame.mixer.music.load("./sounds/chips.wav")
    pygame.mixer.Channel(1).set_volume(fx_volume)
    pygame.mixer.Channel(1).play(pygame.mixer.Sound('./sounds/chips.wav'))

def play_applause():
    pygame.mixer.init()
    pygame.mixer.music.load("./sounds/applause.wav")
    pygame.mixer.Channel(2).set_volume(fx_volume)
    pygame.mixer.Channel(2).play(pygame.mixer.Sound('./sounds/applause.wav'))

def settings():
    global volume, fx_volume
    sg.theme('Black')

    layout = [
        [sg.Text('Settings', size=(30, 1), font=(titleFont, 25))],
        [sg.Text('Music Volume', size=(20,1), font=(titleFont, 15)),
         sg.Slider(range=(0, 100), orientation='h', size=(34, 20), key='slide1', default_value=volume*100)],
        [sg.Text('Effects', size=(20,1), font=(titleFont, 15)),
         sg.Slider(range=(0, 100), orientation='h', size=(34, 20), key='slide2', default_value=fx_volume*100)],
        
        [sg.Button('Exit'),
         sg.Text(' ' * 40), sg.Button('Save')]
    ]

    window = sg.Window('Settings', layout, default_element_size=(40, 1), grab_anywhere=False)

    while True:
        event, values = window.read()

        if event == 'Save':
            volume = float(values['slide1'])/100
            fx_volume = float(values['slide2'])/100
            #filename = sg.popup_get_file('Save Settings', save_as=True, no_window=True)
            #window.SaveToDisk(filename)
            # save(values)
        elif event == 'LoadSettings':
            filename = sg.popup_get_file('Load Settings', no_window=True)
            window.LoadFromDisk(filename)
            # load(form)
        elif event in ('Exit', None):
            break

    window.close()


def game():
    running = True
    global deck, hit
    deck.shuffle()
    dealt = 0
    bet = 1
    chips = 100
    earnings = 0
    player_deck = []
    dealer_deck = []
    player_score = 0
    dealer_score = 0
    split = False
    doubleDown = False
    global use_unpause

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
                        dealt += 1
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                        if player_score == 21 or player_score > 21:
                            draw_dealer_cards(dealer_deck, True)
                            chips, earnings = calc_winner(player_score, dealer_score, chips, bet, earnings, player_deck, dealer_deck)
                            wait(900)
                            dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, player_score, dealer_score)                       
                            draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                            hit = 0
                            draw_player_cards(player_deck)
                            draw_dealer_cards(dealer_deck, False)
                    # else Double Down
                    else:
                        if hit > 0:
                            # do nothing
                            doubleDown = False
                            break
                        if doubleDown == False:
                            bet = bet * 2
                            doubleDown = True
                if event.key == K_f:
                    # hit me
                    hit+=1
                    if dealt == 0:
                        break
                    player_deck.append(deck.hit())
                    draw_player_cards(player_deck)
                    pygame.display.update() 
                    player_score += player_deck[-1].value
                    if player_score > 21 or player_score == 21:
                        draw_dealer_cards(dealer_deck, True)
                        chips, earnings = calc_winner(player_score, dealer_score, chips, bet, earnings, player_deck, dealer_deck)
                        dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, player_score, dealer_score)
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                        hit = 0
                        wait(900)
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                if event.key == K_e:
                    # increase bet
                    if dealt == 0:
                        if bet < 10 and bet < chips:
                            bet+=1
                        elif bet >= 10 and bet < 25 and bet < chips:
                            bet+=5
                        elif bet >= 25 and bet < 100 and bet < chips:
                            bet+=25
                        elif bet >= 100 and bet < chips:
                            bet+=100
                    else:
                        split = 1        
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                if event.key == K_q:
                    # decrease bet
                    if dealt == 0:
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
                if event.key == K_s and chips > 0:
                    if dealt == 0:
                        bet = chips
                    else:
                        chips -= bet
                        earnings -= bet
                        dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, player_score, dealer_score)
                    draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                if event.key == K_r:
                    # Cards not dealt so exit to main menu
                    if dealt == 0:
                        running = 0
                        pygame.mixer.Channel(0).pause()
                        use_unpause = True
                    # User chooses to stay
                    else:
                        # Check if dealer is at 16 if not then add cards to his hand until he is at or passed that value
                        if dealer_score <= 16:
                            while dealer_score <= 16:
                                dealer_deck.append(deck.hit())
                                draw_dealer_cards(dealer_deck, True)
                                dealer_score += int(dealer_deck[-1].value)
                        draw_dealer_cards(dealer_deck, True)
                        chips, earnings = calc_winner(player_score, dealer_score, chips, bet, earnings, player_deck, dealer_deck)
                        # TODO: add print in top left to say who won and how much
                        # TODO: here is where dealer will draw cards until stand limit or draw_game_event 
                        # clear board and set values
                        dealt, player_score, dealer_score = reset_game(player_deck, dealer_deck, player_score, dealer_score)
                        draw_gui(bet, chips, earnings, player_deck, dealer_deck, dealt)
                        hit = 0
        
        pygame.display.update()   
        mainClock.tick(60)

def draw_game_event(bet, player_deck, dealer_deck, action):
    s_bet = str(bet)
    if action == "bust":
        action = "Bust! You lost " + s_bet + " chip(s)"
    elif action == "win":
        action = "You win " + s_bet + " chip(s)!"
    elif action == "lose":
        action = "You lose " + s_bet + " chip(s)"
    elif action == "blackjack":
        action = "Blackjack! You win " + s_bet + " chip(s)!"
    elif action == "breakeven":
        action = "You breakeven."

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
    global hit
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
    if dealt == 1 and hit == 0:
        draw_text("Hit F)", font, (255,255,0), screen, 460, 380)
        draw_text("Double Down W)", font, (255,255,0), screen, 424, 400)
        draw_text("Split E)", font, (255,255,0), screen, 455, 420)
        draw_text("Switch Hands Q)", font, (255,255,0), screen, 425, 440)
        draw_text("Surrender S)", font, (255,255,0), screen, 437, 460)
        draw_text("Stay R)", font, (255,255,0), screen, 454, 480)
    elif dealt == 1 and hit > 0:
        draw_text("Hit F)", font, (255,255,0), screen, 470, 380)
        draw_text("Double Down W)", font, (161,161,0), screen, 435, 400)
        draw_text("Split E)", font, (255,255,0), screen, 465, 420)
        draw_text("Switch Hands Q)", font, (255,255,0), screen, 435, 440)
        draw_text("Surrender S)", font, (255,255,0), screen, 448, 460)
        draw_text("Stay R)", font, (255,255,0), screen, 465, 480)
    else:
        draw_text("Deal W)", font, (255,255,0), screen, 460, 380)
        draw_text("Increase Bet E)", font, (255,255,0), screen, 439, 400)
        draw_text("Decrease Bet Q)", font, (255,255,0), screen, 435, 420)
        draw_text("Bet Max S)", font, (255,255,0), screen, 450, 440)
        draw_text("Exit R)", font, (255,255,0), screen, 465, 460)

    if len(player_cards) > 0:
        draw_player_cards(player_cards)
        draw_dealer_cards(dealer_cards, False)

def calc_winner(player_score, dealer_score, chips, bet, earnings, player_deck, dealer_deck):
    global streak
    if player_score > 21:
        chips -= bet
        earnings -= bet
        streak = 0
        draw_game_event(bet, player_deck, dealer_deck, "bust")
    elif player_score == 21:
        chips += bet
        earnings += bet
        streak += 1
        draw_game_event(bet, player_deck, dealer_deck, "blackjack")
    elif player_score == dealer_score:
        streak = 0
        draw_game_event(bet, player_deck, dealer_deck, "breakeven")
    elif player_score > dealer_score or dealer_score > 21:
        chips += bet
        earnings += bet
        streak += 1
        draw_game_event(bet, player_deck, dealer_deck, "win")
    else:
        chips -= bet
        earnings -= bet
        streak = 0
        draw_game_event(bet, player_deck, dealer_deck, "lose")
    play_chips()
    if streak > 4 :
        play_applause()
        draw_game_event(bet, player_deck, dealer_deck, "You feel lucky...")
    return chips, earnings

def reset_game(player_deck, dealer_deck, player_score, dealer_score):
    global deck
    deck.assemble()
    deck.shuffle()
    player_score = 0
    dealer_score = 0
    player_deck.clear()
    dealer_deck.clear()
    wait(1000)
    return 0, player_score, dealer_score

main_menu()