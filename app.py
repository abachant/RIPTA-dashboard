import urllib.request
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from plotly.graph_objs import *
import datetime
from operator import itemgetter

mapbox_access_token = 'pk.eyJ1IjoiYWJhY2hhbnQiLCJhIjoiY2pjaHZncHJyMnBlMDJxdWo3dDlvN2ZsNyJ9.5iHY-9LLDNum2L7hqHomJw'

plotly.tools.set_credentials_file(username='abachant', api_key='WWLZwB7VhIf7pkNRG9Kr')

app = dash.Dash('RIPTA-App')

def get_data(url):
    """Retreive data from RIPTA's API"""
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
    """Get relevant data and postion it to a pandas dataframe"""
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
    df.route_id = df.route_id.astype(int)
    df["latitude"] = latitude
    df["longitude"] = longitude
    df["bearing"] = bearing
    df["odometer"] = odometer
    df["speed"] = speed
    df.speed = round(df.speed, 1)
    df["current_stop_sequence"] = current_stop_sequence
    df["current_status"] = current_status
    df["timestamp"] = timestamp
    df["congestion_level"] = congestion_level
    df["stop_id"] = stop_id
    return df

def make_data_frame():
    d = get_vehicle_positions()
    df = position_data_to_dataframe(d)
    return df

df = make_data_frame()

data = Data([
    Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=Marker(
            size=9
        ),
        text="test",
    )
])
layout = Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=dict(
            lat=41.83,
            lon=-71.41
        ),
        pitch=0,
        zoom=10
    ),
)

available_routes = [{'label': 'All', 'value': 'All'}]
available_routes_numeric = []
working_route_list = list(df.route_id)

def search_active_routes(routes, term):
    """Find which bus routes are currently active"""
    is_in=False
    for i in routes:
        if term in i.values():
            is_in=True
            break
        else:
            pass
    return is_in

def all_active_routes():
    """Organize all active routes"""
    for i in working_route_list:
        if i==11 and search_active_routes(available_routes, i) == False:
            available_routes.append({'label': 'R/L', 'value': i})
        elif search_active_routes(available_routes_numeric, i) == False:
            available_routes_numeric.append({'label': i, 'value': i})
        else:
            pass

all_active_routes()

available_routes_numeric = sorted(available_routes_numeric, key=itemgetter('value'))
available_routes = available_routes + available_routes_numeric

fig = dict(data=data, layout=layout)

app.layout = html.Div(children=[
    html.H1(children='Realtime RIPTA Locations'),

    html.Div(children='''
        A Dashboard for all RIPTA vehicles and routes.
        '''),
    html.Hr(),

    html.Label('Choose which bus routes to view'),

    dcc.Dropdown(
        id='route-dropdown',
        options=available_routes,
        value='All',
        ),
    dcc.Graph(
        figure=Figure(fig),
        style={'height': 800},
        id='live-update-graph',
        # adding 'animate=True' here would make for smoother callbacks but unfortunately it is still in beta and breaks our ability to maintain camera's position and zoom
        ),
    dcc.Interval(
        id='interval-component',
        interval=1 * 5000, # reload time in milliseconds
        n_intervals=0
        ),
    dcc.Markdown("Source: Transit API(http://realtime.ripta.com:81/)",
                     className="source"),
])

@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals'),
              Input('route-dropdown', 'value')],
              [State('live-update-graph', 'figure')])

def update_graph_live(n, value, fig):
    """Updates the data being plotted at every n_interval"""
    d = get_vehicle_positions()
    df = position_data_to_dataframe(d)
    try:
        value = int(value)
    except ValueError:
        pass
    if value in df.route_id:
        df = df[df.route_id == value]
    data = Data([
        Scattermapbox(
            lat=(df['latitude']),
            lon=(df['longitude']),
            mode='markers',
            marker=Marker(
                size=9
            ),
            hovertext=(df.route_id.astype(str) + ", " + df.vehicle_id.astype(str) + ", " + df.speed.astype(str) + "mph"),
        )
    ])
    fig["data"] = data
    return fig

external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]


for css in external_css:
    app.css.append_css({"external_url": css})

if __name__ == "__main__":
    app.run_server(debug=True)
