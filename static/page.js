// page.js -- draws the game on the page. You don't need to change this file.
//
//   showGame(game)      give it a GameState from your API and it shows the
//                       cards, the totals and the message, and turns the Hit
//                       and Stand buttons on or off
//   showMessage(text)   puts a line of text in the middle of the table

const SUIT_NAMES = { h: "hearts", d: "diamonds", s: "spades", c: "clubs" }

const RESULT_MESSAGES = {
    Player: "You win!",
    Dealer: "Dealer wins.",
    Draw: "It's a draw.",
}

const table = document.querySelector(".table")


export function showMessage(text) {
    document.getElementById("message").textContent = text
}


export function showGame(game) {
    showHand("player-hand", game.player_hand)
    showHand("dealer-hand", game.dealer_hand)
    document.getElementById("player-total").textContent = game.player_total
    document.getElementById("dealer-total").textContent = game.dealer_total

    const finished = game.status === "finished"
    document.getElementById("hit-button").disabled = finished
    document.getElementById("stand-button").disabled = finished
    table.dataset.result = finished ? game.result : ""

    if (!finished) {
        showMessage("Hit or stand?")
    } else if (game.player_total > 21) {
        showMessage("Bust! " + RESULT_MESSAGES[game.result])
    } else if (game.dealer_total > 21) {
        showMessage("Dealer busts. " + RESULT_MESSAGES[game.result])
    } else {
        showMessage(RESULT_MESSAGES[game.result])
    }
}


function showHand(elementId, cards) {
    const hand = document.getElementById(elementId)

    // If the cards on the table aren't the start of this hand, it's a new
    // round: clear them away.
    const onTable = [...hand.children].map((img) => img.alt)
    if (!onTable.every((card, i) => card === cards[i])) {
        hand.replaceChildren()
    }

    // Only add the new cards, so the ones already there don't animate again.
    const alreadyShown = hand.children.length
    for (let i = alreadyShown; i < cards.length; i++) {
        const img = document.createElement("img")
        img.className = "card"
        img.src = cardImagePath(cards[i])
        img.alt = cards[i]
        img.style.animationDelay = `${(i - alreadyShown) * 120}ms`
        hand.append(img)
    }
}


function cardImagePath(card) {
    const suit = SUIT_NAMES[card[0]]
    const index = card.slice(1)
    return `/static/deck/${suit}_${index}.png`
}
