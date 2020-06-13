#!/usr/bin/env python3

import shutil
import psutil
import sys
import time
import socket
import emails
import getpass

def generate_error(subject):
    sender = "automation@example.com"
    recipient = "{}@example.com".format(getpass.getuser())
    body = "Please check your system and resolve the issue as soon as possible."
    attachment = None
    message = emails.generate(sender,recipient, subject, body, attachment)
    emails.send(message)

def check_cpu():
    if psutil.cpu_percent() > 80:
        subject = "Error - CPU usage is over 80%"
        generate_error(subject)

def check_disk():
    # Lower than 20%
    disk = psutil.disk_usage("/")
    available = disk.free / disk.total
    if available < 0.2:
        subject = "Error - Available disk space is less than 20%"
        generate_error(subject)

def check_memory():
    mem_info = dict(psutil.virtual_memory()._asdict())
    if (mem_info["free"] / 125000) < 500:
        subject = "Error - Available memory is less than 500MB"
        generate_error(subject)

def check_host():
    try:
        socket.gethostbyname("localhost")
    except socket.error:
        subject = "Error - localhost cannot be resolved to 127.0.0.1"
        generate_error(subject)

def main(argv):
    while True:
        check_cpu()
        check_disk()
        check_memory()
        check_host()
        time.sleep(60)

if __name__ == "__main__":
    main(sys.argv)