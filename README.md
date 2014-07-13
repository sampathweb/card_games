Card Games:
==========
This package acts as the container for various card games.



BlackJack:  You will be the Player and system acts as the Dealer.
=========
The Objective of the game is to get to 21 or close to it without exceeding 21.
You are playing solely against the dealer or also called the House.
You can draw as many cards as you want.  But if your card count goes over 21, you are 'bust' and loose the wager

Hitting 21 exactly in the first 2 cards is called "BlackJack".  For example (Ace, 10) or (Ace, King) (Ace, Queen) or (Ace, Jack)

Card Couting:
------------
Each Card 2-10 is valued at its face value.
Jack, Queen and King are valued at 10.
Ace can be counted as 1 or a 11 depending on which number gets you closer to 21 without exceeding it.

How to Win:
----------
If you beat the dealer on the card count, you will and earn the wager.  If you loose you pay the wager to the dealer.
The dealer has to draw cards (or hit) until he meets or exceeds 17 (can be changed).  At that point dealer stops to draw any more cards.

Game Settings:
-------------
While initailizing the game via BlackJack class, you will be able to:
a. Set Wager, Maximum Wager.  By default both are 1.
b. Specify if Splits and Doubledowns are allowed.  By Default Split and Doubledowns are allowed.
c. Specify Doubledown maximums.  By default it's 21, but you can specify something less to favor the House.
c. Specify if Dealer minimum.  By Default it's 17.
d. Specify if the dealer limit is soft.  By Default, it's not.
