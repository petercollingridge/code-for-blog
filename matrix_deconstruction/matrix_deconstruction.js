var vm = new Vue({
    el: '#matrix-deconstruction',
    data: {
        a: 1,
        b: 0,
        c: 0,
        d: 1,
        e: 0,
        f: 0,
    },
    computed: {
        matrix: function() {
            const a = isNaN(this.a) ? 0 : this.a;
            const b = isNaN(this.b) ? 0 : this.b;
            const c = isNaN(this.c) ? 0 : this.c;
            const d = isNaN(this.d) ? 0 : this.d;
            const e = isNaN(this.e) ? 0 : this.e;
            const f = isNaN(this.f) ? 0 : this.f;
            return `matrix(${a} ${this.b} ${this.c} ${this.d} ${this.e} ${this.f})`;
        },
        transforms: function() {
            const sx = Math.sign(this.a) * Math.sqrt(this.a * this.a + this.c * this.c);
            const sy = Math.sign(this.d) * Math.sqrt(this.b * this.b + this.d * this.d);
            const tx = this.e;
            const ty = this.f;
            const angle = Math.atan2(this.b, this.d) * 180 / Math.PI;
            return `translate(${tx} ${ty}) scale(${sx} ${sy}) rotate(${angle})`;
        }
    },
});
