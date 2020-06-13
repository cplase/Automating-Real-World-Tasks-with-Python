#!/usr/bin/env python3

import requests
import sys
import os
import re
import logging

def get_images(cwd):
    files = [f for f in os.listdir(cwd) if os.path.isfile(f)]
    images = []
    for file in files:
        if re.search(r"\.(JPEG|jpeg)$", file) == None:
            continue
        images.append(file)
    return images

def post_images(images, url):
    for image in images:
        logging.debug("Opening {}".format(image))
        with open(image, "rb") as opened:
            logging.debug("Sending POST...")
            response = requests.post(url, files={"file": opened})
            if not response.ok:
                raise Exception("POST failed with status code {}".format(response.status_code))
            logging.debug("Success!")
    return 0

def main(argv):
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(levelname)s %(asctime)s %(message)s')
    url = input("IP Address: ")
    url = "http://{}/upload/".format(url)
    images = get_images(os.getcwd())
    return_code = post_images(images, url)
    sys.exit(return_code)

if __name__ == "__main__":
    main(sys.argv)