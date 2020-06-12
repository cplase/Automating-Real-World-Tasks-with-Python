#!/usr/bin/env python3

from PIL import Image
import os
import sys
import logging
import re

def list_files():
    logging.info('Gathering list of files.')
    file_list = [f for f in os.listdir(os.getcwd()) if os.path.isfile(f)]
    logging.debug('Gathered list: {}'.format(str(file_list)))
    return file_list

def verify_images(file_list):
    logging.debug('List received from verify_list function: {}'.format(file_list))
    verified_list = []
    logging.debug('Iterating over file_list {}.'.format(file_list))
    for file in file_list:
        logging.debug('Current file: {}'.format(file))
        try:
            logging.debug('Attempting to open {}...'.format(file))
            im = Image.open(file)
        except IOError:
            logging.error('Cannot open {} as an image!'.format(file))
            continue
        try:
            logging.debug('Verifying {}...'.format(file))
            im.verify()
        except:
            logging.error('Cannot verify {} as an image!'.format(file))
            continue
        logging.info('{} is an image.'.format(file))
        logging.debug('Appending {} to verified_list.'.format(file))
        verified_list.append(file)
        logging.debug('verified_list: {}'.format(str(verified_list)))
    if not verified_list:
        logging.critical('No files are images in this directory! Exiting with code: 1')
        sys.exit(1)
    return verified_list

def rotate_image(im):
    return im.rotate(-90)

def resize_image(im):
    return im.resize((128,128))

def save_as_jpeg(im, im_filename):
    new_file_name = '{}.jpeg'.format((re.search(r'^([\w\-\_]+)', im_filename)).group(0))
    logging.debug('New file name: {}'.format(new_file_name))
    save_location = '/opt/icons/{}'.format(new_file_name)
    logging.debug('Saving file {}'.format(save_location))
    if not os.path.isdir('/opt/icons'):
        os.mkdir('/opt/icons')
    im = im.convert("RGB")
    im.save(save_location, 'JPEG', quality=100)
    if os.path.isfile(save_location):
        logging.debug('File successfully saved!')
        return 0
    logging.error('File did not save successfully!')
    
def main():
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format='%(levelname)s %(asctime)s %(message)s')
    logging.info('Starting script.')
    file_list = list_files()
    image_list = verify_images(file_list)
    for image in image_list:
        im = Image.open(image)
        im_filename = im.filename
        logging.info('Rotating {} clockwise by 90 degrees.'.format(im_filename))
        im = rotate_image(im)
        logging.info('Resizing {} to 128px x 128px resolution.'.format(im_filename))
        im = resize_image(im)
        save_as_jpeg(im, im_filename)
    logging.info('Tasks completed! Exiting script.')
    sys.exit(0)

if __name__ == "__main__":
    main()
