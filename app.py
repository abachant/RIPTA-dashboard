import urllib.request
import json


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


if __name__ == "__main__":
    pass
