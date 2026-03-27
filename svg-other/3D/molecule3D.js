const ATOM_SIZE = 4;
const BOND_THICKNESS = 3;
const ROTATION_SPEED = 0.02;

const ATOM_PROPERTIES = {
  "H": { radius: 1.2, color: "rgb(180, 180, 180)" },
  "C": { radius: 1.7, color: "rgb(64, 61, 64)" },
  "N": { radius: 1.55, color: "rgb(68, 75, 219)" },
  "O": { radius: 1.52, color: "rgb(250, 15, 15)" },
  "P": { radius: 1.8, color: "rgb(237, 107, 7)" },
};

const MOLECULAR_DATA = {
    ATP: {
        info: "Adenosine triphosphate is the short term enzyme store for all cells. It is produced by phosphorylating ADP during catabolic reactions or as part of the electron transport chain. Most biological reactions that require energy obtain it by hydrolysing the final phosphate from ATP.",
        atoms: [["P", 1.200, -0.226, -6.850], ["O", 1.740, 1.140, -6.672], ["O", 2.123, -1.036, -7.891], ["O", -0.302, -0.139, -7.421], ["P", 0.255, -0.130, -4.446], ["O", 0.810, 1.234, -4.304], ["O", -1.231, -0.044, -5.057], ["O", 1.192, -0.990, -5.433], ["P", -0.745, 0.068, -2.071], ["O", -2.097, 0.143, -2.669], ["O", -0.125, 1.549, -1.957], ["O", 0.203, -0.840, -3.002], ["O", -0.844, -0.587, -0.604], ["C", -1.694, 0.260, 0.170], ["C", -1.831, -0.309, 1.584], ["O", -0.542, -0.355, 2.234], ["C", -2.683, 0.630, 2.465], ["O", -4.033, 0.165, 2.534], ["C", -2.011, 0.555, 3.856], ["O", -2.926, 0.043, 4.827], ["C", -0.830, -0.418, 3.647], ["N", 0.332, 0.015, 4.425], ["C", 1.302, 0.879, 4.012], ["N", 2.184, 1.042, 4.955], ["C", 1.833, 0.300, 6.033], ["C", 2.391, 0.077, 7.303], ["N", 3.564, 0.706, 7.681], ["N", 1.763, -0.747, 8.135], ["C", 0.644, -1.352, 7.783], ["N", 0.088, -1.178, 6.602], ["C", 0.644, -0.371, 5.704], ["H", 2.100, -0.546, -8.725], ["H", -0.616, -1.048, -7.522], ["H", -1.554, -0.952, -5.132], ["H", 0.752, 1.455, -1.563], ["H", -2.678, 0.312, -0.296], ["H", -1.263, 1.259, 0.221], ["H", -2.275, -1.304, 1.550], ["H", -2.651, 1.649, 2.078], ["H", -4.515, 0.788, 3.094], ["H", -1.646, 1.537, 4.157], ["H", -3.667, 0.662, 4.867], ["H", -1.119, -1.430, 3.931], ["H", 1.334, 1.357, 3.044], ["H", 3.938, 0.548, 8.562], ["H", 4.015, 1.303, 7.064], ["H", 0.166, -2.014, 8.490]],
        bonds: [[0,1],[0,2],[0,3],[0,7],[2,31],[3,32],[4,5],[4,6],[4,7],[4,11],[6,33],[8,9],[8,10],[8,11],[8,12],[10,34],[12,13],[13,14],[13,35],[13,36],[14,15],[14,16],[14,37],[15,20],[16,17],[16,18],[16,38],[17,39],[18,19],[18,20],[18,40],[19,41],[20,21],[20,42],[21,22],[21,30],[22,23],[22,43],[23,24],[24,25],[24,30],[25,26],[25,27],[26,44],[26,45],[27,28],[28,29],[28,46],[29,30]]
    },
};

(function () {
    const svg = document.getElementById('molecule-viewer');

    const molecule = MOLECULAR_DATA.ATP;

    // Points are objects with x, y, z properties, which we rotate.
    const points = [];

    // Shapes have a refernce to a point and an SVG element.
    // They have an update function which updates the element's position based on the point's position.
    let shapes = [];

    function fitAtomsToViewer(atoms, viewerSize) {
        // Find center of the molecule
        let meanX = 0, meanY = 0, meanZ = 0;
        for (let i = 0; i < atoms.length; i++) {
            meanX += atoms[i][1];
            meanY += atoms[i][2];
            meanZ += atoms[i][3];
        }
        meanX /= atoms.length;
        meanY /= atoms.length;
        meanZ /= atoms.length;

        // Find bounds of the molecule
        let maxD = 0;
        const centeredAtoms = atoms.map(([type, x, y, z]) => {
            const dx = x - meanX;
            const dy = y - meanY;
            const dz = z - meanZ;
            const d = Math.sqrt(dx * dx + dy * dy + dz * dz);
            if (d > maxD) {
                maxD = d;
            }
            return [type, dx, dy, dz];
        });

        const scale = viewerSize / (2 * maxD);
        return centeredAtoms.map(([type, x, y, z]) => ([type, x * scale, y * scale, z * scale]));
    }

    function createCircleElement(cx, cy, r, fill) {
        const circle = document.createElementNS("http://www.w3.org/2000/svg", "circle");
        circle.setAttribute("cx", cx);
        circle.setAttribute("cy", cy);
        circle.setAttribute("r", r);
        circle.setAttribute("fill", fill);
        return circle;
    }

    function addAtoms(atoms) {
        atoms.forEach(([type, x, y, z]) => {
            const { radius, color } = ATOM_PROPERTIES[type];
            const element = document.createElementNS("http://www.w3.org/2000/svg", "g");

            const r = radius * ATOM_SIZE;
            const circle = createCircleElement(0, 0, r, color);
            const highlight1 = createCircleElement(0, 0, r - 0.8, "rgba(255, 255, 255, 0.2)");
            const highlight2 = createCircleElement(-r * 0.25, -r * 0.25, r * 0.2, "rgba(255, 255, 255, 0.5)");

            element.appendChild(circle);
            element.appendChild(highlight1);
            element.appendChild(highlight2);
            svg.appendChild(element);

            const point = { x, y, z, r };
            points.push(point);

            shapes.push({
                element,
                getZ: () => point.z,
                update: () => element.setAttribute("transform", `translate(${point.x}, ${point.y})`), 
            });
        });
    }

    function addBonds(atoms, bonds) {
        bonds.forEach(([i, j]) => {
            const atom1 = atoms[i];
            const atom2 = atoms[j];
            const x1 = atom1.x;
            const y1 = atom1.y;
            const z1 = atom1.z;
            const r1 = atom1.r;
            const x2 = atom2.x;
            const y2 = atom2.y;
            const z2 = atom2.z;
            const r2 = atom2.r;
            const dx = x2 - x1;
            const dy = y2 - y1;
            const dz = z2 - z1;
            const length = Math.sqrt(dx * dx + dy * dy + dz * dz);
            const vx = dx / length;
            const vy = dy / length;
            const vz = dz / length;

            const point1 = { x: x1 + vx * r1, y: y1 + vy * r1, z: z1 + vz * r1 };
            const point2 = { x: x2 - vx * r2, y: y2 - vy * r2, z: z2 - vz * r2 };
            points.push(point1);
            points.push(point2);

            const element = document.createElementNS("http://www.w3.org/2000/svg", "line");
            element.setAttribute("stroke", "rgb(166, 159, 166)");
            element.setAttribute("stroke-width", BOND_THICKNESS);
            svg.appendChild(element);

            const update = () => {
                element.setAttribute("x1", point1.x);
                element.setAttribute("y1", point1.y);
                element.setAttribute("x2", point2.x);
                element.setAttribute("y2", point2.y);
            };

            shapes.push({ element, getZ: () => (atom1.z + atom2.z) / 2, update});
        });
    }

    function updateAtomElements() {
        for (let i = 0; i < shapes.length; i++) {
            shapes[i].update();
        }
        shapes = shapes.sort((a, b) => b.getZ() - a.getZ());
        for (let i = 0; i < shapes.length; i++) {
            svg.appendChild(shapes[i].element);
        }
    };

    const viewerSize = Math.min(svg.clientWidth, svg.clientHeight);
    const scaledAtoms = fitAtomsToViewer(molecule.atoms, viewerSize - 20);

    addAtoms(scaledAtoms);
    addBonds(points, molecule.bonds);

    // Rotation around X axis
    function rotateX3D(theta){
        const ct = Math.cos(theta);
        const st = Math.sin(theta);
        let y, z;
        
        for (let i = 0; i < points.length; i++) {
            y = points[i].y;
            z = points[i].z;
            points[i].y = ct * y - st * z;
            points[i].z = st * y + ct * z;
        }

        updateAtomElements();
    };

    // Rotation around Y axis
    function rotateY3D(theta){
        const ct = Math.cos(theta);
        const st = Math.sin(theta);
        let x, z;
        
        for (let i = 0; i < points.length; i++) {
            x = points[i].x;
            z = points[i].z;
            points[i].x = ct * x + st * z;
            points[i].z = -st * x + ct * z;
        }

        updateAtomElements();
    };

    // Initial rotations
    rotateX3D(90 * Math.PI / 180);
    rotateY3D(90 * Math.PI / 180);
    rotateX3D(90 * Math.PI / 180);
    rotateY3D(90 * Math.PI / 180);
    rotateX3D(180 * Math.PI / 180);
    updateAtomElements();

    function addEventHandlers() {
        let dragging = false;
        document.addEventListener("mouseup", (event) => {
            dragging = false;
        });
        svg.addEventListener("mousedown", (event) => {
            dragging = true;
        });
        svg.addEventListener("mousemove", (event) => {
            if (dragging) {
                rotateX3D(event.movementY * ROTATION_SPEED);
                rotateY3D(event.movementX * ROTATION_SPEED);
            }
        });
    }

    addEventHandlers();
})();