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
        text="yo",
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

# available_routes = [{'label': 'All', 'value': 'All'}]
# for i in df.route_id:
#     available_routes.append({'label': i, 'value': i})

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
        options=[
            {'label': 'All', 'value': 'All'},
            {'label': 'R/L', 'value': '11'},
            {'label': '1', 'value': '1'},
            {'label': '3', 'value': '3'},
            {'label': '6', 'value': '6'},
            # {'label': '8x', 'value': 'MTL'},
            # {'label': '9x', 'value': 'MTL'},
            # {'label': '10x', 'value': 'MTL'},
            # {'label': '12x', 'value': 'MTL'},
            {'label': '13', 'value': '13'},
            {'label': '14', 'value': '14'},
            {'label': '17', 'value': '17'},
            {'label': '18', 'value': '18'},
            {'label': '19', 'value': '19'},
            {'label': '20', 'value': '20'},
            {'label': '21', 'value': '21'},
            {'label': '22', 'value': '22'},
            {'label': '27', 'value': '27'},
            {'label': '28', 'value': '28'},
            {'label': '29', 'value': '29'},
            {'label': '30', 'value': '30'},
            {'label': '31', 'value': '31'},
            {'label': '32', 'value': '32'},
            {'label': '33', 'value': '33'},
            {'label': '34', 'value': '34'},
            {'label': '35', 'value': '35'},
            {'label': '40', 'value': '40'},
            {'label': '49', 'value': '49'},
            {'label': '50', 'value': '50'},
            {'label': '51', 'value': '51'},
            {'label': '54', 'value': '54'},
            {'label': '55', 'value': '55'},
            {'label': '56', 'value': '56'},
            {'label': '57', 'value': '57'},
            {'label': '58', 'value': '58'},
            # {'label': '59x', 'value': 'MTL'},
            {'label': '60', 'value': '60'},
            # {'label': '61x', 'value': 'MTL'},
            {'label': '62', 'value': '62'},
            {'label': '63', 'value': '63'},
            {'label': '64', 'value': '64'},
            # {'label': '65x', 'value': 'MTL'},
            {'label': '66', 'value': '66'},
            {'label': '67', 'value': '67'},
            {'label': '71', 'value': '71'},
            {'label': '72', 'value': '72'},
            {'label': '73', 'value': '73'},
            {'label': '75', 'value': '75'},
            {'label': '76', 'value': '76'},
            {'label': '78', 'value': '78'},
            {'label': '80', 'value': '80'},
            {'label': '87', 'value': '87'},
            {'label': '92', 'value': '92'},
            # {'label': '95x', 'value': 'MTL'}
            ],
        value='All',
        ),
    dcc.Graph(
        figure=Figure(fig),
        style={'height': 800},
        id='live-update-graph'
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
    d = get_vehicle_positions()
    df = position_data_to_dataframe(d)
    try:
        value = int(value)
    except ValueError:
        pass
    print("Route IDs")
    print(df.route_id)
    # print("DF before", df)
    print("Value is", value)
    print("Value type is", type(value))
    if value in df.route_id:
        print("Filtering dataframe")
        df = df[df.route_id == value]
    # print("DF after", df)
    print("DataFrame has", len(df), "rows")
    data = Data([
        Scattermapbox(
            lat=(df['latitude']),
            lon=(df['longitude']),
            mode='markers',
            marker=Marker(
                size=9
            ),
            hovertext=(df['route_id'].astype(str) + ", " + df['vehicle_id']),
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
