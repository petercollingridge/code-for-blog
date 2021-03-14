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


def get_svg(tree, dx=100, dy=50, include_styles=True):
    max_x = dx * (len(tree.get_all_leaves()))
    max_y = dy * (tree.get_y_coord() + 1)

    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {max_x} {max_y + 30}">\n'
    if include_styles:
        svg += """
    <style>
        .arm {
            stroke: #111;
            stroke-width: 2;
            stroke-linecap: round;
        }
        .leaf-label {
            text-anchor: middle;
            alignment-baseline: hanging;
        }
    </style>
"""

    svg += tree.write_as_svg(dx, dy, 5, max_y)
    svg += "</svg>"
    
    return svg


def write_svg(svg, filename):
    if not filename[-4] == '.svg':
        filename += '.svg'

    print(filename)
    with open(filename, 'w') as f:
        f.write(svg)


def write_tree(nodes, dx, dy, include_styles=False):
    tree = Node(nodes)
    svg = get_svg(tree, dx, dy, include_styles)
    filename = "-".join(node.name for node in tree.get_all_leaves())
    write_svg(svg, filename)


if __name__ == '__main__':
    nodes = ("A", ("B", ("C", "D")))
    nodes = ((("A", "B"), "C"), "D")
    nodes = ("A", (("B", "C"), "D"))
    nodes = (("A", ("B", "C")), "D")
    nodes = (("A", "B"), ("C", "D"))

    # nodes = ("A", ("B", "C"))
    # nodes = (("B", "C"), "A")
    # write_tree(nodes, 40, 20, True)

    nodes = ("Human", "Chimp")
    nodes = ("Dog", ("Human", "Chimp"))
    nodes = (("Chimp", "Human"), "Dog")
    nodes = ("Dog", ("Monkey", ("Human", "Chimp")))
    nodes = (("Dog", "Wolf"), ("Human", "Chimp"))
    nodes = ("Dog", (("Chimp", "Human"), "Monkey"))
    nodes = ("Chicken", ("Dog", ("Human", "Chimp")))

    nodes = ("Chicken", ("Dog", ("Monkey", ("Human", "Chimp"))))
    nodes = ("Chicken", (("Dog", "Wolf"), ("Human", "Chimp")))

    write_tree(nodes, 80, 30, True)
