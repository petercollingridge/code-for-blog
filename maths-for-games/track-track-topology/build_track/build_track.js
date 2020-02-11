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
            // const LENGTH = 10000 / (dist + 20);
            const LENGTH = 50;

            const c1 = Math.cos(coord1.angle);
            const s1 = Math.sin(coord1.angle);
            const c2 = Math.cos(coord2.angle);
            const s2 = Math.sin(coord2.angle);

            const x1 = coord1.x + LENGTH * c1;
            const y1 = coord1.y + LENGTH * s1;
            const x2 = coord2.x + LENGTH * c2;
            const y2 = coord2.y + LENGTH * s2;

            if (dist < 50) { 
                // When points are close create a mid point to loop around
                const x3 = (coord1.x + coord2.x + LENGTH * 5 * (c1 + c2)) / 2;
                const y3 = (coord1.y + coord2.y + LENGTH * 5 * (s1 + s2)) / 2;
                const midAngle = (coord1.angle + coord2.angle) / 2;
                const dx = LENGTH * Math.cos(midAngle + Math.PI / 2);
                const dy = LENGTH * Math.sin(midAngle + Math.PI / 2);

                // Determine which way vector should point
                const dot = c1 * dx + s1 * dy;
                const x4 = x3 + Math.sign(dot) * dx
                const y4 = y3 + Math.sign(dot) * dy;

                let d = `M${ coord1.x } ${ coord1.y }`;
                d += `C${x1} ${y1} ${x4} ${y4} ${x3} ${y3}`;
                d += `S${x2} ${y2} ${ coord2.x } ${ coord2.y }`;
                return d;
            } else {
                return `M${ coord1.x } ${ coord1.y }C${x1} ${y1} ${x2} ${y2} ${ coord2.x } ${ coord2.y }`;
            }
        },
        getCoordinates(position, point) {
            let { x, y, angle } = point;
            x = parseFloat(x);
            y = parseFloat(y);
            const angleRadians = angle * Math.PI / 180;
            
            if (position === 'base') {
                return { x, y, angle: angleRadians - Math.PI };
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
