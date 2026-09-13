"""
Tests for the API endpoints. These talk to the app over HTTP, the same way a
web page would, so they only care about what goes in and what comes back.
"""

import pytest


# --- GET /health -- the worked example --------------------------------------
#
# Read this one first. It is complete and passing.
#
#   client.get("/health")   sends a GET request, like typing the URL in a browser
#   response.status_code    the HTTP status: 200 means OK, 404 means not found
#   response.json()         the body of the response, turned into a Python dict

def test_health_responds_with_200(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_says_ok(client):
    response = client.get("/health")
    assert response.json() == {"status": "ok"}


# --- GET / -- the web page ---------------------------------------------------

def test_home_page_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


# ============================================================================
# Mae -- your endpoints start here.
#
# Do tests/test_models.py first, so GameState exists. Then work down this file
# one test at a time: when a test goes green, delete the @pytest.mark.skip line
# above the next one.
#
# The work comes in rounds. Each round builds one endpoint, then you connect it
# to the web page in static/app.js and try it in the browser before moving on.
#
# Every /games endpoint sends back a GameState. Build it from a Game (see
# game.py) plus the game's id, and work the totals out with total_calc.
#
# Most tests call use_deck(...) first, so the cards are always the same. Your
# endpoints don't need to know about that -- just get a new deck by calling
# make_deck(), and the tests handle the rest.
# ============================================================================

# Player gets h9 + h5 = 16. Dealer gets d9 + d6 = 17. The next card is c2 (a 3).
DECK = ["h9", "h5", "d9", "d6", "c2", "s8", "c9", "d3"]

# Player gets h1 + h2 = 5, so two hits (c2 then c3) still leave them on 12.
TWO_HITS_DECK = ["h1", "h2", "d9", "d6", "c2", "c3", "s8"]

# Player gets 16, and the next card is s9 (a 10) -- a hit goes bust.
PLAYER_BUSTS_DECK = ["h9", "h5", "d9", "d6", "s9", "c2"]

# Dealer gets d9 + d4 = 15, so on a stand they take c3 (a 4) and stop on 19.
DEALER_HITS_DECK = ["h9", "h8", "d9", "d4", "c3", "c9"]

# Player gets ace + king: blackjack straight away.
PLAYER_BLACKJACK_DECK = ["h0", "h12", "d9", "d6", "c2", "s8"]


# ============================================================================
# ROUND 1 -- Deal.  POST /games starts a new game.
# ============================================================================


def test_new_game_responds_with_200(client, use_deck):
    use_deck(DECK)
    response = client.post("/games")
    assert response.status_code == 200


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_new_game_gives_back_an_id(client, use_deck):
    use_deck(DECK)
    body = client.post("/games").json()
    assert isinstance(body["id"], str)
    assert body["id"] != ""


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_new_game_deals_the_player_the_top_two_cards(client, use_deck):
    use_deck(DECK)
    body = client.post("/games").json()
    assert body["player_hand"] == ["h9", "h5"]


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_new_game_deals_the_dealer_the_next_two_cards(client, use_deck):
    use_deck(DECK)
    body = client.post("/games").json()
    assert body["dealer_hand"] == ["d9", "d6"]


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_new_game_sends_both_totals(client, use_deck):
    use_deck(DECK)
    body = client.post("/games").json()
    assert body["player_total"] == 16
    assert body["dealer_total"] == 17


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_new_game_is_the_players_turn(client, use_deck):
    use_deck(DECK)
    body = client.post("/games").json()
    assert body["status"] == "player_turn"
    assert body["result"] is None


# STOP. Round 1's endpoint is done. Go to static/app.js, do ROUND 1 there, and
# check the Deal button works in the browser before carrying on.


# ============================================================================
# ROUND 2 -- Hit.  POST /games/{game_id}/hit gives the player a card.
# ============================================================================

@pytest.mark.skip(reason="Mae: do ROUND 1 in static/app.js first, then delete this line")
def test_hit_gives_the_player_the_next_card(client, use_deck):
    use_deck(DECK)
    created = client.post("/games").json()
    body = client.post(f"/games/{created['id']}/hit").json()
    assert body["player_hand"] == ["h9", "h5", "c2"]
    assert body["player_total"] == 19


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_a_second_hit_adds_to_the_first(client, use_deck):
    # The first hit has to change the game stored in `games`, not just the
    # response -- otherwise the second hit starts from the original two cards.
    use_deck(TWO_HITS_DECK)
    created = client.post("/games").json()
    client.post(f"/games/{created['id']}/hit")
    body = client.post(f"/games/{created['id']}/hit").json()
    assert body["player_hand"] == ["h1", "h2", "c2", "c3"]


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_hit_that_goes_bust_finishes_the_game(client, use_deck):
    use_deck(PLAYER_BUSTS_DECK)
    created = client.post("/games").json()
    body = client.post(f"/games/{created['id']}/hit").json()
    assert body["status"] == "finished"
    assert body["result"] == "Dealer"


# STOP. Go to static/app.js, do ROUND 2, and try the Hit button.


# ============================================================================
# ROUND 3 -- Stand.  POST /games/{game_id}/stand: the dealer plays, and the
# round ends.
# ============================================================================

@pytest.mark.skip(reason="Mae: do ROUND 2 in static/app.js first, then delete this line")
def test_stand_finishes_the_game(client, use_deck):
    use_deck(DECK)
    created = client.post("/games").json()
    body = client.post(f"/games/{created['id']}/stand").json()
    assert body["status"] == "finished"


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_stand_gives_the_result(client, use_deck):
    # Player stands on 16, dealer already has 17.
    use_deck(DECK)
    created = client.post("/games").json()
    body = client.post(f"/games/{created['id']}/stand").json()
    assert body["result"] == "Dealer"


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_stand_makes_the_dealer_play_out_their_hand(client, use_deck):
    use_deck(DEALER_HITS_DECK)
    created = client.post("/games").json()
    body = client.post(f"/games/{created['id']}/stand").json()
    assert body["dealer_hand"] == ["d9", "d4", "c3"]
    assert body["dealer_total"] == 19


# STOP. Go to static/app.js, do ROUND 3, and play a whole game in the browser.


# ============================================================================
# ROUND 4 -- Making the API solid. The page works now; these are the cases a
# real API has to get right.
# ============================================================================

@pytest.mark.skip(reason="Mae: do ROUND 3 in static/app.js first, then delete this line")
def test_two_new_games_get_different_ids(client, use_deck):
    use_deck(DECK)
    first = client.post("/games").json()
    second = client.post("/games").json()
    assert first["id"] != second["id"]


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_new_game_does_not_send_the_deck(client, use_deck):
    # If the web page could see the deck, the player would know every card
    # coming. Only the fields in GameState should go out.
    use_deck(DECK)
    body = client.post("/games").json()
    assert "deck" not in body


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_new_game_with_a_player_blackjack_is_already_finished(client, use_deck):
    use_deck(PLAYER_BLACKJACK_DECK)
    body = client.post("/games").json()
    assert body["status"] == "finished"
    assert body["result"] == "Player"


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_get_game_returns_the_game_that_was_created(client, use_deck):
    use_deck(DECK)
    created = client.post("/games").json()
    response = client.get(f"/games/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_get_game_with_an_unknown_id_is_404(client):
    response = client.get("/games/not-a-real-id")
    assert response.status_code == 404


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_hit_with_an_unknown_id_is_404(client):
    response = client.post("/games/not-a-real-id/hit")
    assert response.status_code == 404


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_hit_after_the_game_is_finished_is_400(client, use_deck):
    # 400 means "bad request": the request makes sense, just not right now.
    use_deck(PLAYER_BUSTS_DECK)
    created = client.post("/games").json()
    client.post(f"/games/{created['id']}/hit")  # goes bust
    response = client.post(f"/games/{created['id']}/hit")
    assert response.status_code == 400


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_stand_with_an_unknown_id_is_404(client):
    response = client.post("/games/not-a-real-id/stand")
    assert response.status_code == 404


@pytest.mark.skip(reason="Mae: delete this line when the test above is green")
def test_stand_after_the_game_is_finished_is_400(client, use_deck):
    use_deck(DECK)
    created = client.post("/games").json()
    client.post(f"/games/{created['id']}/stand")
    response = client.post(f"/games/{created['id']}/stand")
    assert response.status_code == 400
