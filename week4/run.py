#!/usr/bin/env python3

import os
import requests
import re
import logging
import sys

def get_text_files(directory):
    files = [f for f in os.listdir(directory) if os.path.isfile(f)]
    text_files = []
    for file in files:
        if re.search(r"\.(txt|TXT)$", file) == None:
            continue
        text_files.append(file)
    logging.debug("Returning text_files: {}".format(text_files))
    return text_files

def process_text_files(txt_files, directory):
    json_data = []
    entry_keys = ("name", "weight", "description", "image_name")
    for txt_file in txt_files:
        logging.debug("{}".format(txt_file))
        with open(os.path.join(directory, txt_file), "r") as f:
            entry_template = {}
            content = [line.strip() for line in f.readlines() if line.strip() != ""]
            image_file_name = re.search(r"^(\w+)\.(txt|TXT)$", txt_file)
            image_file_name = image_file_name.group(1)
            logging.debug("{}".format(image_file_name))
            image_file_name = "{}.jpeg".format(image_file_name)
            logging.debug("{}".format(image_file_name))
            content.append(image_file_name)
            logging.debug("{}".format(content))
            for i, entry in enumerate(entry_keys):
                regex_search = re.search(r"^(\d+) lbs$", content[i])
                if regex_search != None:
                    content[i] = regex_search.group(1)
                entry_template[entry] = content[i]
            json_data.append(entry_template)
    logging.debug("Returning json_data: {}".format(json_data))
    return json_data

def post_json_data(json_data, url):
    for entry in json_data:
        logging.debug("Sending {} as json POST request".format(entry))
        response = requests.post(url, json=entry)
        if not response.ok:
            raise Exception("POST failed with status code {}".format(response.status_code))
        logging.debug("POST success!")
    return 0

def main(argv):
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(levelname)s %(asctime)s %(message)s')
    url = "http://{}/fruits/".format(input("IP Address: "))
    logging.debug("Assigning {} as directory".format(os.getcwd()))
    directory = os.getcwd()
    text_files = get_text_files(directory)
    json_data = process_text_files(text_files, directory)
    return_code = post_json_data(json_data, url)
    sys.exit(return_code)

if __name__ == "__main__":
    main(sys.argv)