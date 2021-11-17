function addCountWords(textareaId, buttonId, outputId) {
    const textarea = document.getElementById(textareaId);
    const button = document.getElementById(buttonId);
    const output = document.getElementById(outputId);

    button.addEventListener('click', () => {
        const text = textarea.value;
        const counts = countWords(text);
        outputWordCounts(output, counts);
    })
}

function countWords(text) {
    const counts = {};
    const words = text.toLowerCase().split(/[\s\.,;:"=]/g);
    words.forEach((word) => {
        word = word.replace(/\W /g, '');
        if (word) {
            if (counts[word]) {
                counts[word]++;
            } else {
                counts[word] = 1;
            }
        }
    });
    return counts;
}

function addElement(tag, parent, text) {
    const element = document.createElement(tag)
    element.innerHTML = text;
    parent.appendChild(element);
}

function outputWordCounts(output, counts) {
    const sortedCounts = Object
        .entries(counts)
        .sort((a, b) => b[1] - a[1])
    
    output.innerHTML = '';
    const table = document.createElement('table');
    const tHead = document.createElement('thead');
    const tBody = document.createElement('tbody');
    const tHeadRow = document.createElement('tr');

    addElement('th', tHeadRow, 'Word');
    addElement('th', tHeadRow, 'Count');

    sortedCounts.forEach(([word, count]) => {
        const row = document.createElement('tr');
        addElement('td', row, word);
        addElement('td', row, count);
        tBody.appendChild(row);
    })

    tHead.appendChild(tHeadRow);
    table.appendChild(tHead);
    table.appendChild(tBody);
    output.appendChild(table);
}