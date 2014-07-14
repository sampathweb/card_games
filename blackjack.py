#!/usr/bin/env python
"""
A package to wrap the rules of BlackJack.
"""
from __future__ import print_function
import random


class BlackJack(object):

    def __init__(self, wager=1, max_wager=1, dealer_min=17, allow_soft_limit=True, allow_split=True, allow_dd=True, allow_dd_after_split=True):
        """Returns None.  Initiailizes the Game with rules, wager limits and draws the initial set of two cards for player and dealer"""
        self.max_wager = max_wager
        self.dealer_min = dealer_min
        self.allow_soft_limit = allow_soft_limit
        self.allow_split = allow_split
        self.allow_dd_after_split = allow_dd_after_split  # Allow Double Down after Split
        self.card_suits = ['Spade', 'Heart', 'Diamond', 'Club']
        self.card_faces = {str(numb): numb for numb in range(2, 11)}
        for face in ('jack', 'king', 'queen'):
            self.card_faces[face] = 10
        self.card_faces['ace'] = 11
        # Set the player hand, Dealer hand
        self.players = []  # Assume One Player Hand (No Split)
        self.players.append(self._init_player(wager, allow_dd))
        self.dealer_hand = []
        self.wager_earned = 0
        self.card_deck = [(face, suit) for suit in self.card_suits for face in self.card_faces.keys()]
        random.shuffle(self.card_deck)  # Shuffle the card deck
        # Draw two cards for Player and Dealer
        self.players[0]['hand'].append(self._pick_card())
        self.players[0]['hand'].append(self._pick_card())
        self.dealer_hand.append(self._pick_card())
        self.dealer_hand.append(self._pick_card())
        self.verify_blackjack()  # Verify if hand has hit a blackjack
        return None

    def _init_player(self, wager, allow_dd):
        player = {
            'hand': [],
            'wager': wager,
            'active': True,
            'allow_dd': allow_dd,
            'result': None
        }
        return player

    def _face_value(self, face_numb):
        '''Returns card value for the card. Card needs to be of format (face, suit)'''
        return self.card_faces[face_numb]

    def _pick_card(self):
        '''Draws a Card from the Deck and return the card'''
        return self.card_deck.pop()

    def _get_hand_value(self, hand, allow_soft_limit=True):
        hand_values = [0]
        for face, suit in hand:
            card_value = self._face_value(face)
            hand_values = [value + card_value for value in hand_values]
            if face == 'ace' and allow_soft_limit:
                hand_values_ace = [value - 10 for value in hand_values if value < 21]
                hand_values += hand_values_ace
        # Get the higehst value that's 21 or less.  If none found, get the bust value
        hand_values.sort(reverse=True)  # Highest number First
        for value in hand_values:
            hand_value = value
            if hand_value <= 21:  # Found the highest number <= 21
                break
        return hand_value

    def get_dealer_upcard(self):
        """Returns the first Dealer Card as Dealer Up Card"""
        return self.dealer_hand[0]

    def split(self):
        '''Splits the hand into two hands when 2 x wager is less than max and splits allowed'''
        if self.allow_split and len(self.players) == 1 and self.players[0]['active'] and self.max_wager >= (self.players[0]['wager'] * 2):
            if self.allow_dd_after_split and self.players[0]['allow_dd']:
                allow_dd = True
            else:
                self.players[0]['allow_dd'] = False
            player2 = self._init_player(self.players[0]['wager'], allow_dd)
            player2['hand'].append(self.players[0]['hand'].pop())  # Pop Player1 Hand and assign the card to player2
            self.players.append(player2)  # Add Split hand to the Player
            # Pick one more card for both Hands
            self.players[0]['hand'].append(self._pick_card())
            self.players[1]['hand'].append(self._pick_card())
            res = True
        else:
            res = False
        self.allow_split = False  # No more split allowed
        return res

    def double_down(self, hand_idx=0):
        '''Returns True if double down was successful else returns False'''
        wager_required = 0
        for player in self.players:
            wager_required += player['wager']
        wager_required += self.players[hand_idx]['wager']  # Add the wager for current hand again (Double)
        player = self.players[hand_idx]
        if player['allow_dd'] and player['active']:
            if self.max_wager >= wager_required:
                player['wager'] = player['wager'] * 2
            else:
                player['wager'] = self.max_wager  # Double down what ever is remaining
            self.hit(hand_idx)
            self.stand(hand_idx)
            return True
        else:
            return False

    def verify_blackjack(self, hand_idx=0):
        '''Returns True when Player has hit a BlackJack and issues computes game result (via Stand) Else Returns False'''
        if self.player_hand_value(hand_idx) == 21 and len(self.players[hand_idx]['hand']) == 2:
            self.stand(hand_idx)
            return True
        else:
            return False

    def is_bust(self, hand_idx=0):
        """Checks if the Player has bust - Card Count > 21"""
        if self.player_hand_value(hand_idx) > 21:
            return True
        else:
            return False

    def hit(self, hand_idx=0):
        player = self.players[hand_idx]
        if player['active']:
            player['hand'].append(self._pick_card())
        if self.dealer_hand_value() < self.dealer_min:
            self.dealer_hand.append(self._pick_card())
        if self.is_bust(hand_idx):
            self.stand(hand_idx)  # Force Stand and compute game result
        # Turn Off Split and Double Down after the first hit
        if player['allow_dd']:  # Don't allow double down after the first hit
            player['allow_dd'] = False
        if self.allow_split:  # Don't allow split after the first hit
            self.allow_split = False

    def player_hand_value(self, hand_idx=0):
        return self._get_hand_value(self.players[hand_idx]['hand'])

    def dealer_hand_value(self):
        return self._get_hand_value(self.dealer_hand, allow_soft_limit=self.allow_soft_limit)

    def stand(self, hand_idx=0):
        dealer_value = self.dealer_hand_value()
        # Dealer has to hit until it's atleast Dealer Min (Default 17)
        while dealer_value < self.dealer_min:
            self.dealer_hand.append(self._pick_card())
            dealer_value = self.dealer_hand_value()
        #Compute Player Hand value
        player = self.players[hand_idx]
        player_value = self.player_hand_value(hand_idx)
        if player['active']:
            # When Player has Blackjack in 2 cards and dealer doesn't
            if player_value == 21 and len(player['hand']) == 2 and \
                    (dealer_value != 21 or (dealer_value == 21 and len(self.dealer_hand) > 2)):
                    player['result'] = 'blackjack'
                    self.wager_earned += 1.5 * player['wager']
            # When Both Player and Dealer values are equal or both are Bust, then "Push".
            elif player_value == dealer_value or (player_value > 21 and dealer_value > 21):
                player['result'] = 'push'
            # When Only Player is Bust, then "Bust". You lost the wager
            elif player_value > 21:
                player['result'] = 'bust'
                self.wager_earned -= player['wager']
            # When Only Dealer is Bust, then "Won".  You won the wager
            elif dealer_value > 21:
                player['result'] = 'won'
                self.wager_earned += player['wager']
            # When both Player and delaer are not bust and Player has higher number than Dealer
            elif player_value > dealer_value:
                player['result'] = 'won'
                self.wager_earned += player['wager']
            # When both Player and delaer are not bust and Player has lower number than Dealer
            elif dealer_value > player_value:
                player['result'] = 'lost'
                self.wager_earned -= player['wager']
            player['active'] = False  # Set Player Hand Active to False after a Stand
        return None
