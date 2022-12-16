import json
import httplib2 as http
import math

from datetime import datetime, timedelta
from dateutil import parser
from typing import List

from node import post_data
from credentials import LTA_API


class Bus:
    def __init__(self, ServiceNo, NextBus, Latitude, Longtitude):
        self.date = str(datetime.now().date())
        self.time = str(datetime.now().time().replace(microsecond=0))
        self.service_no = ServiceNo
        self.arrival_time = NextBus
        self.latitude = Latitude
        self.longitude = Longtitude

    def update_database(self):
        data = {"date": self.date, "time": self.time, "service_no": self.service_no, "arrival_time": self.arrival_time, "latitude": self.latitude, "longitude": self.longitude}
        post_data(request="APPEND", database="bus_arrival", data=data)


def get_arrival_time(ISO_time):
    if ISO_time:
        time = parser.parse(ISO_time).astimezone()
        time_now = datetime.now().replace(microsecond=0).astimezone()
        arrival_time = (time - time_now).seconds / 60
        
        
        return str(math.ceil(arrival_time)) if arrival_time < 1000 else "Arr"
    else:
        return "-"


def get_coordinates(coordinates):
    latitude, longitude = coordinates["Latitude"], coordinates["Longitude"]

    if latitude == "" and longitude == "" or latitude == "0" and longitude == "0":
        return "None", "None"
    else:
        return str(latitude), str(longitude)


def get_data():
    headers = { 'AccountKey' : LTA_API, 'accept' : 'application/json'}
    target = "http://datamall2.mytransport.sg/ltaodataservice/BusArrivalv2?BusStopCode=12101"
    response, content = http.Http().request(target, "GET", "", headers)
    bus_data = json.loads(content)

    buses:List[Bus] = []

    for bus in bus_data["Services"]:
        service_no = int(bus["ServiceNo"])

        arrival_time_1 = get_arrival_time(bus["NextBus"]["EstimatedArrival"])
        arrival_time_2 = get_arrival_time(bus["NextBus2"]["EstimatedArrival"])
        arrival_time_3 = get_arrival_time(bus["NextBus3"]["EstimatedArrival"])

        arrival_time = [arrival_time_1, arrival_time_2, arrival_time_3]

        latitude_1, longitude_1 = get_coordinates(bus["NextBus"])
        latitude_2, longitude_2 = get_coordinates(bus["NextBus2"])
        latitude_3, longitude_3= get_coordinates(bus["NextBus3"])

        latitude = [latitude_1, latitude_2, latitude_3]
        longitude = [longitude_1, longitude_2, longitude_3]

        buses.append(Bus(service_no, arrival_time, latitude, longitude))
    
    return buses


def update_bus(context):
    buses = get_data()

    post_data(request="DELETE", database="bus_arrival", data="null")

    bus : Bus
    for bus in buses:
        bus.update_database()

    return buses


def buses(update, context):
    chat_id = update.message.chat.id

    buses = get_data()

    bus_text = "<code>-----------------------------</code>\n" \
               "<code> Bus Arrival @ Ngee Ann Poly </code>\n" \
               "<code>-----------------------------</code>\n" \
               "<code> Bus No. :       Time        </code>\n" \
               "<code>-----------------------------</code>\n"

    bus : Bus
    for bus in buses:
        bus_text += f"<code> {bus.service_no:<8}:  {bus.arrival_time[0]:<5} {bus.arrival_time[1]:<5} {bus.arrival_time[2]:<5}</code>\n"

    context.bot.send_message(text=bus_text, chat_id=chat_id, parse_mode="HTML")



