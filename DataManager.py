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
        self.req_data = None

        self.DISCTRICT_ID_FILE_NAME = "district-id.json"

    def get_data(self):
        """
        Returns a dictionary of vaccine availability data.
        """

        str_data = requests.get(self.REQ_URL).content.decode()
        self.req_data = json.loads(str_data)

        return self.req_data

    def find_available_vaccines(self):
        """
        Returns a list of vaccines available with their info.
        """

        self.available_vaccines = []

        if not self.req_data:
            self.get_data()

        for center in self.req_data["centers"]:
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

    def save_district_ids(self):
        """
        Makes a json file which has district names and their id's.
        """

        id_num = 0
        district_id_data = []
        invalid_district_id_counter = 0

        while True:
            data = json.loads(requests.get(f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={id_num}&date=02-06-2021").content.decode())
            invalid_district_id_counter += 1

            if len(data["centers"]) > 0:
                name = data["centers"][0]["district_name"]
                district_data = {
                    "name": name,
                    "id": id_num,
                }
                district_id_data.append(district_data)
                invalid_district_id_counter = 0
                print(f'{id_num} - {name}')

            if invalid_district_id_counter >= 50:
                break

            id_num += 1

        with open(self.DISCTRICT_ID_FILE_NAME, "w") as id_f:
            json.dump(district_id_data, id_f, indent=4)

if __name__ == "__main__":
    Manager = DataManager()
    Manager.save_district_ids()
