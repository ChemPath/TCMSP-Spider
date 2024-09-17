#!/usr/local/bin/python3
# -*- encoding: utf-8 -*-

import os
from tcmsp import TcmspSpider

def get_herb_data():
    """
    Search for herbs to be queried and download data.
    :return: None
    """
    tcmsp = TcmspSpider()

    # Construct the full path to herb_list.txt
    herb_list_path = os.path.join("C:\\Users\\Dr. Contessa Petrini\\ChemPath\\TCMSP-Spider", "herb_list.txt")

    # Build the herb list
    herb_list = []
    try:
        with open(herb_list_path, "r", encoding="utf-8") as f:
            for line in f:
                herb_list.append(line.strip())
    except FileNotFoundError:
        print(f"Error: The file {herb_list_path} was not found.")
        return

    print(f"共有{len(herb_list)}个药物需要查询！\n")

    tcmsp.token = tcmsp.get_token()

    # Iterate over the herbs to query
    for herb in herb_list:
        if herb == "":
            continue

        herb_three_names = tcmsp.get_herb_name(herb)

        # Check if herb_three_names is None or empty
        if not herb_three_names:
            print(f"No data found for herb: {herb}. Skipping...\n")
            continue

        # If multiple herbs are found, download each
        for name in herb_three_names:
            herb_cn_name = name["herb_cn_name"]
            herb_en_name = name["herb_en_name"]
            herb_pinyin_name = name["herb_pinyin"]
            tcmsp.get_herb_data(herb_cn_name, herb_en_name, herb_pinyin_name)

if __name__ == "__main__":
    get_herb_data()
