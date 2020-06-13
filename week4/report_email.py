#!/usr/bin/env python3

import os
import re
import datetime
import reports
import sys
import emails
import getpass

def get_directory(argv):
    directory = argv[1]
    if os.path.isdir(directory):
        return os.path.abspath(directory)
    return os.getcwd()

def get_txt_files(directory):
    files = [os.path.join(directory, f)
    for f in os.listdir(directory)
    if os.path.isfile(os.path.join(directory, f))
    ]
    for file in files:
        re_result = re.search(r"\.(txt|TXT)$", file)
        if re_result == None:
            files.remove(file)
    return files

def process_txt_files(files):
    data = ""
    for txt in files:
        with open(txt, "r") as f:
            content = [line.strip() for line in f.readlines() if line.strip() != ""]
            data = "{}name: {}<br/>weight: {}<br/><br/>".format(data, content[0], content[1])
    return data

def main(argv):
    directory = get_directory(argv)
    txt_files = get_txt_files(directory)
    data = process_txt_files(txt_files)
    report_name = "/tmp/processed.pdf"
    current_date = datetime.date.today()
    current_date = current_date.strftime("%B %d, %Y")
    report_title = "Processed Update on {}".format(current_date)
    reports.generate(report_name, report_title, data)
    sender = "automation@example.com"
    recipient = "{}@example.com".format(getpass.getuser())
    subject = "Upload Completed - Online Fruit Store"
    body = "All fruits are uploaded to our website successfully. A detailed list is attached to this email."
    email = emails.generate(sender, recipient, subject, body, report_name)
    emails.send(email)

if __name__ == "__main__":
    main(sys.argv)