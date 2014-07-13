#!/usr/bin/env python
"""
A package to wrap the rules of BlackJack.
"""
from __future__ import print_function
import random


class BlackJack(object):

    def __init__(self, wager=1, max_wager=1, dealer_min=17, allow_soft_limit=True, allow_split=True, allow_double_down=True, level=0):
        """Returns None.  Initiailizes the Game with rules, wager limits and draws the initial set of two cards for player and dealer"""
        self.wager = wager
        self.max_wager = max_wager
        self.dealer_min = dealer_min
        self.allow_soft_limit = allow_soft_limit
        self.allow_split = allow_split
        self.allow_double_down = allow_double_down
        self.level = level
        self.card_suits = ['spade', 'heart', 'diamond', 'club']
        self.card_faces = {str(numb): numb for numb in range(2, 11)}
        for face in ('jack', 'king', 'queen'):
            self.card_faces[face] = 10
        self.card_faces['ace'] = 11
        # Set the player hand, Dealer hand
        self.player_hands = []
        self.player_hands.append([])  # Assume One Player Hand (No Split)
        self.dealer_hand = []
        self.result = None
        self.wager_earned = 0
        self.card_deck = [(face, suit) for suit in self.card_suits for face in self.card_faces.keys()]
        random.shuffle(self.card_deck)  # Shuffle the card deck
        # Draw two cards for Player and Dealer
        self.player_hands[0].append(self._pick_card())
        self.player_hands[0].append(self._pick_card())
        self.dealer_hand.append(self._pick_card())
        self.dealer_hand.append(self._pick_card())
        return None

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

    def split(self):
        if self.allow_split and self.max_wager >= (self.wager * 2):
            self.allow_split = False
            card2 = self.player_hands[0].pop()  # Unpack the player hand
            self.player_hands.append([card2])  # Add Split hand to the Player
            self.player_hands[0].append(self._pick_card())
            self.player_hands[1].append(self._pick_card())
            return True
        else:
            return False

    def double_down(self):
        '''Returns True if double down was successful else returns False'''
        wager_required = self.wager * 2 * len(self.player_hands)  # Take splits into account
        if self.allow_double_down and self.max_wager >= wager_required:
            self.wager = self.wager * 2
            return True
        else:
            return False

    def hit(self):
        for player_hand in self.player_hands:
            player_hand.append(self._pick_card())
        if self.dealer_hand_value() < self.dealer_min:
            self.dealer_hand.append(self._pick_card())
        # Turn Off Split and Double Down after the first hit
        if self.allow_double_down:  # Don't allow double down after the first hit
            self.allow_double_down = False
        if self.allow_split:  # Don't allow split after the first hit
            self.allow_split = False

    def player_hands_value(self):
        hands_value = []
        for player_hand in self.player_hands:
            hands_value.append(self._get_hand_value(player_hand))
        return tuple(hands_value)

    def dealer_hand_value(self):
        return self._get_hand_value(self.dealer_hand, allow_soft_limit=self.allow_soft_limit)

    def stand(self):
        dealer_value = self.dealer_hand_value()
        player_values = self.player_hands_value()
        self.game_result = []
        for player_value in player_values:
            if player_value > 21:
                self.game_result.append('bust')
                self.wager_earned -= self.wager
            elif dealer_value > 21:
                self.game_result.append('won')
                self.wager_earned += self.wager
            elif player_value > dealer_value:
                self.game_result.append('won')
                self.wager_earned += self.wager
            elif dealer_value > player_value:
                self.game_result.append('lost')
                self.wager_earned -= self.wager
            elif player_value == dealer_value:
                self.game_result.append('push')
            else:
                self.game_result.append(None)
        return self.game_result
