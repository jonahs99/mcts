from functools import reduce
import matplotlib.pyplot as plt

def draw_tree(node):
    plt.figure()

    def visible_childs(node):
        return list(filter(lambda child: child.n > 0, node.children))

    def draw_node(node, x, y, w):
        children = visible_childs(node)

        n = len(children)
        for i, child in enumerate(children):
            cx = (x + (i / (n - 1) - 0.5) * w) if n > 1 else x
            cy = y - 1
            plt.plot([x, cx], [y, cy], 'g-')
            draw_node(child, cx, cy, w / n)
        a = node.w / node.n if node.n > 0 else 0
        plt.plot([x], [y], 'bo')
        plt.annotate(str(node.w) + '/' + str(node.n), (x, y + 0.1))
    
    draw_node(node, 0, 0, 2)
    plt.show(block = False)