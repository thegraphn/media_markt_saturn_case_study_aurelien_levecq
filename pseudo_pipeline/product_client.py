import json
import requests
from model.product import Product


class CategoryClient:
    def __init__(self):
        self._host = "0.0.0.0"
        self._port = 8810

        self._request_url = 'http://{}:{}/api/'.format(self._host, self._port)

    def get_category(self, product: Product):
        data = {"name": product.name,
                "short_description": product.short_description,
                "short_description_mm": product.short_description_mm,
                "long_description": product.long_description,
                "long_description_mn": product.long_description_mm,
                "marketing_text_mm": product.marketing_text_mm
                }
        result = requests.post("{}inference".format(self._request_url), json=data)

        res_dict = json.loads(result.text)
        categories = res_dict["results"]["predicted_categories"]
        return categories
