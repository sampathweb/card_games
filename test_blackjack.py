#!/usr/bin/env python
"""
Test code for blackjack game.  Tests can be run with py.test or nosetests.
"""
from __future__ import print_function
import unittest
from blackjack import BlackJack


class TestRule(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_init(self):
        mygame = BlackJack()
        self.assertEqual(len(mygame.player_hands[0]), 2)  # Initial hand for Player
        self.assertEqual(len(mygame.dealer_hand), 2)  # Initial hand for Dealer

    def test_player_hit(self):
        mygame = BlackJack()
        mygame.hit()
        self.assertEqual(len(mygame.player_hands[0]), 3)  # Three cards in Player's hand

    def test_player_split(self):
        mygame = BlackJack(wager=1, max_wager=2)
        mygame.split()
        self.assertEqual(len(mygame.player_hands), 2)  # Two Hands Played by Player

    def test_player_split_not_enough_wager(self):
        mygame = BlackJack(wager=1, max_wager=1)
        mygame.split()
        self.assertEqual(len(mygame.player_hands), 1)  # Only Hand Played. Since not enough wager
        self.assertEqual(len(mygame.player_hands[0]), 2)

    def test_player_split_not_allowed(self):
        mygame = BlackJack(wager=1, max_wager=100, allow_split=False)
        mygame.split()
        self.assertEqual(len(mygame.player_hands), 1)  # Only Hand Played. Since split not allowed
        self.assertEqual(len(mygame.player_hands[0]), 2)

    def test_player_double_down(self):
        mygame = BlackJack(wager=5, max_wager=100)  # Double down allowed by default
        mygame.double_down()
        self.assertEqual(mygame.wager, 10)  # Double down Succeeded
        # Now, bust to verify that double down of wager is good
        for cnt in range(15):  # Draw 15 cards - Sure to loose
            mygame.hit()
        mygame.stand()
        self.assertEqual(mygame.wager_earned, -10)  # Lost the double down wager

    def test_player_double_down_split(self):
        mygame = BlackJack(wager=5, max_wager=100)  # Double down & Split allowed by default
        mygame.double_down()
        self.assertEqual(mygame.wager, 10)  # Double down Succeeded
        mygame.split()
        # Now, bust to verify that double down then Split worked
        for cnt in range(15):  # Draw 15 cards - Sure to loose
            mygame.hit()
        mygame.stand()
        self.assertEqual(mygame.wager_earned, -20)  # Lost the double down / Split wager

    def test_player_split_double_down(self):
        mygame = BlackJack(wager=5, max_wager=100)  # Double down & Split allowed by default
        mygame.split()
        self.assertEqual(len(mygame.player_hands), 2)  # Split Succeeded
        mygame.double_down()
        self.assertEqual(mygame.wager, 10)  # Double down Succeeded
        # Now, bust to verify that Split then double down worked
        for cnt in range(15):  # Draw 15 cards - Sure to loose
            mygame.hit()
        mygame.stand()
        self.assertEqual(mygame.wager_earned, -20)  # Lost the double down / Split wager

    def test_player_double_down_not_allowed(self):
        mygame = BlackJack(wager=5, max_wager=100, allow_double_down=False)
        mygame.double_down()
        self.assertEqual(mygame.wager, 5)  # Did not double down
        # Now, bust to verify that double down did not reduce wager twice
        for cnt in range(15):  # Draw 15 cards - Sure to loose
            mygame.hit()
        mygame.stand()
        self.assertEqual(mygame.wager_earned, -5)  # Original wager lost, not double down

    def test_player_double_down_not_enough_wager(self):
        mygame = BlackJack(wager=5, max_wager=9, allow_double_down=True)
        mygame.double_down()
        self.assertEqual(mygame.wager, 5)  # Did not double down
        # Now, bust to verify that double down did not reduce wager twice
        for cnt in range(15):  # Draw 15 cards - Sure to loose
            mygame.hit()
        mygame.stand()
        self.assertEqual(mygame.wager_earned, -5)  # Original wager lost, not double down

    def test_player_bust(self):
        mygame = BlackJack(wager=10, max_wager=12)
        for cnt in range(10):  # Draw 10 cards - Sure to loose
            mygame.hit()
        self.assertEqual(len(mygame.player_hands[0]), 12)  # Twelve cards in Player's hand
        mygame.stand()  # Stand to verify that you got busted when you pull 12 cards
        self.assertEqual(mygame.game_result[0], 'bust')  # Definitely a bust
        self.assertEqual(mygame.wager_earned, -10)  # Lost the wager

    def test_player_win(self):
        for cnt in range(100):  # Try 100 Times
            mygame = BlackJack(wager=10, max_wager=12)
            while mygame.player_hands_value()[0] < 12:
                mygame.hit()
            mygame.stand()
            if (mygame.player_hands_value()[0] <= 21 and mygame.player_hands_value()[0] > mygame.dealer_hand_value()) or \
                    (mygame.player_hands_value()[0] > 21 and mygame.player_hands_value()[0] < mygame.dealer_hand_value()):
                self.assertEqual(mygame.game_result[0], 'won')
                self.assertEqual(mygame.wager_earned, mygame.wager)

    def test_player_push(self):
        for cnt in range(100):  # Try 100 Times because cards are drawn at random and favorable cards may not occur all times
            mygame = BlackJack(wager=10, max_wager=12)
            while mygame.player_hands_value()[0] < 12:
                mygame.hit()
            mygame.stand()
            if mygame.player_hands_value()[0] == mygame.dealer_hand_value():
                self.assertEqual(mygame.game_result[0], 'push')
                self.assertEqual(mygame.wager_earned, 0)

    def test_player_lost(self):
        for cnt in range(100):  # Try 100 Times because cards are drawn at random and favorable cards may not occur all times
            mygame = BlackJack(wager=10, max_wager=12)
            while mygame.player_hands_value()[0] < 12:
                mygame.hit()
            mygame.stand()
            if mygame.player_hands_value()[0] <= 21 and \
                    mygame.dealer_hand_value() <= 21 and \
                    mygame.player_hands_value()[0] < mygame.dealer_hand_value():
                self.assertEqual(mygame.game_result[0], 'lost')
                self.assertEqual(mygame.wager_earned, -1 * mygame.wager)

if __name__ == '__main__':
    unittest.main()
