import requests
from datetime import datetime
import json


class DataManager:
    def __init__(self):
        """
        Gets the data and has a method to find if vaccines are available.
        """
        date = str(datetime.now().date()).split("-")
        date = f"{date[2]}-{date[1]}-{date[0]}"
        self.REQ_URL = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=188&date={date}"
        self.data = None

    def get_data(self):
        """
        Returns a dictionary of vaccine availability data.
        """

        str_data = requests.get(self.REQ_URL).content.decode()
        self.data = json.loads(str_data)

        return self.data

    def find_available_vaccines(self):
        """
        Returns a list of vaccines available with their info.
        """

        self.available_vaccines = []

        if not self.data:
            self.get_data()

        for center in self.data["centers"]:
            for session in center["sessions"]:
                if session["available_capacity"] > 0:
                    vaccine_data = {
                        "center-name": center["name"],
                        "address": center["address"],
                        "date": session["date"],
                        "slots": session["slots"],
                        "min-age": session["min_age_limit"],
                        "vaccine-name": session["vaccine"],
                        "available-dose-1": session["available_capacity_dose1"],
                        "available-dose-2": session["available_capacity_dose2"],
                    }
                    # print(json.dumps(vaccine_data, indent=4))
                    self.available_vaccines.append(vaccine_data)

        return self.available_vaccines


if __name__ == "__main__":
    Manager = DataManager()
    data = Manager.get_data()
    available_vaccines = Manager.find_available_vaccines()
    print(json.dumps(available_vaccines, indent=4))