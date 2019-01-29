var vm = new Vue({
    el: '#generate-words',
    data: {
        words: [],
        colours: []
    },
    methods: {
        addWord() {
            this.words.push(getSillyWord());
            this.colours.push('hsl(' + Math.floor(Math.random() * 360) + ', 100%, 40%');
        }
    }
});
