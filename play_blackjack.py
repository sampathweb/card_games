#!/usr/bin/env python
from __future__ import print_function
from blackjack import BlackJack


def play_blackjack(wager, max_wager):
    game = BlackJack(wager=wager, max_wager=max_wager, allow_split=True, allow_double_down=True)
    while True and not game.result:
        print('Your Hand %s is of value %s' % (game.player_hands, game.player_hands_value()))
        action = get_player_input(game.allow_split)
        if action == 1:  # Hit
            game.hit()
        elif action == 2:  # Stand
            game.stand()
        elif action == 3:  # Split
            game.split()
        else:
            pass
    print("Dealer's Final Hand %s is of value %d" % (game.dealer_hand, game.dealer_hand_value()))
    print('Result is: ', game.result)
    return game.result, game.wager_earned


def get_player_input(allow_split):
    '''Returns the action choice made by the Player.
    Player can choose to Hit(1), Stand(2) or Split(3)
    '''
    if allow_split:
        choices_avail = ['1', '2', '3']
        msg = 'Enter: hit (1), stand (2) or split (3) or help (h): '
    else:
        choices_avail = ['1', '2']
        msg = 'Enter: hit (1), stand (2) or help (h): '
    choice = 0
    while choice not in choices_avail:
        choice = raw_input(msg).upper()
        if choice == 'H':  # Help
            print('You can Hit (1): Draw one more card to see if you get closer to 21, but not higher.')
            print('You can Stand (2): Compare your current hand value with Dealer hand value to see if you scored higher, but still 21 or below.')
            if allow_split:
                print('You can Split (3): ')
    return int(choice)


def get_wager_input(max_chips, min_chips=1):
    chips = 0
    while chips < min_chips or chips > max_chips:
        chips = raw_input('How many chips do you wager? (min %d, max %d): ' % (min_chips, max_chips))
        try:
            chips = int(chips)
        except:
            chips = 0
    return chips


def _initialize_game():
    player = {}
    player['chips'] = 100
    player['round'] = 0
    player['won'] = 0
    player['lost'] = 0
    player['push'] = 0
    player['bust'] = 0
    return player

if __name__ == '__main__':
    player = _initialize_game()
    print('Welcome to BlackJack')
    print('-' * 20)
    print('You have 100 Chips to play this game.  On each round, you will have to wager atleast one chip.  You can wager more.')
    play = 'Y'
    while play != 'N' or player['chips'] > 0:
        play = raw_input('Play a round of BlackJack (Y/N)? ').upper()
        wager = get_wager_input(player['chips'])
        if play.upper() == 'Y':
            player['round'] += 1
            result, wager = play_blackjack(wager, player['chips'])
            player['chips'] += wager
            player[result] += 1
