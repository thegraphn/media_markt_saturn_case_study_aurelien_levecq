from model.product_tree import categories_tree


class Category:
    def __init__(self, name, parent, children):
        self.name = name
        self.parent = parent
        self.children = children
        if type(children) == list:
            self.children = self.assign_children(self.children)

    def assign_children(self, children: list):
        list_children = []
        for child in children:
            list_children.append(Category(str(child), parent=self.parent, children=None))
        return list_children

    def assign_parent(self, prt):
        self.parent = prt


m_c = Category("MediaMarkt_DE", None, None)
child_mc = Category("202", m_c, ["203", "205"])

print(child_mc.children[0].name)
print(child_mc.parent.name)

for pt, childrn in categories_tree.items():
    print(pt, childrn)
    m_c.assign_children(childrn)
print(m_c.children)
