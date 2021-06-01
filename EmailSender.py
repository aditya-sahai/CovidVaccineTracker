import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from json import load


class EmailSender:
    def __init__(self):
        """
        Sends email.
        """
