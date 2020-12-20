from collections import defaultdict
from typing import Any, Tuple
import csv
import pandas as pd

from model.product_tree import find_parents, has_no_child

list_accepted_labels = ["802",
                        "8021",
                        "8022",
                        "8023",
                        "8024",
                        "4036",
                        "777",
                        "2668",
                        "2669",
                        "779",
                        "4100",
                        "4200",
                        "202",
                        "203",
                        "204",
                        "205",
                        "206",
                        "213",
                        "696",
                        "898",
                        "789",
                        "20566",
                        "207",
                        "208",
                        "209",
                        "210",
                        "211",
                        "212",
                        "691",
                        "3678",
                        "3122",
                        "6557",
                        "4500",
                        "1815",
                        "4888",
                        "214",
                        "215",

                        "216",
                        "217",
                        "218",
                        "219",
                        "220",
                        "221",
                        "222",
                        "223",
                        "224",
                        "225",
                        "226",
                        "227",
                        "228",
                        "787",
                        "229",
                        "230",
                        "231",
                        "232",
                        "233",
                        "234",
                        "235",
                        "236",
                        "237",
                        "240",
                        "692",
                        "2850",
                        "11234",
                        "2567",
                        "238",
                        "239",
                        "10040",
                        "241",
                        "242",
                        "243",
                        "244",
                        "245",
                        "246",
                        "3501",
                        "247",
                        "248",
                        "249",
                        "250",
                        "3500",
                        "4300",
                        "251",
                        "252",
                        "253",
                        "254",
                        "255",
                        "256",
                        "257",
                        "258",
                        "788",
                        "765",
                        "4561",

                        "259",
                        "260",
                        "261",
                        "262",
                        "263",
                        "264",
                        "265",
                        "266",
                        "267",
                        "268",
                        "269",
                        "784",
                        "270",
                        "271",
                        "272",
                        "273",
                        "274",
                        "275",
                        "276",
                        "277",
                        "278",
                        "279",
                        "280",
                        "281",
                        "283",
                        "290",
                        "282",
                        "284",
                        "1629",
                        "285",
                        "286",
                        "287",
                        "289",
                        "292",
                        "4211",
                        "288",
                        "291",
                        "293",
                        "294",
                        "295",
                        "296",
                        "297",
                        "298",
                        "299",
                        "300",
                        "301",
                        "302",
                        "303",
                        "304",
                        "305",
                        "306",
                        "307",
                        "308",
                        "309",
                        "310",
                        "311",
                        "312",
                        "313",
                        "314",
                        "315",
                        "749",
                        "750",
                        "5698",
                        "1993",
                        "316",
                        "317",
                        "318",
                        "319",
                        "320",
                        "321",
                        "322",
                        "323",
                        "324",
                        "325",
                        "326",
                        "327",
                        "328",
                        "329",
                        "330",
                        "331",
                        "332",
                        "333",
                        "10039",
                        "334",
                        "335",
                        "336",
                        "337",
                        "338",
                        "340",
                        "342",
                        "810",
                        "1476",
                        "343"
                        ]
texts = []
labels = []
texts_not_full = []
labels_not_full = []
list_found_labels = []
c = 0


def write_data_set_to_file(output_file: str, txts: list, lbls: list, one_label: bool):
    headers = ["text", "label"]
    with open(output_file, "w", encoding="utf-8") as o:
        csv_writer = csv.writer(o, delimiter="\t")
        csv_writer.writerow(headers)
        for text, label in zip(txts, lbls):
            if not one_label:
                if type(label) == str:
                    label = ";".join(label)
                    label = str(label)
                    label = label.replace(";", ",")  # for farm
                label = ",".join(label)
            if one_label:
                pass
            csv_writer.writerow([text, label])


def create_text_labels(file_path: str, one_label: bool) -> Tuple[list, list]:
    df = pd.read_csv(file_path, sep="\t")

    name_list = df["<Name>"].tolist()
    label_list = df["Category Relation Classification Reference"].tolist()
    long_description_list = df["Long Description"].tolist()
    long_description_mm_list = df["Long Description MM"].tolist()
    marketing_text_mm_list = df["Marketing Text MM"].tolist()
    short_description_list = df["Short Description"].tolist()
    short_description_mm_list = df["Short Description MM"].tolist()
    online_status_list = df["Online Status"].tolist()

    name_labels = defaultdict(list)
    for name, long_description, long_description_mm, marketing_text, short_description, short_description_mm, online_status, label in zip(
            name_list, long_description_list, long_description_mm_list, marketing_text_mm_list, short_description_list,
            short_description_mm_list, online_status_list, label_list):
        text = " ".join(name) + "[SEP]"
        if type(short_description) == str and len(short_description) > 5 and short_description not in name:
            text += short_description + " [SEP] "

        if type(long_description) == str and len(long_description) > 5:
            text += long_description + " [SEP] "
        if type(long_description_mm) == str and len(long_description_mm) > 5:
            text += long_description_mm + " [SEP] "

        if type(marketing_text) == str and len(marketing_text) > 5 and marketing_text not in name:
            text += marketing_text + " [SEP] "
        if not one_label:
            if type(label) != float:  # skip => no label(s) for the article
                label_split = []
                if type(label) == str:
                    label_split = label.split(";")
                if type(label) == list:
                    label_list = label
                label = []
                for ll in label_split:
                    if ll in list_accepted_labels:
                        label.append(ll)
                        list_found_labels.append(ll)
                if len(label) > 0:
                    labels.append(label)
                    texts.append(text.replace("\n", ""))

        if one_label:
            if type(label) != float:
                label_split = label.split(";")

                for ll in label_split:
                    if ll in list_accepted_labels:

                        has_child = has_no_child(ll)
                        if not has_child:
                            labels.append(ll)
                            texts.append(text.replace("\n", ""))
    return labels, texts
