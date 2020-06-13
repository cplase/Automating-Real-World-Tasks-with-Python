#!/usr/bin/env python3

from PIL import Image
import os
import sys
import logging
import re

def process_images(files):
    """Accepts a list of files and process them."""
    if not files:
        raise ValueError("There are no images in the directory")
    logging.debug("Iterating over list of files")
    for file in files:
        try:
            logging.debug(
                "Attmpting to process {}...".format(file)
            )
            im = Image.open(file)
            im.verify()
        except:
            logging.debug("File is not an image")
            continue
        logging.debug("File is an image")
        save_location = "~/supplier-data/images"
        new_file_name = os.path.join(
            save_location,
            "{}.jpeg".format(
                (re.search(r'^([\w\-\_]+)', im.filename)).group(0))
        )
        logging.debug("Converting {} to RGB and resizing to 600px by 400px".format(im.filename))
        im = im.resize((600, 400))
        im = im.convert("RGB")
        logging.debug("Saving new image {}".format(new_file_name))
        im.save(new_file_name, "JPEG", quality=100)

def process_files(directory):
    """Lists files in the given directory and returns a list of
    image file locations.
    """
    logging.debug("Gathering list of files")
    files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
        ]
    logging.debug("List of files in directory: {}".format(files))
    if not files:
        raise ValueError("There are no files in the directory")
    process_images(files)

def check_directory(argv):
    """Checks the argument, validates it is a valid directory, and then
    returns said directory.
    If the argument doesn't exist (or isn't valid), then the
    the current working directory is returned.
    """
    logging.debug("Setting directory to current working directory")
    directory = os.getcwd()
    logging.debug("Checking if an argument was given to the script")
    if len(argv) > 1:
        logging.debug("Arguments found")
        logging.debug(
            "Checking if the first argument is a valid directory"
            )
        if os.path.isdir(argv[1]):
            logging.debug("First argument is a valid directory")
            logging.debug(
                "Assigning first argument as directory variable: {}".format(
                    argv[1]
                    )
                )
            directory = argv[1]
    return directory
    
def main(argv):
    """Set log level to DEBUG, stream logs to STDOUT, and format the
    the logs using the following format:

    %(levelname)s %(asctime)s %(message)s
    """
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(levelname)s %(asctime)s %(message)s')
    logging.debug("Starting script")
    directory = check_directory(argv)
    process_files(directory)

if __name__ == "__main__":
    main(sys.argv)