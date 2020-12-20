"""
do a for loop over data
create a class category_model with name,long_description etc.
do same in service
explain a bit in this script where to save to data base, where to import from data base

"""

import pandas as pd

# The input data could come from a data base. Here because I do not have the know how to build a data base
# I fake it by iterating over the csv file
from model.product import Product
from pseudo_pipeline.product_client import CategoryClient

input_data = "../data/TV & Audio products Data Set - to be assigned to categories.csv"

df = pd.read_csv(input_data, sep="\t")
name_list = df["<Name>"].tolist()
long_description_list = df["Long Description"].tolist()
long_description_mm_list = df["Long Description MM"].tolist()
marketing_text_mm_list = df["Marketing Text MM"].tolist()
short_description_list = df["Short Description"].tolist()
short_description_mm_list = df["Short Description MM"].tolist()
online_status_list = df["Online Status"].tolist()
list_articles = []

for name, long_description, long_description_mm, marketing_text, short_description, short_description_mm, online_status in zip(
        name_list, long_description_list, long_description_mm_list, marketing_text_mm_list, short_description_list,
        short_description_mm_list, online_status_list):
    article = Product(name=name, categories=[], online_status=online_status, long_description=long_description,
                      long_description_mm=long_description_mm,
                      marketing_text_mm=marketing_text, short_description=short_description,
                      short_description_mm=short_description_mm, categories_predicted=[])
    if online_status == "ACTIVE":
        list_articles.append(article)

category_client = CategoryClient()
for i, article in enumerate(list_articles):
    print("x" * 100)
    print(article.short_description,article.long_description_mm)
    article.categories_id = category_client.get_category(article)
    article.categories_names = article.convert_id_2_categories(article.categories_id)
    print("categories predicted", article.categories_names)
    article.categories_parent = article.get_categories_parents()
    article.categories_parent_name = article.convert_id_parents_2_name()
    # save/update article into the database
