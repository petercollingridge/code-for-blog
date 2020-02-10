const DEGREES_30 = Math.PI * 30 / 180;
const POINT_ARC_LENGTH = 50;
const POINT_SIZE = 2 * POINT_ARC_LENGTH * Math.sin(DEGREES_30 / 2);
// const POINT_SIZE = POINT_ARC_LENGTH;


var vm = new Vue({
    el: '#track-builder',
    data: {
        points: [
            { x: 100, y: 100, angle: 0 },
            { x: 300, y: 100, angle: 180 },
        ],
        connections: [
            {
                point1: 0,
                point2: 1,
                position1: 'arm1',
                position2: 'arm2',
            }, {
                point1: 0,
                point2: 0,
                position1: 'arm2',
                position2: 'base',
            }
        ],
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
        getDistance: function (coord1, coord2) {
            const dx = coord1.x - coord2.x;
            const dy = coord1.y - coord2.y;
            return Math.sqrt(dx * dx + dy * dy);
        },
        getConnectionPath({point1, point2, position1, position2,}) {            
            const coord1 = this.getCoordinates(position1, this.points[point1]);
            const coord2 = this.getCoordinates(position2, this.points[point2]);

            const dist = this.getDistance(coord1, coord2);
            const LENGTH = 8000 / (dist + 20);
            console.log(LENGTH)

            const x1 = coord1.x + LENGTH * Math.cos(coord1.angle);
            const y1 = coord1.y + LENGTH * Math.sin(coord1.angle);
            const x2 = coord2.x + LENGTH * Math.cos(coord2.angle);
            const y2 = coord2.y + LENGTH * Math.sin(coord2.angle);

            return `M${ coord1.x } ${ coord1.y }C${x1} ${y1} ${x2} ${y2} ${ coord2.x } ${ coord2.y }`;
        },
        getCoordinates(position, point) {
            const { x, y, angle } = point;
            const angleRadians = angle * Math.PI / 180;

            if (position === 'base') {
                return { x, y, angle: angle - Math.PI };
            } else {
                const dAngle = position === 'arm1' ? -DEGREES_30 : DEGREES_30;
                const turnAngle = angleRadians + dAngle / 2;
                return {
                    x: x + POINT_SIZE * Math.cos(turnAngle),
                    y: y + POINT_SIZE * Math.sin(turnAngle),
                    angle: angleRadians + dAngle
                };
            }
        }
    }
});
