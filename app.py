import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt

def get_data(url):
    response = urllib.request.urlopen(url).read()
    response = json.loads(response)
    return response


def get_trip_updates():
    url = "http://realtime.ripta.com:81/api/tripupdates?format=json"
    return get_data(url)


def get_vehicle_positions():
    url = "http://realtime.ripta.com:81/api/vehiclepositions?format=json"
    return get_data(url)


def get_service_alerts():
    url = "http://realtime.ripta.com:81/api/servicealerts?format=json"
    return get_data(url)

def position_data_to_dataframe(d):
    vehicle_id = []
    trip_id = []
    start_time = []
    start_date = []
    schedule_relationship = []
    route_id = []
    latitude = []
    longitude = []
    bearing = []
    odometer = []
    speed = []
    current_stop_sequence = []
    current_status = []
    timestamp = []
    congestion_level = []
    stop_id = []

    for entity_item in d["entity"]:
        vehicle_id.append(entity_item["vehicle"]["vehicle"]["id"])
        trip_id.append(entity_item["vehicle"]["trip"]["trip_id"])
        start_time.append(entity_item["vehicle"]["trip"]["start_time"])
        start_date.append(entity_item["vehicle"]["trip"]["start_date"])
        schedule_relationship.append(entity_item["vehicle"]["trip"]["schedule_relationship"])
        route_id.append(entity_item["vehicle"]["trip"]["route_id"])
        latitude.append(entity_item["vehicle"]["position"]["latitude"])
        longitude.append(entity_item["vehicle"]["position"]["longitude"])
        bearing.append(entity_item["vehicle"]["position"]["bearing"])
        odometer.append(entity_item["vehicle"]["position"]["odometer"])
        speed.append(entity_item["vehicle"]["position"]["speed"])
        current_stop_sequence.append(entity_item["vehicle"]["current_stop_sequence"])
        current_status.append(entity_item["vehicle"]["current_status"])
        timestamp.append(entity_item["vehicle"]["timestamp"])
        congestion_level.append(entity_item["vehicle"]["congestion_level"])
        stop_id.append(entity_item["vehicle"]["stop_id"])
    df = pd.DataFrame()
    df["vehicle_id"] = vehicle_id
    df["trip_id"] = trip_id
    df["start_time"] = start_time
    df["start_date"] = start_date
    df["schedule_relationship"] = schedule_relationship
    df["route_id"] = route_id
    df["latitude"] = latitude
    df["longitude"] = longitude
    df["bearing"] = bearing
    df["odometer"] = odometer
    df["speed"] = speed
    df["current_stop_sequence"] = current_stop_sequence
    df["current_status"] = current_status
    df["timestamp"] = timestamp
    df["congestion_level"] = congestion_level
    df["stop_id"] = stop_id
    return df


if __name__ == "__main__":
    d = get_vehicle_positions()
    df = position_data_to_dataframe(d)
    df[df.latitude != 0].plot(x="longitude", y="latitude", kind="scatter")
    plt.show()
