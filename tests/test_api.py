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
