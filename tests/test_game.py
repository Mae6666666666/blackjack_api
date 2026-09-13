import game


# --- card_value -------------------------------------------------------------

def test_card_value_number_card_is_one_more_than_its_index():
    assert game.card_value("d2") == 3


def test_card_value_ten_is_ten():
    assert game.card_value("d9") == 10


def test_card_value_jack_queen_and_king_are_ten():
    assert game.card_value("d10") == 10
    assert game.card_value("d11") == 10
    assert game.card_value("d12") == 10


def test_card_value_ace_counts_as_one_on_its_own():
    assert game.card_value("d0") == 1


# --- total_calc -------------------------------------------------------------

def test_total_calc_adds_two_cards():
    assert game.total_calc(["d2", "d8"]) == 12


def test_total_calc_adds_every_card_in_the_hand():
    assert game.total_calc(["d2", "s11", "h4"]) == 18


def test_total_calc_ace_is_11_when_it_fits():
    assert game.total_calc(["d0", "d10"]) == 21


def test_total_calc_ace_is_1_when_11_would_bust():
    assert game.total_calc(["d0", "d10", "h10"]) == 21


def test_total_calc_empty_hand_is_worth_nothing():
    assert game.total_calc([]) == 0


def test_total_calc_lone_ace_is_11():
    assert game.total_calc(["d0"]) == 11


def test_total_calc_two_aces_are_11_plus_1():
    assert game.total_calc(["d0", "s0"]) == 12


def test_total_calc_three_aces_are_11_plus_1_plus_1():
    assert game.total_calc(["d0", "s0", "h0"]) == 13


def test_total_calc_ace_drops_to_1_when_a_later_card_would_bust():
    # ace + 6 is a soft 17, then the 10 would make 27, so the ace becomes 1.
    assert game.total_calc(["d0", "d5", "d9"]) == 17


def test_total_calc_card_order_does_not_matter():
    assert game.total_calc(["d9", "d5", "d0"]) == 17


def test_total_calc_face_cards_are_all_10():
    assert game.total_calc(["d10", "d11", "d12"]) == 30


def test_total_calc_suit_makes_no_difference():
    assert game.total_calc(["c3", "h3"]) == game.total_calc(["d3", "s3"])


def test_total_calc_hand_with_no_ace_can_go_bust():
    assert game.total_calc(["d9", "h9", "s4"]) == 25


# --- is_bust ----------------------------------------------------------------

def test_is_bust_over_21_is_bust():
    assert game.is_bust(["d9", "h9", "s4"]) is True  # 25


def test_is_bust_20_is_not_bust():
    assert game.is_bust(["d9", "h9"]) is False


def test_is_bust_exactly_21_is_not_bust():
    assert game.is_bust(["d9", "h9", "s0"]) is False  # ace counts as 1


def test_is_bust_22_is_bust():
    assert game.is_bust(["d9", "h9", "s1"]) is True


def test_is_bust_small_hand_is_not_bust():
    assert game.is_bust(["d2", "h1"]) is False  # 5


# --- is_blackjack -----------------------------------------------------------

def test_is_blackjack_ten_then_ace():
    assert game.is_blackjack(["d9", "h0"]) is True


def test_is_blackjack_ace_then_ten():
    assert game.is_blackjack(["h0", "h9"]) is True


def test_is_blackjack_ace_with_jack_queen_or_king():
    assert game.is_blackjack(["h0", "c10"]) is True
    assert game.is_blackjack(["h0", "s11"]) is True
    assert game.is_blackjack(["h0", "s12"]) is True


def test_is_blackjack_21_from_three_cards_is_not_blackjack():
    assert game.is_blackjack(["h1", "s8", "s9"]) is False  # 2 + 9 + 10


def test_is_blackjack_two_cards_under_21_is_not_blackjack():
    assert game.is_blackjack(["h5", "s7"]) is False  # 14


# --- compare_hands ----------------------------------------------------------

def test_compare_hands_dealer_higher():
    assert game.compare_hands(["h5", "s7"], ["h2", "d2"]) == "Dealer"


def test_compare_hands_same_total_is_a_draw():
    assert game.compare_hands(["h5", "s7"], ["c5", "d7"]) == "Draw"


def test_compare_hands_player_higher():
    assert game.compare_hands(["h5", "s7"], ["h0", "d9"]) == "Player"


# --- build_deck -------------------------------------------------------------

def test_build_deck_has_52_cards():
    assert len(game.build_deck()) == 52


def test_build_deck_contains_the_ace_of_diamonds():
    assert "d0" in game.build_deck()


def test_build_deck_has_13_of_each_suit():
    deck = game.build_deck()
    for suit in ["h", "d", "s", "c"]:
        assert len([card for card in deck if card[0] == suit]) == 13


def test_build_deck_has_no_repeated_cards():
    deck = game.build_deck()
    assert len(set(deck)) == 52


# --- deal_card --------------------------------------------------------------

def test_deal_card_takes_the_top_card():
    assert game.deal_card(["h0", "h1", "h2"]) == "h0"


def test_deal_card_takes_the_top_card_of_a_different_deck():
    assert game.deal_card(["s5", "d2"]) == "s5"


def test_deal_card_removes_the_card_from_the_deck():
    deck = ["h0", "h1", "h2"]
    game.deal_card(deck)
    assert deck == ["h1", "h2"]


# --- deal_hand --------------------------------------------------------------

def test_deal_hand_deals_the_number_asked_for():
    assert len(game.deal_hand(["h0", "h1", "h2", "h3"], 2)) == 2
    assert len(game.deal_hand(["h0", "h1", "h2", "h3"], 3)) == 3


def test_deal_hand_removes_the_dealt_cards_from_the_deck():
    deck = ["h0", "h1", "h2", "h3"]
    game.deal_hand(deck, 2)
    assert deck == ["h2", "h3"]


def test_deal_hand_deals_from_the_top():
    assert game.deal_hand(["h0", "h1", "h2", "h3"], 2) == ["h0", "h1"]


# --- shuffle ----------------------------------------------------------------

def test_shuffle_keeps_52_cards():
    assert len(game.shuffle(game.build_deck())) == 52


def test_shuffle_changes_the_order():
    # Could in theory come back in order -- about a 1 in 10^67 chance.
    assert game.shuffle(game.build_deck()) != game.build_deck()


def test_shuffle_keeps_exactly_the_same_cards():
    assert sorted(game.shuffle(game.build_deck())) == sorted(game.build_deck())


def test_shuffle_works_on_a_small_deck():
    assert sorted(game.shuffle(["h0", "h1", "h2"])) == ["h0", "h1", "h2"]


def test_shuffle_leaves_the_original_deck_alone():
    deck = game.build_deck()
    game.shuffle(deck)
    assert deck == game.build_deck()
