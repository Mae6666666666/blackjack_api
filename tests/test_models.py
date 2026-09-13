"""
Mae -- your first job: write the GameState model in models.py.

Read the explanation at the top of models.py first, and look at how
HealthResponse is written. GameState works the same way, just with more fields.

GameState is what every /games endpoint will send back. It needs these fields:

    id            a string       -- which game this is
    player_hand   a list of str  -- the player's cards, e.g. ["h9", "h5"]
    dealer_hand   a list of str  -- the dealer's cards
    player_total  an int         -- the player's hand total
    dealer_total  an int         -- the dealer's hand total
    status        a string       -- "player_turn" or "finished"
    result        a string, or None -- "Player", "Dealer" or "Draw" once the
                                       round is over; None until then.

Hints for the types: a list of strings is written  list[str]
                     "a string or None" is written  str | None

Work through these tests in order. When one goes green, delete the
@pytest.mark.skip line above the next one.
"""


def test_game_state_keeps_the_values_it_is_given():
    from models import GameState

    state = GameState(
        id="abc",
        player_hand=["h9", "h5"],
        dealer_hand=["d9", "d6"],
        player_total=16,
        dealer_total=17,
        status="player_turn",
        result=None,
    )
    assert state.id == "abc"
    assert state.player_hand == ["h9", "h5"]
    assert state.dealer_hand == ["d9", "d6"]
    assert state.player_total == 16
    assert state.dealer_total == 17
    assert state.status == "player_turn"
    assert state.result is None



def test_game_state_result_is_none_if_you_leave_it_out():
    from models import GameState

    state = GameState(
        id="abc",
        player_hand=["h9", "h5"],
        dealer_hand=["d9", "d6"],
        player_total=16,
        dealer_total=17,
        status="player_turn",
    )
    assert state.result is None


def test_game_state_player_total_must_be_a_number():
    from models import GameState

    # Run this and read the red error: pydantic refuses "sixteen" because
    # player_total is an int. Then change "sixteen" to 16 to make it green.
    state = GameState(
        id="abc",
        player_hand=["h9", "h5"],
        dealer_hand=["d9", "d6"],
        player_total=16,
        dealer_total=17,
        status="player_turn",
    )
    assert state.player_total == 16
