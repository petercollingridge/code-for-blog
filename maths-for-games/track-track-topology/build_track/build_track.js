const DEGREES_30 = Math.PI * 30 / 180;
const POINT_ARC_LENGTH = 50;
// const POINT_SIZE = 2 * POINT_ARC_LENGTH * Math.sin(DEGREES_30 / 2);
const POINT_SIZE = POINT_ARC_LENGTH;


var vm = new Vue({
    el: '#track-builder',
    data: {
        points: [
            { x: 100, y: 100, angle: 0 },
            { x: 300, y: 100, angle: 180 },
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
            return this.connectionPoint1 !== '' &&
                this.connectionPoint2 !== '' &&
                this.connectionPosition1 &&
                this.connectionPosition2;
        }
    },
    methods: {
        selectPoint: function(i) {
            this.selectedPoint = i;
        },
        addConnection() {
            // TODO: Check is connection is valid

            this.connections.push({
                point1: this.connectionPoint1,
                point2: this.connectionPoint2,
                position1: this.connectionPosition1,
                position2: this.connectionPosition2,
            })
        },
        getConnectionPath({point1, point2, position1, position2,}) {
            const p = this.points[point1];
            const coord1 = this.getCoordinates(position1, this.points[point1]);
            const coord2 = this.getCoordinates(position2, this.points[point2]);
            return `M${p.x} ${p.y} ${ coord1.x } ${ coord1.y }L${ coord2.x } ${ coord2.y }`;
        },
        getCoordinates(position, point) {
            const { x, y, angle } = point;
            const angleRadians = (angle - 90) * Math.PI / 180;

            if (position === 'base') {
                return { x, y, angle };
            } else {
                const turnAngle = angleRadians + (position === 'arm1' ? -DEGREES_30 : DEGREES_30);
                return {
                    x: x + POINT_SIZE * Math.cos(turnAngle),
                    y: y + POINT_SIZE * Math.sin(turnAngle),
                    angle: turnAngle
                };
            }
        }
    }
});
