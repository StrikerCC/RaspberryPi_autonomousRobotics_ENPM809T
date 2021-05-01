import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def main():
    # define time stamp & record an image
    pic_time = datetime.now().strftime('%Y%m%d%H%M%S')
    command = 'raspistill -w 1200 -h 720 -vf -hf -o ' + pic_time + '.jpg'
    os.system(command)
    
    # email information
    smtpUser = 'chengc0611@163.com'
    # smtpPass = 'CCws886747'
    smtpPass = 'UKQOELRAQBOGKCCN'

    # destination email information
    toAdd = 'chengc0611@gmail.com'
    fromAdd = smtpUser
    subject = 'Image recorded at ' + pic_time
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = fromAdd
    msg['To'] = toAdd
    msg.preamble = 'Image recorrded at ' + pic_time

    # email text 
    body = MIMEText('Image recorded at ' + pic_time)
    msg.attach(body)

    # attach iamge
    fp = open(pic_time + '.jpg', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    # send email 
    s = smtplib.SMTP('smtp.163.com', 465)
    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser, smtpPass)
    s.sendmail(fromAdd, toAdd, msg.as_string())
    s.quit()
    
    print('Email delivered!')


if __name__ == '__main__':
    main()

