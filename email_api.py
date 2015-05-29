import json
import sys
import urllib2
import os
import glob
import imaplib
import email
import time

import globaldata, commonfunctions
from pageobjectsfrontend import checkout



#Email variables
EMAIL_NOREPLY = "noreply@feepay.com"
EMAIL_SUBJECT = "TIES Test District, #987 TEST FeePay Receipt"
CC = "Credit card"
CHECKING = "Checking"
SAVINGS = "Savings"



def build_validation_array(customer, conf_num):
        
    items = customer.cart_items
    total = checkout.get_total(items)
    fullname = customer.fullname
    payment_type = customer.payment_type
    account = customer.account
    ccnum = customer.ccnum
    
    validation = []
    validation.append("Total: " + total)
    validation.append("Name: " + fullname)
    validation.append(conf_num)
    
    if payment_type == CHECKING:
        validation.append("Method: Checking ****" + account[-4:])
    elif payment_type == SAVINGS:
        validation.append("Method: Savings ****" + account[-4:])
    else:
        cc_type = checkout.get_cc_type(ccnum)
        validation.append("Method: " + cc_type + " ****" + ccnum[-4:])
    
    for item in items:        
        validation.append("What: " + item[0] + "\r\nAmount: " + item[1])
        
    return validation
        
        


def login(login):
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(login, globaldata.EMAILPASS)
    return mail



def clean_inbox(mail):
    failed = False
    failure = ""

    print("Cleaning email inbox...")
    
    mail.select("inbox")
    result, email_data = mail.search(None, "ALL") 
    for num in email_data[0].split():
        mail.store(num, '+FLAGS', '\\Deleted')
    mail.expunge() 
    
    #Looping until email clean   
    ids = email_data[0]    
    first_time = time.time()
    last_time = first_time   
    while len(ids) > 0: 
        new_time = time.time()
        mail.select("inbox")
        result, email_data = mail.search(None, "ALL")     
        ids = email_data[0]         
        if  new_time - last_time > globaldata.TIMEOUT:
            failed = True
            failure = failure + "Email not expunged within " + str(globaldata.TIMEOUT) + " seconds.\n"
            print("FAILURE: Email not expunged within " + str(globaldata.TIMEOUT) + " seconds.")
            break 

    if not failed:
        print("SUCCESS: Emails successfully expunged.")

    return [failed, failure]



def validate_email(mail, validations):   
    
    failed = False
    failure = ""
    subject_validation = EMAIL_SUBJECT
    email_from = EMAIL_NOREPLY     

    print("Looping inbox until mail received...")
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
        if  new_time - last_time > globaldata.TIMEOUT:
            failed = True
            failure = failure + "Email not received within " + str(globaldata.TIMEOUT) + " seconds.\n"
            print("FAILURE: Email not received within " + str(globaldata.TIMEOUT) + " seconds.")
            break    
    
    if not failed: 
        id_list = ids.split()   
        latest_email_id = id_list[-1]    
        result, email_data = mail.fetch(latest_email_id, "(RFC822)")   
        raw_email = email_data[0][1]
        email_message = email.message_from_string(raw_email)               
                
        if email_message['Subject'] == subject_validation:
            print("SUCCESS: Validated email subject is '" + subject_validation + "'")
        else:
            failed = True
            failure = failure + "Email subject was not '" + subject_validation + "'.\n"
            print("FAILURE: Email subject was not '" + subject_validation + "'.")

        if email_message['From'] == email_from:
            print("SUCCESS: Validated email from is '" + email_from + "'")
        else:
            passed = 1
            failure = failure + "Email from was not '" + email_from + "'.\n"
            print("FAILURE: Email from was not '" + email_from + "'.")        
        

        try:
            body_text = email_message.get_payload()[0].as_string()
            
            #Check each validation passed in
            for validation in validations:              
                if validation in body_text:
                    print("SUCCESS: Validated email body contained '" + validation + "'.")
                else:
                    failed = True
                    failure = failure + "Email body did not contain '" + validation + ".\n"
                    print("FAILURE: Email body did not contain '" + validation + ".")
                
        except Exception, e:
            failed = True
            failure = failure + "Exception in getting payload for '"
            failure = failure + json_type + ": " + e

    return [failed, failure]
                
                
   
def close_email(mail): 
    mail.close()
    mail.logout()


