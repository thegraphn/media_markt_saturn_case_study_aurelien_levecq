# -*- coding: utf-8 -*-

"""
Predict categories for a product
"""
from typing import Dict
from farm.infer import Inferencer


class CategoryPredictor:

    def __init__(self):
        self.save_dir = "category_model/"
        self.model = Inferencer.load(self.save_dir, gpu=False, task_type="text_classification",
                                     disable_tqdm=True, use_fast=True)

    def run(self, name: str, short_description_text: str, short_description_mm_text: str, long_description_text: str,
            long_description_mn_text: str, marketing_text_mm_text: str) -> Dict[str, str]:

        input_text = self.pre_processing(name, short_description_text, short_description_mm_text, long_description_text,
                                         long_description_mn_text, marketing_text_mm_text)

        return {"predicted_categories": self.predict(input_text), "input_text": input_text}

    def predict(self, text: str) -> list:
        texts_to_be_predicted = [{"text": text}]

        result = self.model.inference_from_dicts(dicts=texts_to_be_predicted)
        predictions = []
        for batch in result:
            for x in batch["predictions"]:
                prediction = x["label"]
                label = prediction.replace('"', "")
                label = label.replace("[", "")
                label = label.replace("]", "")
                label = label.replace("'", "")
                label = label.replace(" ", "")
                labels = label.split(",")
                predictions.append(labels)
        return predictions[0]  # we return the first prediction, as we have only 1 element in the batch

    @staticmethod
    def pre_processing(name: str, short_description_text: str, short_description_mm_text: str,
                       long_description_text: str,
                       long_description_mn_text: str, marketing_text_mm_text: str) -> str:
        """
        Prepare the input string to feed into the model
        :param marketing_text_mm_text:
        :param long_description_mn_text:
        :param long_description_text:
        :param short_description_mm_text:
        :param name: Input string of the product's name
        :param short_description_text: Input string of the product's short description
        :return:
        """
        text = " ".join(name) + "[SEP]"
        if type(short_description_text) == str and len(short_description_text) > 5 and short_description_text not in name:
            text += short_description_text + " [SEP] "

        if type(long_description_text) == str and len(long_description_text) > 5:
            text += long_description_text + " [SEP] "
        if type(long_description_mn_text) == str and len(long_description_mn_text) > 5:
            text += long_description_mn_text + " [SEP] "

        if type(marketing_text_mm_text) == str and len(marketing_text_mm_text) > 5 and marketing_text_mm_text not in name:
            text += marketing_text_mm_text + " [SEP] "

        return text
