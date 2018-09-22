// Given an array and a callback function
// return a function that passes each element of
// the array as an argument to the callback function
function applyToSet(groups, callback) {
    return function() {
        for (var i = 0; i < groups.length; i++) {
            callback(groups[i]);
        }
    };
}

function highlight(element) {
    element.classList.add("highlight");
}

function unhighlight(element) {
    element.classList.remove("highlight");
}

function addHighlight(cardSelector, setSelector) {
    var element = document.getElementById(cardSelector);
    if (element) {
        var groups = document.getElementsByClassName(setSelector);
        element.addEventListener('mouseover', applyToSet(groups, highlight));
        element.addEventListener('mouseout', applyToSet(groups, unhighlight));
    }
}

function geometryHighlights(n) {
    for (var i = 1; i <= n; i++) {
        addHighlight('card-' + n + '-' + i, 'set-' + n + '-' + i);
        var symbol = String.fromCharCode(i + 64);
        addHighlight('symbol-' + n + symbol, 'line-' + n + symbol);
    }
}

for (var i = 1; i <= 7; i++) {
    addHighlight('card' + i, 'set' + i);
}

for (var i = 1; i <= 13; i++) {
    addHighlight('card13-' + i, 'set13-' + i);
}

geometryHighlights(3);
geometryHighlights(5);
geometryHighlights(6);
geometryHighlights(7);

var app = new Vue({
    el: '#app',
    data: {
        numSymbols: 7,
        cardSymbols: 3,
        symbols: "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        symbolWidth: 24,
        cards: [],
        newCard: {},
        newCardSymbolCount: 0,
        matchingCards: {},
        unusableSymbols: {},
        symbolCount: {}
    },
    computed: {
        allSymbols: function () {
            return this.symbols.substr(0, this.numSymbols);
        },
        cardWidth: function() {
            return this.symbolWidth * this.numSymbols;
        },
    },
    methods: {
        getTranslation: function(index) {
            return "translate(20 " + (index * 27 + 24) + ")";
        },

        getSymbolX: function(symbol) {
            // Convert symbol to index
            if (isNaN(symbol)) { symbol = symbol.charCodeAt(0) - 65; }
            return (symbol + 0.5) * this.symbolWidth;
        },

        toggleSymbol: function(symbol) {   
            if (!this.newCard[symbol]) {
                this.addSymbol(symbol);
            } else {
                this.removeSymbol(symbol);
            }
        },

        addSymbol: function(symbol) {
            Vue.set(this.newCard, symbol, true);
            this.newCardSymbolCount++
            if (this.newCardSymbolCount == this.cardSymbols) {
                this.addCard();
            } else {
                var matchingCards = this.getCardsWithSymbol(symbol);
                for (var i = 0; i < matchingCards.length; i++) {
                    var card = matchingCards[i];
                    this.matchingCards[card.join("")] = true;
                    this.findUnusableSymbols(card, symbol);
                }
            }
        },

        removeSymbol: function(symbol) {
            Vue.set(this.newCard, symbol, false);
            this.newCardSymbolCount--;

            for (var card in this.matchingCards) {
                if (this.matchingCards[card]) {
                    if (card.indexOf(symbol) > -1) {
                        this.matchingCards[card] = false;
                        for (var i = 0; i < card.length; i++) {
                            this.unusableSymbols[card[i]] = false;
                        }
                    }
                }
            }
        },

        addCard: function() {
            var card = [];
            for (var symbol in this.newCard) {
                this.symbolCount[symbol] = (this.symbolCount[symbol] || 0) + 1;
                if (this.newCard[symbol]) {
                    card.push(symbol);
                }
            }
            this.cards.push(card);
            this.newCard = {};
            this.matchingCards = {};
            this.newCardSymbolCount = 0;
            this.unusableSymbols = {};
        },

        removeCard: function(index) {
            var card = this.cards.splice(index, 1)[0];
        },

        getCardsWithSymbol: function(symbol) {
            return this.cards.filter(function(card) {
                return card.indexOf(symbol) > -1;
            });
        },

        findUnusableSymbols: function(card, usedSymbol) {
            for (var i = 0; i < card.length; i++) {
                if (card[i] !== usedSymbol) {
                    this.unusableSymbols[card[i]] = true;
                }
            }
        }
    }
});