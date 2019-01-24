var vm = new Vue({
    el: '#generate-words',
    data: {
        words: ["hello", "goodbye"]
    },
    methods: {
        addWord() {
            this.words.push("new word")
        }
    }
});
