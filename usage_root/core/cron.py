#!/usr/bin/env python
from twilio.rest import Client
from django.conf import settings
import os



def my_cron_job():
    balance = 15.5
    if balance < 50:
        with open('file.txt','a') as file:
            file.write('data')
            
