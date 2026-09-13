from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from game import build_deck, shuffle
from models import HealthResponse

app = FastAPI()

# Every game in progress, looked up by its id. This lives in memory, so all
# the games disappear when the server restarts.
games = {}


def make_deck():
    """A fresh shuffled deck for a new game.

    Always get a deck by calling this. The tests swap it for a fixed deck, so
    they know exactly which cards will come out.
    """
    return shuffle(build_deck())


@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok")


# --- Your endpoints go below ------------------------------------------------



# The card images, served at /static/deck/hearts_0.png and so on.
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent / "static"),
    name="static",
)
