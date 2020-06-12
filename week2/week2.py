#!/usr/bin/env python3

import os
import requests
import re
import logging
import sys
import json

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s %(asctime)s %(message)s')

def get_directory_of_files(directory):
    logging.debug('Building list of files in directory {}'.format(directory))
    list_of_files = [f for f in os.listdir(directory) if os.path.isfile('{}/{}'.format(directory, f))]
    logging.debug('List of files in directory: {}'.format(list_of_files))
    if not list_of_files:
        logging.critical('There are no files in the directory {}'.format(directory))
        raise ValueError('There are no files in the directory')
    logging.debug('List of files found: {}'.format(list_of_files))
    return list_of_files

def process_into_dictionary(list_of_f, directory):
    logging.debug('Generating empty dictionary to append responses to')
    response_dict = []
    entry_format = ('title', 'name', 'date', 'feedback')
    logging.debug('Format for review entries: {}'.format(entry_format))
    logging.debug('Iterating over: {}'.format(list_of_f))
    for f in list_of_f:
        logging.debug('Opening {} as a file'.format(f))
        with open('{}/{}'.format(directory, f), 'r') as entry:
            logging.debug('Creating empty dictionary template')
            dict_template = {}
            content = [line.strip() for line in entry.readlines()]
            logging.debug('Content read from file: {}'.format(content))
            logging.debug('Constructing dictionary to append to response_dict')
            for i, entry in enumerate(entry_format):
                logging.debug('Index={} Entry={}'.format(i, entry))
                logging.debug('Adding key={} value={}'.format(entry, content[i]))
                dict_template[entry] = content[i]
            logging.debug('Appending {} to response_dict'.format(dict_template))
            response_dict.append(dict_template)
            logging.debug('Done. Next file')
    logging.debug('response_dict built: {}'.format(response_dict))
    return response_dict

def upload_to_web(response_dict):
    url = 'http://34.72.87.22/feedback/'
    for entry in response_dict:
        response = requests.post(url, json=entry)
        if not response.ok:
            raise Exception('POST failed with status code {}'.format(response.status_code))
        logging.debug('POST succeeded with status code {}'.format(response.status_code))
    return 0

def main():
    logging.debug('Begin script')
    directory = '/data/feedback'
    list_of_files = get_directory_of_files(directory)
    response_dict = process_into_dictionary(list_of_files, directory)
    exit_code = upload_to_web(response_dict)
    logging.debug('Ending script with exit code {}'.format(exit_code))
    sys.exit(exit_code)

if __name__ == "__main__":
    main()