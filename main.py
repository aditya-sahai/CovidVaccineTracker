from EmailSender import EmailSender
from DataManager import DataManager

from time import sleep


VaccineData = DataManager()
DataMailSender = EmailSender()

while True:
    available_vaccines = VaccineData.find_available_vaccines()

    if len(available_vaccines) > 0:
        DataMailSender.send_vaccine_mail(available_vaccines)
        print("Sent Vaccines Info!")

    sleep(1800)