function circlesIntersect(c1, c2) {
    const dx = c1.x - c2.x;
    const dy = c1.y - c2.y;
    const d = Math.sqrt(dx * dx + dy * dy);
    return d <= c1.r + c2.r;
}

function circlesIntersectOptimised(c1, c2) {
    const dx = c1.x - c2.x;
    const dy = c1.y - c2.y;
    const r = c1.r + c2.r;
    return dx * dx + dy * dy <= r * r;
}

const circle1 = { x: 100, y: 50, r: 40 };
const circle2 = { x: 200, y: 80, r: 70 };
const circle3 = { x: 200, y: 80, r: 60 };

let hit;
hit = circlesIntersect(circle1, circle2);     // True
hit = circlesIntersect(circle1, circle3);     // False
