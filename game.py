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
