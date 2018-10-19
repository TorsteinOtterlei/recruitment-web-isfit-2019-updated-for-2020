import boto3
import random
import os
from botocore.exceptions import ClientError

# Hent ut autentiseringsnøkkel
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']

# Adressen må være verifisert i Amazon SES.
SENDER = "ISFiT <noreply@isfit.no>"
RECIPIENT = "gard.steinsvik@isfit.no"

AWS_REGION = "eu-west-1"
CHARSET = "UTF-8"

# The subject line for the email.
SUBJECT = "[AWS][SES][GØY] Amazon SES Test-epost (Sendt fra Python)"

BODY_HTML = """
<html>
    <head></head>
    <body>
        """ + str(random.randint(0, 10)) + """
        <h1>Amazon SES Test-epost (SDK for Python)</h1>
        <p>This email was sent with
        <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
        <a href='https://aws.amazon.com/sdk-for-python/'>
        AWS SDK for Python (Boto)</a>.</p>
        """ + str(random.randint(0, 10)) + """
        <h3>Hilsen Gard :)</h3>
    </body>
</html>
"""

# BODY_TEXT brukes dersom mottakerens epost-klient ikke støtter HTML.
BODY_TEXT = ("Amazon SES Test (Python)\r\n"
             "This email was sent with Amazon SES using the "
             "AWS SDK for Python (Boto)."
             )

client = boto3.client('ses', aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                      region_name=AWS_REGION)

try:
    response = client.send_email(
        Destination={
            'ToAddresses': [
                RECIPIENT,
            ],
            'CcAddresses': [],
            'BccAddresses': []
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
