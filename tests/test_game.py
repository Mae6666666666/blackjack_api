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
