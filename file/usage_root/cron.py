import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'usage.settings')
import django
django.setup()
import json
import requests
from twilio.rest import Client
from django.conf import settings
from core.models import Notification,Threshold


def my_cron_job():
    client = Client(settings.ACCOUNT_API_KEY,settings.ACCOUNT_API_SECRET,settings.TWILIO_ACCOUNT_SID)
    # balance = float(client.api.v2010.balance.fetch().balance)
    currency = client.api.v2010.balance.fetch().currency
    balance = int(200)
    # print(balance)
    email = Notification.objects.all()[0]
    # print(email.to_user)
    threshold_list = []
    threshold = Threshold.objects.all().order_by('-value')
    for value in threshold:
        threshold_list.append(int(value.value))
    # print(threshold_list)
    for threshold_value in threshold_list:
        noti = Threshold.objects.get(value=threshold_value)
        
        if threshold_value >= balance:
                   
            if threshold_value == balance:
                if not noti.flag:
                    payload = {"text": f"account balance is equal to threshold ${threshold_value}"}
                    message = requests.post('https://hooks.slack.com/services/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',data=json.dumps(payload))
                    print(message.text)
                    noti.flag = True
                    noti.save()

            elif threshold_value > balance:
                if not noti.flag:
                    payload = {"text": f"account balance  is below than threshold ${threshold_value} , current balance ${balance}"}
                    message = requests.post('https://hooks.slack.com/services/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',data=json.dumps(payload))
                    print(message.text)
                    noti.flag = True
                    noti.save()
      
        elif threshold_value < balance:
            if noti.flag:
                payload = {"text": f"account balance  is above than threshold ${threshold_value} , current balance ${balance}"}
                message = requests.post('https://hooks.slack.com/services/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',data=json.dumps(payload))
                print(message.text)
                noti.flag = False
                noti.save()

                
                
            
                
        
    
    
    
    

            
    
    
if __name__ == '__main__':
    my_cron_job()
    
    

    
    
    
    
# def my_cron_job():
    # balance = 15.5
    # if balance < 50:
    #     with open('file.txt','a') as file:
    #         file.write('data')
    
#-------------
    # print(f'Your account has {balance:.2f} {currency} left.')
    # with open('file.txt','a') as file:
    #         file.write(f'Your account has {balance:.2f} {currency} left.\n')
    # threshold_balance = [0,10,20,30,50,100,150]
    # for value in threshold_balance:
    #     if value >= balance:
    #         print(f' balance is below than {value}')
    # if balance > 50:
    #     with open('file.txt','a') as file:
    #         file.write('data')
            
