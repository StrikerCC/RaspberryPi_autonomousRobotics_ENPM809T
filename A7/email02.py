#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   email02.py    
@Github  :   https://github.com/StrikerCC

@Modify Time      @Author       @Version    @Desciption
------------      -------       --------    -----------
4/24/2021 9:36 PM   Cheng Chen    1.0         None
'''

# import lib
import os
from datetime import datetime
import smtplib

def main():
    my_email, my_password = 'groudvehicle.cheng@gmail.com', 'CCws886747'
    recipent = 'chengc0611@gmail.com'
    quote = 'wtf'
    connection = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    connection.ehlo()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(from_addr=my_email,
                        to_addrs=recipent,
                        msg="Subject:Motivational quote\n\n" + quote)
    connection.close()


if __name__ == '__main__':
    main()
