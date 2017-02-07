import json
import sys
import urllib2
import os
import glob
import imaplib
import email
import time
import globaldata
import commonfunctions as cf
from pageobjectsfrontend import checkout


def login(login, password):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, password)
    return mail


def clean_inbox(mail):
    failed = False
    failure = ""

    mail.select("inbox")
    result, email_data = mail.search(None, "ALL")
    for num in email_data[0].split():
        mail.store(num, '+FLAGS', '\\Deleted')
    mail.expunge()

    # Looping until email clean
    ids = email_data[0]
    first_time = time.time()
    last_time = first_time
    while len(ids) > 0:
        new_time = time.time()
        mail.select("inbox")
        result, email_data = mail.search(None, "ALL")
        ids = email_data[0]
        if new_time - last_time > globaldata.TIMEOUT:
            failed = True
            failure = failure + "Email not expunged within " + str(globaldata.TIMEOUT) + " seconds.\n"
            print("FAILURE: Email not expunged within " + str(globaldata.TIMEOUT) + " seconds.")
            break

    if not failed:
        # print("SUCCESS: Emails successfully expunged.")
        return True

    return [failed, failure]


def validate_email(mail, subject, email_from, validations):

    failed = False
    success = 0

    mail.select("inbox")
    result, email_data = mail.search(None, "ALL")
    ids = email_data[0]
    first_time = time.time()
    last_time = first_time
    while len(ids) == 0:
        new_time = time.time()
        mail.select("inbox")
        result, email_data = mail.search(None, "ALL")
        ids = email_data[0]
        if new_time - last_time > globaldata.TIMEOUTLONG:
            failed = True
            print("FAILURE: Email not received within " + str(globaldata.TIMEOUTLONG) + " seconds.")
            return False

    if not failed:
        id_list = ids.split()
        latest_email_id = id_list[-1]
        result, email_data = mail.fetch(latest_email_id, "(RFC822)")
        raw_email = email_data[0][1]
        email_message = email.message_from_string(raw_email)

        if email_message['Subject'] != subject:
            print("FAILURE: Email subject was not '" + subject + "'.")
            return False

        # get the from address from the received email
        received_from = email.utils.parseaddr(email_message['From'])
        # parseaddr returns a tuple <name, email>

        if received_from[1] == email_from:
            # print("SUCCESS: Validated email from is '" + email_from + "'")
            next
        else:
            print("FAILURE: Email from was not '" + email_from + "'.")
            return False

        try:
            body_text = email_message.get_payload()
            # Check each validation passed in
            for validation in validations:
                if validation in body_text:
                    # print("SUCCESS: Validated email body contained '" + validation + "'.")
                    next
                else:
                    print("FAILURE: Email body did not contain '" + validation + ".")
                    return False

        except Exception, e:
            return False

    return True


def close_email(mail):
    mail.close()
    mail.logout()
