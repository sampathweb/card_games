#!/usr/bin/env python
"""
Play blackjack, by running the program via command line: python play_blackjack.py
"""
from __future__ import print_function
import sys
from blackjack import BlackJack

# To get this program to work with both Python 2 and Python 3, input is assigned raw_input when running in Python 2
try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass


def play_blackjack(wager, max_wager):
    """Returns the game result and wage Earned. Plays One Round of BlackJack"""
    game = BlackJack(wager=wager, max_wager=max_wager, allow_split=True, allow_dd=True)
    player = game.players[0]
    print('\nYour Hand %s has %s points.  Your wager is: %d' % (player['hand'], game.player_hand_value(), player['wager']))
    print("Dealer's upcard is: ", game.get_dealer_upcard())
    if not game.verify_blackjack():
        req_split = input('\nWould you like to Split (Y/N)? ').upper()
        if req_split == 'Y':
            if game.split():  # Split
                print('Your hand has been split.  You will play one Hand at a time.', end='\n\n')
            else:
                print("Looks like you don't have enough credits to split.  Playing the round without the split")
    for hand_idx in range(len(game.players)):
        if hand_idx == 1:
            print('\nNow, Play your Second (Split) Hand.  Results will be shown at the end')
        player = game.players[hand_idx]
        while True and player['active']:
            print('Your hand %s has %s points.' % (player['hand'], game.player_hand_value(hand_idx)))
            action = get_player_input(player['allow_dd'])
            if action == 1:  # Hit
                game.hit(hand_idx)
            elif action == 2:  # Stand.  Round Ends when Player Chooses to Stand
                game.stand(hand_idx)
            elif action == 3:  # Double down
                game.double_down(hand_idx)
    results = []
    print('\nRound Results:')
    print('-' * 13)
    for hand_idx in range(len(game.players)):
        print('Your Hand %s with %s points.  Your wager was %d' % (player['hand'], game.player_hand_value(hand_idx), player['wager']))
        print("Dealer's Final Hand %s is of value %d" % (game.dealer_hand, game.dealer_hand_value()))
        print('Result: ', game.players[hand_idx]['result'])
        results.append(game.players[hand_idx]['result'])
    return results, game.wager_earned


def get_player_input(allow_double_down=True):
    """Returns the action choice made by the Player.
    Player can choose to Hit(1), Stand(2) or Double Down (3)
    """
    choices_avail = ['h', '1', '2']
    msg = 'Select: help (h), hit (1), stand (2)'
    if allow_double_down:
        choices_avail.append('3')
        msg += ' ,double down (3)'
    msg += ' :'
    choice = 0
    while choice not in choices_avail:
        choice = input(msg).upper()
        if choice == 'H':  # Help
            print('Choose One of the following:')
            print('Hit (1): Draw one more card to see if you get closer to 21, but not higher.')
            print('Stand (2): Compare your current hand value with Dealer hand value to see if you scored higher, but still 21 or below.')
            if allow_double_down:
                print('Double Down (3): ')
    return int(choice)


def get_wager_input(max_chips, min_chips=1):
    """Retuns the wager the player chooses for this round.  It cannot exceed the maximum available."""
    chips = 0
    while chips < min_chips or chips > max_chips:
        chips = input('How many chips do you wager? (min %d, max %d): ' % (min_chips, max_chips))
        try:
            chips = int(chips)
        except:
            chips = 0
    return chips


def _initialize_game(wager_credits):
    """Returns the initialized player attributes.
    This function is called just once, but the player dict is updated on each round
    """
    player = {}
    player['chips'] = wager_credits
    player['round'] = 0
    player['blackjack'] = 0
    player['won'] = 0
    player['lost'] = 0
    player['push'] = 0
    player['bust'] = 0
    return player

if __name__ == '__main__':
    """Entry point of the program when run via command line"""
    # Get the wager credits provided in run argument
    wager_credits = 100
    if len(sys.argv) >= 2:
        try:
            wager_credits = int(sys.argv[1])
        except:
            print('Could not convert the Wager Credits provided: %s into a number. Default credit of 100 provided.' % sys.argv[1])
    # Now, initailize the game and start the rounds
    player = _initialize_game(wager_credits)
    print('Welcome to BlackJack')
    print('*' * 20)
    print('You can play as many rounds as you want and as long as you have atleast 1 wager credit left to play.  You can wager more.')
    play = 'Y'
    # Play until the player says N or until he runs out of credits
    while play != 'N' and player['chips'] > 0:
        print('\nYou have %d wager credits to play this game.' % player['chips'])
        play = input('Play a round of BlackJack (Y/N)? ').upper()
        if play == 'Y':
            wager = get_wager_input(player['chips'])
            player['round'] += 1
            results, wager = play_blackjack(wager, player['chips'])
            player['chips'] += wager
            for result in results:  # Could be two hands with Split
                player[result] += 1
    print('\nFinal Results:')
    print('-' * 13)
    print('Your Final Wager Credits: ', player['chips'])
    print('Your results: %d blackjack, %d won, %d lost, %d bust, %d push' % (player['blackjack'], player['won'], player['lost'], player['bust'], player['push']))
    print('Thanks for playing BlackJack.')
