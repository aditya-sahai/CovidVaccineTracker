import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from json import load


class EmailSender:
    def __init__(self):
        """
        Sends email.
        """
        with open("credentials.json", "r") as creds_f:
            credentials = load(creds_f)

        self.SENDER_MAIL_ADDR = credentials["email-address"]
        self.SENDER_PASS = credentials["password"]
        self.RECEIVER_ADDR = "receiver-addr@gmail.com"

    def get_mail_content(self, available_vaccines_list):
        """
        Returns a str of available vaccines.
        """
        mail_content = "\n---------Available Vaccines----------\n\n"

        for vaccine in available_vaccines_list:

            available_slots = ""
            for slot in vaccine["slots"]:
                available_slots += f"\t{slot}\n"

            line = f"\n{vaccine['vaccine-name']} available at {vaccine['center-name']}.\nDetails\nDate: {vaccine['date']}\nAvailable Dose 1: {vaccine['available-dose-1']}\nAvailable Dose 2: {vaccine['available-dose-2']}\nMinimum Age: {vaccine['min-age']}\nAvailable Slots:\n{available_slots}\n\n"

            mail_content += line

        return mail_content

    def send_vaccine_mail(self, available_vaccines_list):
        """
        Sends a mail from the available vaccines list obtained from DataManager.
        """

        message = MIMEMultipart()
        message["From"] = self.SENDER_MAIL_ADDR
        message["To"] = self.RECEIVER_ADDR
        message["Subject"] = "Available COVID Vaccines In Gurgaon."
        mail_content = self.get_mail_content(available_vaccines_list)
        message.attach(MIMEText(mail_content, "plain"))

        session = smtplib.SMTP("smtp.gmail.com", 587)
        session.starttls()
        session.login(self.SENDER_MAIL_ADDR, self.SENDER_PASS)
        text = message.as_string()
        session.sendmail(self.SENDER_MAIL_ADDR, self.RECEIVER_ADDR, text)
        session.quit()


if __name__ == "__main__":
    from DataManager import DataManager
    data = DataManager()
    data = data.find_available_vaccines()
    Sender = EmailSender()
    Sender.send_vaccine_mail(data)
