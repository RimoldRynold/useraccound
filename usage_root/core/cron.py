#!/usr/bin/env python

from twilio.rest import Client
from django.conf import settings

TWILIO_ACCOUNT_SID = 'AC7920b6d90fdc17921b35032c86c033dd'
ACCOUNT_API_KEY = 'SK25cf2f8ffc8549e3cdcfc8b69d58d39a'
ACCOUNT_API_SECRET = 'MnNWgeEgpjsyw8L706nO9TNVReNCMriT'

def my_cron_job():
    client = Client(ACCOUNT_API_KEY,ACCOUNT_API_SECRET,TWILIO_ACCOUNT_SID)
    # balance = float(client.api.v2010.balance.fetch().balance)
    balance = 50
    from usage_root.core.models import Notification
    email = Notification.objects.all().email
    print(email)
    currency = client.api.v2010.balance.fetch().currency
    # print(f'Your account has {balance:.2f} {currency} left.')
    # with open('file.txt','a') as file:
    #         file.write(f'Your account has {balance:.2f} {currency} left.\n')
    threshold_balance = [0,10,20,30,50,100,150]
    for value in threshold_balance:
        if value >= balance:
            print(f' balance is below than {value}')
            
    
    
if __name__ == '__main__':
    my_cron_job()
    
    

    
    
    
    
# def my_cron_job():
    # balance = 15.5
    # if balance < 50:
    #     with open('file.txt','a') as file:
    #         file.write('data')
            
