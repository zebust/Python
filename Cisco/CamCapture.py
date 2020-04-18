import requests
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText



def sendemail(url):
    sender_email = "world.of.api@gmail.com"
    receiver_email = "akhan@tdlogicalis.com.au"
    password = "*******"

    email_text = """

    Click on below link to view camera snapshot
    
    %s
     
    """ % (url)

    msg = MIMEText(email_text)

    msg['Subject'] = 'Meraki Camera Capture'
    msg['From'] = 'World of API'
    msg['To'] = 'akhan@tdlogicalis.com.au'


    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(sender_email, password)
        mail.sendmail(sender_email, receiver_email, msg.as_string())
        mail.close()
        input('\n\nCamera link has been sent to akhan@tdlogicalis.com.au \n\n Press any key to exit')

    except  smtplib.SMTPException:
        print ("Error: unable to send email")

    return 0



if __name__ == "__main__":

    api_key = '*************************************'
    api_snapshot_url = 'https://api.meraki.com/api/v0/networks/**************************/cameras/****************/snapshot?timestamp='
    api_video_url = 'https://api.meraki.com/api/v0/networks/**********************/cameras/***************/videoLink?timestamp='
    headers = {'x-cisco-meraki-api-key': api_key,'Content-Type': 'application/json'}


    day_val= int(input('Day: '))
    month_val = int(input('Month: '))
    hour_val = int(input('Hour (24H format): '))
    minute_val = int(input('Minute: '))

    temp = datetime(2020, month_val, day_val, hour_val, minute_val)

    option = int(input('\n\nSelect your Option''\n' + '1: Video Link ' + '\n' + '2: Snapshot ' + '\n' + '>> '))


    if option == 1:
        # Convert time to EPOC milli second format
        timestamp_video = str(temp.timestamp() * 1000)

        #Extract Video URL
        video_api_timestamp = api_video_url + timestamp_video
        video_url = requests.get(video_api_timestamp, headers=headers).json()['url']
        sendemail(video_url)

    elif option == 2:
        # Conver time to iso8601 format and adding 18 hours delta due to timezone difference, only needed for snapshot..... strange..... right!!!!
        delta = 18
        temp2 = temp - timedelta(hours=delta)
        timestamp_snapshot= temp2.isoformat()
        print(timestamp_snapshot)

        # Extract snapshot URL
        snapshot_api_timestamp = api_snapshot_url + timestamp_snapshot
        snapshot_url = requests.post(snapshot_api_timestamp, headers=headers).json()['url']
        sendemail(snapshot_url)
        #print(snapshot_url)

    else:
        input('\n\nYou have enter invalid Entry. \n\nEnter any key to exit')