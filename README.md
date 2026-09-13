# blackjack_api

The blackjack rules from [html_blackjack](https://github.com/Mae6666666666/html_blackjack),
rebuilt in Python and served by a FastAPI API. A web page will call the API to
play a round: one player against the dealer.

## Running it

```sh
uv sync                    # install everything (first time only)
uv run pytest              # run the tests
uv run fastapi dev main.py # start the server
```

With the server running:

- http://127.0.0.1:8000 — the game
- http://127.0.0.1:8000/health — is the API alive?
- http://127.0.0.1:8000/docs — every endpoint, and you can try them out
- http://127.0.0.1:8000/static/deck/hearts_0.png — a card image

In VS Code, the Testing panel and the play buttons next to each test work too.

## What's where

| File | What it does |
|---|---|
| `game.py` | The rules of blackjack. No web code. |
| `models.py` | The shape of the data the API sends back. |
| `main.py` | The API endpoints. They call `game.py` and send back models. |
| `tests/test_game.py` | Tests for the rules. |
| `tests/test_models.py` | Tests for the models. |
| `tests/test_api.py` | Tests for the endpoints. |
| `tests/conftest.py` | Shared test setup: a test client and a fixed deck. |
| `static/index.html`, `static/style.css` | The web page. |
| `static/page.js` | Draws the game on the page. |
| `static/app.js` | Connects the page to the API. |
| `static/deck/` | The card images. |

## Your JavaScript functions, in Python

Python names use `snake_case` instead of `camelCase`.

| html_blackjack (JS) | blackjack_api (Python) |
|---|---|
| `totalCalc` | `total_calc` |
| `isBust` | `is_bust` |
| `isBlackjack` | `is_blackjack` |
| `compareCards` | `compare_hands` |
| `buildDeck` | `build_deck` |
| `dealCard` | `deal_card` |
| `dealHand` | `deal_hand` |
| `shuffle` | `shuffle` |
| `dealerShouldHit` | `dealer_should_hit` |
| `playDealerTurn` | `play_dealer_turn` |
| `whoWins` | `who_wins` |

New in Python: `card_value`, and the round itself — `Game`, `start_game`,
`player_hit` and `player_stand`.

Changes from the JS version:

- If both hands bust, the **dealer** wins — the player busted first.
- A two-card blackjack beats any other 21.
- `shuffle` gives back a shuffled copy instead of emptying the deck it was given.

## The rules this follows

- The player gets the first two cards, the dealer the next two. Both of the
  dealer's cards are shown.
- If either hand is a blackjack, the round ends straight away.
- The player hits until they stand or go bust.
- The dealer then takes cards until they reach 17, and stands on a soft 17.
- No betting, splitting or doubling down.

## Where to start (Mae)

1. Read `models.py` — it explains what a model is, using `HealthResponse`.
2. Read the `/health` endpoint in `main.py` and its tests in `tests/test_api.py`.
3. Open `tests/test_models.py` and write `GameState`.
4. Work down `tests/test_api.py` one test at a time. When a test goes green,
   delete the `@pytest.mark.skip` line above the next one.
5. The tests come in rounds: **Deal**, **Hit**, **Stand**, then **making the API
   solid**. At the end of each round, do the same round in `static/app.js` and
   try it in the browser before carrying on.

The page's HTML, CSS and `page.js` are done. Your JavaScript is only the part
that talks to the API.
