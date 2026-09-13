// app.js -- Mae, this file is yours. It connects the page to your API.
//
// page.js does all the drawing. Your job is the conversation with the server:
// when a button is clicked, send the right request, wait for the reply, and
// hand the GameState that comes back to showGame().
//
// To try it out:
//   uv run fastapi dev main.py      then open http://127.0.0.1:8000
//
// Open DevTools (Cmd + Option + I). The Network tab shows every request your
// code sends and exactly what came back. The Console tab shows any errors.

import { showGame, showMessage } from "./page.js"

const dealButton = document.getElementById("deal-button")
const hitButton = document.getElementById("hit-button")
const standButton = document.getElementById("stand-button")


// ROUND 1 -- Deal
//
// When the Deal button is clicked:
//   1. send a POST request to /games
//   2. read the JSON out of the response
//   3. pass it to showGame()
//
// Hit and Stand will need to know which game they are playing, so keep hold
// of the game's id somewhere they can reach it.


// ROUND 2 -- Hit
//
// When the Hit button is clicked, send a POST request to /games/<the id>/hit
// and show the game that comes back.


// ROUND 3 -- Stand
//
// The same idea as Hit, but to /games/<the id>/stand.


// ROUND 4 -- When things go wrong
//
// Not every response is a GameState. A 404 or 400 comes back with an error
// instead. Check response.ok before calling showGame(), and if it's false,
// use showMessage() to say something went wrong.
