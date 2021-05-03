#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   communication.py    
@Github  :   https://github.com/StrikerCC

@Modify Time      @Author       @Version    @Desciption
------------      -------       --------    -----------
5/3/2021 10:54 PM   Cheng Chen    1.0         None
'''

# import lib
import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


class email:
    def __init__(self):
        self.smtpUser = 'chengc0611@163.com'     # email information
        # smtpPass = 'CCws886747'
        self.smtpPass = 'UKQOELRAQBOGKCCN'      # email password

        # destination email information
        self.toAdd = 'chengc0611@gmail.com'


    def send(self, text):
        text = str(text)

        # define time stamp & record an image
        pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
        command = 'raspistill -w 1200 -h 720 -vf -hf -o ' + pic_time + '.jpg'
        os.system(command)

        fromAdd = self.smtpUser
        subject = 'Image recorded at ' + pic_time
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = fromAdd
        msg['To'] = self.toAdd
        msg.preamble = 'Image recorrded at ' + pic_time

        # email text
        body = MIMEText(text + 'Image recorded at ' + pic_time)
        msg.attach(body)

        # attach iamge
        fp = open(pic_time + '.jpg', 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)

        # send email
        s = smtplib.SMTP('smtp.163.com', 25)
        s.ehlo()
        s.starttls()
        s.ehlo()

        s.login(self.smtpUser, self.smtpPass)
        s.sendmail(fromAdd, self.toAdd, msg.as_string())
        s.quit()

        print('Email delivered!')