import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'usage.settings')
import django
django.setup()
import json

import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from django.conf import settings
from core.models import Notification,Threshold,TwilioApi




threshold_list = []
thresholds = Threshold.objects.all().order_by('-value')
if Notification.objects.all():
    notification = Notification.objects.all()[0]
else:
    notification = ''
    
    
def send_email(threshold_value=None,balance=None,ok_state=None,api_down=None):
            # sender = ''
            receivers = notification.to_user
            email_message =MIMEMultipart()
            email_message['From'] = 'From Raasbot'
            email_message['To'] = receivers
            
            if threshold_value:
                email_message['Subject'] = 'Twilio Account Balance'
                if not ok_state:
                    if balance:
                        body = f"account balance  is below than threshold ${threshold_value} , current balance ${balance}"
                    else:
                        body = f"account balance is equal to threshold ${threshold_value}"
                else:
                    body = f"account balance  is above than threshold ${threshold_value} , current balance ${balance}"
            if api_down:
                email_message['Subject'] = 'Twilio API Down'
                body = f"Reason : {str(api_down)}"
            email_message.attach(MIMEText(body,'plain'))
            text=email_message.as_string()
            smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
            smtpObj.starttls()
            try:
                smtpObj.login(settings.EMAIL_SENDER , settings.SENDER_PASSWORD)
                smtpObj.sendmail(settings.EMAIL_SENDER, receivers, text)
                smtpObj.quit()
            except Exception as e:
                print ("Error: unable to send email")
                
    
def twilio_api_check():
    try:
        
        client = Client(settings.ACCOUNT_API_KEY,settings.ACCOUNT_API_SECRET,settings.TWILIO_ACCOUNT_SID)
        balance = float(client.api.v2010.balance.fetch().balance)
    
    except TwilioRestException as e:
        if TwilioApi.objects.all():
            if  TwilioApi.objects.all()[0].api_status == True:
                
                send_email(api_down=e.msg)
                payload = {"text": f"Twlio API Down due to {e.msg}"}
                message = requests.post(notification.webhook_url,data=json.dumps(payload))
                api_status = TwilioApi.objects.all()[0]
                api_status.api_status = False
                api_status.save()
        else:
            TwilioApi.objects.create(api_status=False)
            send_email(api_down=e.msg)
            payload = {"text": f"Twlio API Down due to {e.msg}"}
            message = requests.post(notification.webhook_url,data=json.dumps(payload))
    except Exception as e:
        print(e)
    
    else:
        if TwilioApi.objects.all():
            api_status=TwilioApi.objects.all()[0]
            api_status.api_status = True
            api_status.balance=balance
            api_status.save()
            
        else:
            TwilioApi.objects.create(api_status=True,balance=balance)
            
        return balance
        
        
        


def my_cron_job():
    if notification:
        #for email notification
        balance=twilio_api_check()
        if balance:
        
            for value in thresholds:
                threshold_list.append(int(value.value))
                
            for threshold_value in threshold_list:
                threshold_notification = Threshold.objects.get(value=threshold_value)
                
                if threshold_value >= balance: 
                    if threshold_value == balance:
                        if not threshold_notification.flag:
                            payload = {"text": f"account balance is equal to threshold ${threshold_value}"}
                            message = requests.post(notification.webhook_url,data=json.dumps(payload))
                        
                    
                            send_email(threshold_value)
                            if message.text == 'ok':
                                threshold_notification.flag = True
                                threshold_notification.save()

                    elif threshold_value > balance:
                        if not threshold_notification.flag:
                            payload = {"text": f"account balance  is below than threshold ${threshold_value} , current balance ${balance}"}
                            message = requests.post(notification.webhook_url,data=json.dumps(payload))
                        
                            
                            send_email(threshold_value,balance)
                            if message.text == 'ok':
                                threshold_notification.flag = True
                                threshold_notification.save()
            
                elif threshold_value < balance:
                    if threshold_notification.flag:
                        payload = {"text": f"account balance  is above than threshold ${threshold_value} , current balance ${balance}"}
                        message = requests.post(notification.webhook_url,data=json.dumps(payload))
        
                        
                        send_email(threshold_value,balance,ok_state=True)
                        if message.text == 'ok':
                            threshold_notification.flag = False
                            threshold_notification.save()

            
    
if __name__ == '__main__':
    my_cron_job()
    
    

            
