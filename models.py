"""
Models: the exact shape of the data the API sends back.

A model is a class that inherits from pydantic's BaseModel. Each line inside
it is one field: a name, a colon, and the type that field must be.

    class HealthResponse(BaseModel):
        status: str

That says: "a health response has exactly one field, called status, and it is
a string". When an endpoint returns one of these, FastAPI turns it into JSON:

    {"status": "ok"}

Why bother, when you could just return a dict like {"status": "ok"}?

  1. It checks your work. Try HealthResponse(status=5) and pydantic raises a
     ValidationError, because 5 is not a string. A typo in a dict would just
     quietly send the wrong thing to the browser.

  2. It is a promise. Whoever writes the web page can read this class and know
     exactly what they will get back, without reading the endpoint code.

  3. It filters. Put `response_model=HealthResponse` on the endpoint and
     FastAPI only sends the fields listed here -- anything else the endpoint
     returns gets left out. That matters when some data must stay secret.

  4. It documents itself. Run the server and open http://127.0.0.1:8000/docs
     -- every model shows up there, with its fields and types.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """What GET /health sends back: just a sign of life."""
    status: str


# --- Your model goes below --------------------------------------------------

class GameState(BaseModel):
    id: str
    player_hand: list[str]
    dealer_hand: list[str]
    player_total: int
    dealer_total: int
    status: str
    result: str | None = None