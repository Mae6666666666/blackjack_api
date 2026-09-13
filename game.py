"""
Blackjack game logic. No web code in here -- just the rules.

A card is written as a suit letter + a deck index, matching the images in
static/deck/. The index runs 0-12, so it is one behind the card it stands for:

    d0  = ace of diamonds     -> 1 or 11
    d2  = 3 of diamonds       -> 3
    d9  = 10 of diamonds      -> 10
    d10 = jack                -> 10
    d11 = queen               -> 10
    d12 = king                -> 10

An ace counts 11 whenever that keeps the hand at 21 or under, otherwise 1.
"""

import random


# --- Card values and totals -------------------------------------------------

def card_value(card):
    """The value of one card, counting an ace as 1."""
    index = int(card[1:])
    value = index + 1
    return min(value, 10)


def total_calc(hand):
    """The best total for a hand, counting one ace as 11 if it fits."""
    total = 0
    has_ace = False
    for card in hand:
        value = card_value(card)
        if value == 1:
            has_ace = True
        total += value

    # Only one ace can ever be 11 -- two would already be 22.
    if has_ace and total + 10 <= 21:
        total += 10
    return total


# --- Checking hands ---------------------------------------------------------

def is_bust(hand):
    """True if the hand is over 21."""
    return total_calc(hand) > 21


def is_blackjack(hand):
    """True if the hand is an ace and a ten-value card, and nothing else."""
    return len(hand) == 2 and total_calc(hand) == 21


def compare_hands(dealer_hand, player_hand):
    """Which total is higher: "Dealer", "Player" or "Draw". Ignores busts."""
    dealer_total = total_calc(dealer_hand)
    player_total = total_calc(player_hand)
    if dealer_total > player_total:
        return "Dealer"
    if dealer_total == player_total:
        return "Draw"
    return "Player"


# --- The deck ---------------------------------------------------------------

SUITS = ["h", "d", "s", "c"]


def build_deck():
    """A full 52-card deck, in order."""
    deck = []
    for index in range(13):
        for suit in SUITS:
            deck.append(suit + str(index))
    return deck


def deal_card(deck):
    """Take the top card off the deck and return it. The deck gets shorter."""
    return deck.pop(0)


def deal_hand(deck, number):
    """Deal `number` cards off the top of the deck."""
    hand = []
    for _ in range(number):
        hand.append(deal_card(deck))
    return hand


def shuffle(deck):
    """A shuffled copy of the deck. The original is left alone."""
    shuffled = list(deck)
    random.shuffle(shuffled)
    return shuffled


# --- The dealer and the result ----------------------------------------------

def dealer_should_hit(hand):
    """The dealer takes a card under 17 and stands on 17 or more."""
    return total_calc(hand) < 17


def play_dealer_turn(deck, hand):
    """Keep dealing the dealer cards until they reach 17. Returns the hand."""
    while dealer_should_hit(hand):
        hand.append(deal_card(deck))
    return hand


def who_wins(dealer_hand, player_hand):
    """The result of a finished round: "Dealer", "Player" or "Draw"."""
    # The player plays first, so a player who busts has lost before the
    # dealer even starts -- even if the dealer busts too.
    if is_bust(player_hand):
        return "Dealer"
    if is_bust(dealer_hand):
        return "Player"

    # A blackjack beats any other 21. Two blackjacks draw.
    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)
    if player_blackjack and not dealer_blackjack:
        return "Player"
    if dealer_blackjack and not player_blackjack:
        return "Dealer"

    return compare_hands(dealer_hand, player_hand)
