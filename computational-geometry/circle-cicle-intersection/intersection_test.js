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

function intersectionPoints(c1, c2) {
    // Distance between centers
    let dx = c2.x - c1.x;
    let dy = c2.y - c1.y;
    const d = Math.sqrt(dx * dx + dy * dy);
    
    // Circles too far apart
    if (d > c1.r + c2.r) { return; }
    
    // One circle completely inside the other
    if (d < Math.abs(c1.r - c2.r)) { return; }
    
    // Get unit vector from one center to the other
    dx /= d;
    dy /= d;
    
    // Center of intersection line is a units along the line
    // from circle 1 in the direction of circle 2
    const a = (c1.r * c1.r - c2.r * c2.r + d * d) / (2 * d);
    const px = c1.x + a * dx;
    const py = c1.y + a * dy;
    
    // Height of intersection line
    const h = Math.sqrt(c1.r * c1.r - a * a);

    // Intersection points are perpendicular to the line between
    // the circles, h units up or down.
    return {
        p1: {
            x: px + h * dy,
            y: py - h * dx
        },
        p2: {
            x: px - h * dy,
            y: py + h * dx
        }
    };
};

const circle1 = { x: 100, y: 50, r: 40 };
const circle2 = { x: 200, y: 80, r: 70 };
const circle3 = { x: 200, y: 80, r: 60 };

let hit;
hit = circlesIntersect(circle1, circle2);     // True
hit = circlesIntersect(circle1, circle3);     // False

hit = intersectionPoints(circle1, circle2);
console.log(hit);