var vm = new Vue({
    el: '#track-builder',
    data: {
        points: [
            { x: 100, y: 100, angle: 270 },
            { x: 300, y: 100, angle: 90 },
        ],
        connections: [],
        selectedPoint: false,
        connectionPoint1: '',
        connectionPoint2: '',
        connectionPosition1: '',
        connectionPosition2: '',
    },
    computed: {
        canAddConnections: function() {
            return this.connectionPoint1 && this.connectionPoint2 &&
                this.connectionPoint1 && this.connectionPoint2;
        }
    },
    methods: {
        selectPoint: function(i) {
            this.selectedPoint = i;
        },
        addConnection() {
            // Check is connection is valid

            this.connections.push({
                point1: this.connectionPoint1,
                point2: this.connectionPoint2,
                position1: this.connectionPosition1,
                position2: this.connectionPosition2,
            })
        },
        getConnectionPath(connection) {
            co
        }
    }
});
