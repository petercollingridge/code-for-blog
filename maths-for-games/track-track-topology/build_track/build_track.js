var vm = new Vue({
    el: '#track-builder',
    data: {
        points: [
            { x: 100, y: 100, angle: 270 },
            { x: 300, y: 100, angle: 90 },
        ],
        selectedPoint: 0
    }
});