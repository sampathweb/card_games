BlackJack:
=========
The Objective of the game is to get to 21 or close to it without exceeding 21.  You are playing solely against the dealer or also called the House.

How to Run:
----------
If you have python installed, you can run from command line as:

`python play_blackjack.py`

By default, you are given 100 wager credits.  If you want more credits, run the program with credits you need.  For example:

`python play_blackjack.py 200`  will give you 200 credits.

The credits needs to be numeric.  If you give a invalid input, you will be given the default 100 wager credit.

To Run Tests and verify that it passes the pre-determined test conditions, just run:

`python test_blackjack.py`

This app uses standard python modules and has no external libraries.  It has been tested with both Python 2.7 and Python 3.4.


Card Couting:
------------
* Each Card 2-10 is valued at its face value.
* Jack, Queen and King are valued at 10.
* Ace can be counted as 1 or a 11 depending on which number gets you closer to 21 without exceeding it.

Game Rules:
----------
You are awarded a set Wager Credits.  play_blackjack gives you 100 wager credits but you can change it by passing the credits you want in the input.  You can continue to play the game as long as have atleast 1 wager credit available.

At the start of each round, you specify how much you want to wager.

* Hitting 21 exactly in the first 2 cards is called "BlackJack".  For example (Ace, 10) or (Ace, King) (Ace, Queen) or (Ace, Jack).  You get 1.5 times the wager when you hit blackjack.
* You can draw as many cards as you want.  But if your card count goes over 21, you are 'bust' and loose the wager
* You can Split and play both hands - one after the another.
* You can double down on your hand.  You can also double down after you split on any one or both hands.

If you beat the dealer on the card count, you win and earn the wager.  If you loose you pay the wager to the dealer.  The dealer has to draw cards (or hit) until he meets or exceeds 17 (can be changed).  At that point dealer stops to draw any more cards.


Game Settings:
-------------
While initailizing the game via BlackJack class, you will be able to:

* Set Wager, Maximum Wager.  By default both are 1.
* Specify if Splits and Doubledowns are allowed.  By default Split and Doubledowns are allowed.
* Specify if Doubledown after a Split is allowed.  By default, it is allowed.
* Specify Doubledown maximums.  By default it's 21, but you can specify something less to favor the House.
* Specify if Dealer minimum.  By default it's 17.
* Specify if the dealer limit is soft.  By default, it's not.
