#!/usr/bin/env python
"""
Test code for blackjack game.  Test can be run from command line: python test_blackjack.py

Due to the randomness of the cards drawn, many of the runs try multiple times to hit the test condition and avoid 'BlackJack'.
"""
from __future__ import print_function
import unittest
from blackjack import BlackJack


class TestRule(unittest.TestCase):

    def setUp(self):
        self.run_max = 100000  # Max attempts for each test
        self.test_ran = False

    def tearDown(self):
        self.assertTrue(self.test_ran)  # Verify that test ran

    def test_init(self):
        mygame = BlackJack()  # Default Initialization
        self.assertEqual(len(mygame.players), 1)  # Assert only one player playing before split
        self.assertEqual(len(mygame.players[0]['hand']), 2)  # Initial hand for Player
        self.test_ran = True

    def test_hit(self):
        for run in range(self.run_max):
            mygame = BlackJack()
            if not mygame.verify_blackjack():  # Not a BlackJack
                mygame.hit()
                self.assertEqual(len(mygame.players[0]['hand']), 3)  # Three cards in Player's hand
                self.test_ran = True
                break

    def test_split(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=1, max_wager=2)
            if mygame.player_hand_value() != 21:
                mygame.split()
                self.assertEqual(len(mygame.players), 2)  # Two Hands Played by Player
                self.assertEqual(len(mygame.players[0]['hand']), 2)
                self.assertEqual(len(mygame.players[1]['hand']), 2)
                self.test_ran = True
                break

    def test_split_not_allowed_blackjack(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=1, max_wager=2)
            if mygame.verify_blackjack():
                # Split should not be possible when blackjack
                self.assertFalse(mygame.split())
                self.assertEqual(len(mygame.players), 1)
                self.assertIn(mygame.players[0]['result'], ['blackjack', 'push'])
                self.test_ran = True
                break

    def test_split_not_allowed(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=1, max_wager=100, allow_split=False)
            if not mygame.verify_blackjack():  # Not a BlackJack
                mygame.split()
                self.assertEqual(len(mygame.players), 1)  # Only Hand Played. Since split not allowed
                self.assertEqual(len(mygame.players[0]['hand']), 2)
                self.test_ran = True
                break

    def test_split_not_enough_wager(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=1, max_wager=1)
            if not mygame.verify_blackjack():  # Not a BlackJack
                mygame.split()
                self.assertEqual(len(mygame.players), 1)  # Only Hand Played. Since not enough wager
                self.assertEqual(len(mygame.players[0]['hand']), 2)
                self.test_ran = True
                break

    def test_double_down(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=5, max_wager=100)  # Double down allowed by default
            if mygame.player_hand_value() != 21:
                mygame.double_down()
                self.assertEqual(mygame.players[0]['wager'], 10)  # Double down Succeeded
                self.assertFalse(mygame.players[0]['active'])  # Assert that game is not active
                self.test_ran = True
                break

    def test_double_down_not_allowed_blackjack(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=5, max_wager=100)  # Double down allowed by default
            if mygame.player_hand_value() == 21:
                # Doubledown should not be possible when blackjack
                self.assertFalse(mygame.double_down())
                self.assertEqual(len(mygame.players), 1)
                self.assertIn(mygame.players[0]['result'], ['blackjack', 'push'])
                self.test_ran = True
                break

    def test_double_down_not_allowed(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=5, max_wager=100, allow_dd=False)
            if mygame.player_hand_value() != 21:
                mygame.double_down()
                self.assertEqual(mygame.players[0]['wager'], 5)  # Did not double down
                self.test_ran = True
                break

    def test_double_down_not_enough_wager(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=5, max_wager=9, allow_dd=True)
            if mygame.player_hand_value() != 21:
                mygame.double_down()
                self.assertEqual(mygame.players[0]['wager'], 9)  # Double Down to Max Value
                self.test_ran = True
                break

    def test_double_down_after_split(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=5, max_wager=100)  # Double down & Split allowed by default
            if mygame.player_hand_value() != 21:
                mygame.split()
                # Double down one hand
                mygame.double_down(hand_idx=0)
                self.assertEqual(mygame.players[0]['wager'], 10)
                self.assertEqual(mygame.players[1]['wager'], 5)
                self.test_ran = True
                break

    def test_player_blackjack1(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=10, max_wager=12)
            player = mygame.players[0]
            if mygame.player_hand_value() == 21 and mygame.dealer_hand_value() != 21:
                self.assertEqual(player['result'], 'blackjack')
                self.assertEqual(mygame.wager_earned, 1.5 * player['wager'])
                self.test_ran = True
                break

    def test_player_blackjack2(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=10, max_wager=12)
            player = mygame.players[0]
            if mygame.player_hand_value() == 21 and mygame.dealer_hand_value() == 21 and len(mygame.dealer_hand) > 2:
                self.assertEqual(player['result'], 'blackjack')
                self.assertEqual(mygame.wager_earned, 1.5 * player['wager'])
                self.test_ran = True
                break

    def test_player_bust(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=10, max_wager=12)
            if not mygame.verify_blackjack():  # Not a BlackJack
                for cnt in range(10):  # Draw 10 cards - Sure to loose
                    mygame.hit()
                mygame.stand()  # Stand to verify that you got busted when you pull 12 cards
                if mygame.dealer_hand_value() <= 21:
                    self.assertEqual(mygame.players[0]['result'], 'bust')  # Definitely a bust
                    self.assertEqual(mygame.wager_earned, -10)  # bust
                    self.test_ran = True
                    break

    def test_player_and_dealer_bust(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=10, max_wager=12)
            if not mygame.verify_blackjack():  # Not a BlackJack
                for cnt in range(10):  # Draw 10 cards - Sure to loose
                    mygame.hit(hand_idx=0)
                mygame.stand()  # Stand to verify that you got busted when you pull 12 cards
                if mygame.dealer_hand_value() > 21:
                    self.assertEqual(mygame.players[0]['result'], 'push')  # Both bust, so a Push
                    self.assertEqual(mygame.wager_earned, 0)  # Both bust
                    self.test_ran = True
                    break

    def test_player_push(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=10, max_wager=12)
            if not mygame.verify_blackjack():  # Not a BlackJack
                while mygame.player_hand_value() < 12 and mygame.players[0]['active']:
                    mygame.hit()
                mygame.stand()
                if mygame.player_hand_value() == mygame.dealer_hand_value():
                    self.assertEqual(mygame.players[0]['result'], 'push')
                    self.assertEqual(mygame.wager_earned, 0)
                    self.test_ran = True
                    break

    def test_player_won(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=10, max_wager=12)
            while mygame.player_hand_value() < 12 and mygame.players[0]['active']:
                mygame.hit()
            mygame.stand()
            player_hand_value = mygame.player_hand_value(hand_idx=0)
            # When player hand is < 21, but > Dealer hand and it's not blackjack, player wins
            if player_hand_value <= 21 and \
                    player_hand_value > mygame.dealer_hand_value() and \
                    len(mygame.players[0]['hand']) > 2:
                self.assertEqual(mygame.players[0]['result'], 'won')
                self.assertEqual(mygame.wager_earned, mygame.players[0]['wager'])
                self.test_ran = True
                break

    def test_player_lost(self):
        for run in range(self.run_max):
            mygame = BlackJack(wager=10, max_wager=12)
            while mygame.player_hand_value() < 12 and mygame.players[0]['active']:
                mygame.hit()
            mygame.stand()
            if mygame.player_hand_value() <= 21 and \
                    mygame.dealer_hand_value() <= 21 and \
                    mygame.player_hand_value() < mygame.dealer_hand_value():
                self.assertEqual(mygame.players[0]['result'], 'lost')
                self.assertEqual(mygame.wager_earned, -1 * mygame.players[0]['wager'])
                self.test_ran = True
                break

if __name__ == '__main__':
    unittest.main()
