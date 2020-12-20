import pandas as pd
import networkx as nx

categories_data_path = "../../data/TV & Audio categories Data Set.csv"
categories_df = pd.read_csv(categories_data_path, sep="\t")
children = categories_df["<ID>"].tolist()
parents = categories_df["<Parent ID>"].tolist()
category_names = categories_df["<Name>"]
id_2_name = {str(id_number): name for id_number, name in zip(children, category_names)}
id_2_name["MediaMarkt_DE"] = 0

DiG = nx.from_pandas_edgelist(categories_df, '<ID>', '<Parent ID>', create_using=nx.DiGraph())

categories_tree = {}
for n1 in DiG.nodes():
    for n2 in nx.ancestors(DiG, n1):
        if n1 not in categories_tree.keys():
            categories_tree[n1] = []
            categories_tree[n1].append(n2)
        else:
            categories_tree[n1].append(n2)

list_categories = []
for key, value in categories_tree.items():
    list_categories.append(str(key))
    for v in value:
        list_categories.append(str(v))
list_categories = list(set(list_categories))


def find_parents(child, parent_list):
    if child == "MediaMarkt_DE":
        return parent_list
    child = int(child)
    for pa, ch in zip(parents, children):
        if child == ch:
            parent_list.append(pa)
            return find_parents(pa, parent_list)


def has_no_child(parent):
    for pt, ch in zip(parents, children):
        if pt == parent:
            if ch != pt:
                return False



