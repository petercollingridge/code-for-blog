class Node:
    def __init__(self, children, index=0):
        if isinstance(children, str):
            self.is_leaf = True
            self.index = index
            self.name = children
        else:
            self.is_leaf = False
            self.index = None
            self.child_1 = Node(children[0], index=index)
            index += self.child_1._count_descendants()
            self.child_2 = Node(children[1], index=index)

    def count_descendants(self):
        if self.is_leaf:
            return 0
        else:
            return self._count_descendants()

    def _count_descendants(self):
        if self.is_leaf:
            return 1
        else:
            return self.child_1._count_descendants() + self.child_2._count_descendants()

    def get_x_coord(self):
        if self.is_leaf:
            return self.index
        else:
            return (self.child_1.get_x_coord() + self.child_2.get_x_coord()) / 2

    def get_y_coord(self):
        if self.is_leaf:
            return 0
        else:
            return 1 + max(self.child_1.get_y_coord(), self.child_2.get_y_coord())

    def get_all_leaves(self):
        if self.is_leaf:
            return [self]
        else:
            return self.child_1.get_all_leaves() + self.child_2.get_all_leaves()

    def write_as_svg(self, dx, dy, parent_y, max_y):
        x = dx * (0.5 + self.get_x_coord())
        y = max_y - dy * self.get_y_coord()

        # Vertical line for this node
        s = f'<line class="arm" x1="{x}" x2="{x}" y1="{y}" y2="{parent_y}"/>\n'
        if self.is_leaf:
            s += f'<text class="leaf-label" x="{x}" y="{y + 5}">{self.name}</text>\n'
            return s
        else:
            x1 = dx * (0.5 + self.child_1.get_x_coord())
            x2 = dx * (0.5 + self.child_2.get_x_coord())
            s += f'<line class="arm" x1="{x1}" x2="{x2}" y1="{y}" y2="{y}"/>\n'
            s += self.child_1.write_as_svg(dx, dy, y, max_y)
            s += self.child_2.write_as_svg(dx, dy, y, max_y)
            return s

    def __str__(self):
        if self.is_leaf:
            return f"Leaf node {self.name} (index={self.index})"
        else:
            return "<Node>"


def draw_svg(tree, dx=80, dy=80):
    max_x = dx * (len(tree.get_all_leaves()) + 1)
    max_y = dy * (tree.get_y_coord() + 1)

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_x} {max_y + 20}">\n'
    svg += """
    <style>
        .arm {
            stroke: #111;
            stroke-weight: 1;
            stroke-linecap: round;
        }
        .leaf-label {
            text-anchor: middle;
            alignment-baseline: hanging;
        }
    </style>
    """
    svg += tree.write_as_svg(dx, dy, 0, max_y)
    svg += "</svg>"
    
    with open('tree.svg', 'w') as f:
        f.write(svg)


example = ("A", ("B", "C"))
example = ("A", (("B", "C"), "D"))

tree = Node(example)
nodes = tree.get_all_leaves()

draw_svg(tree, 100, 50)
# print(tree.get_height())
# print(tree.child_1.get_height())
# print(tree.child_2.get_height())

# print(tree.child_2.count_descendants())
# print(tree.child_2.child_1)
# print(tree.child_2.child_2)
