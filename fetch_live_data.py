import requests
from dotenv import dotenv_values
import json
from datetime import datetime
import streamlit as st

class Data:
    def __init__(self):
        self.base_url = "https://" + st.secrets["API_HOST"]
        self.headers = {
            "X-RapidAPI-Key": st.secrets["API_KEY"],
            "X-RapidAPI-Host": st.secrets["API_HOST"]
        }
#         self.config = dotenv_values(".env")
#         self.base_url = "https://" + self.config["API_HOST"]
#         self.headers = {
#             "X-RapidAPI-Key": self.config["API_KEY"],
#             "X-RapidAPI-Host": self.config["API_HOST"]
#         }

    def get_matches(self):
        url = self.base_url + "/fixtures-by-series/" + str(self.config["SERIES_ID"])
        response = requests.request("GET", url, headers=self.headers)
        today_matches_id = list()

        for match in response.json()["results"]:
            if (datetime.strptime(match["date"], "%Y-%m-%dT%H:%M:%S+00:00").date() == datetime.today().date()):
                today_matches_id.append(match["id"])

        return today_matches_id
    
    def get_match_details(self, match_id):
        url = self.base_url + "/match/" + str(match_id)
        response = requests.get(url, headers=self.headers)

        return response.json()["results"]
    
