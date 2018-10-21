import boto3
import random
import os
from botocore.exceptions import ClientError
from jobs.models import Interview
from accounts.models import *

def send_email(user):
    # Hent ut autentiseringsnøkler
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']


    the_interview = Interview.objects.get(applicant=user)

    contact_phone = ""
    if the_interview.first.phone_number != None:
        contact_phone = str(the_interview.first.phone_number)

    # Adressen må være verifisert i Amazon SES.
    SENDER = "ISFiT <apply@isfit.no>"
    RECIPIENT = the_interview.applicant.email

    AWS_REGION = "eu-west-1"
    CHARSET = "UTF-8"

    # The subject line for the email.
    SUBJECT = "Interview ISFiT 2019"

    BODY_HTML = """
    <html>
        <head></head>
        <body>
            <h2>Hi, """ + str(user.get_full_name()) + """!</h2>
            <h3>Thanks for your application to ISFiT 2019.
            We have scheduled you for the following interview:</h3>
            <h4>Time:</h4> <p>""" + str(the_interview.pretty_interview_time()) + """</p>
            <h4>Place:</h4> <p>""" + str(the_interview.room) + """</p>
            <h3>IMPORTANT!</h3>
            <p>Tip: download the Mazemap app so you can easily find the room you'll be meeting in.</p>
            <p>Phone number to interviewer: """ + contact_phone + """.</p>
            <p>Good luck at your interview -- we look forward to meeting you!</p>
        </body>
    </html>
    """

    # BODY_TEXT brukes dersom mottakerens epost-klient ikke støtter HTML.
    BODY_TEXT = ("Hi, " + str(user.get_full_name()) + "!\r\n "
                "Thanks for your application to ISFiT 2019."
                "We have scheduled you for the following interview:"
                "Room: " + str(the_interview.room) +""
                "Time: " + str(the_interview.pretty_interview_time()) +""
                "IMPORTANT!"
                "Tip: download the Mazemap app so you can easily find the room you'll be meeting in."
                "Phone number to interviewer: " + contact_phone +"."
                "Good luck at your interview -- we look forward to meeting you!")


    client = boto3.client('ses',  aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          region_name=AWS_REGION)


    if the_interview.first != None and the_interview.second != None and the_interview.third != None:
        bcc_list = [str(the_interview.first.email), str(the_interview.second.email), str(the_interview.third.email)]
    elif the_interview.first != None and the_interview.second == None and the_interview.third != None:
        bcc_list = [str(the_interview.first.email), str(the_interview.third.email)]
    else:
        bcc_list = [str(the_interview.first.email), str(the_interview.second.email)]



    try:
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
                'CcAddresses': [],
                'BccAddresses': bcc_list
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])
