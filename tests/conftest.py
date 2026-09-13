"""
Shared setup for the API tests. pytest loads this file automatically, and any
test can ask for one of these fixtures just by naming it as a parameter.
"""

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture
def client():
    """A fake browser that sends requests straight to the app -- no server needed.

    Also empties the games dict, so every test starts with no games in it.
    """
    main.games.clear()
    return TestClient(main.app)


@pytest.fixture
def use_deck(monkeypatch):
    """Make new games deal these cards, in this order, instead of a shuffled deck.

        use_deck(["h9", "h5", "d9", "d6", "c2"])

    The player gets the first two, the dealer the next two, and hits come
    from the rest.
    """
    def _use_deck(cards):
        monkeypatch.setattr(main, "make_deck", lambda: list(cards))
    return _use_deck
