import urllib.request
import json
import pandas as pd
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly.graph_objs import *
import datetime

mapbox_access_token = 'pk.eyJ1IjoiYWJhY2hhbnQiLCJhIjoiY2pjaHZncHJyMnBlMDJxdWo3dDlvN2ZsNyJ9.5iHY-9LLDNum2L7hqHomJw'

plotly.tools.set_credentials_file(username='abachant', api_key='WWLZwB7VhIf7pkNRG9Kr')

app = dash.Dash('RIPTA-App')

# app = dash.Dash(__name__)
# app.layout = html.Div(
#     html.Div([
#         html.H1('Realtime RIPTA Locations'),
#         html.Div(id='live-update-text'),
#         dcc.Graph(id='live-update-graph'),
#         dcc.Interval(
#             id='interval-component',
#             interval=1*1000, # in milliseconds
#             n_intervals=0
#         )
#     ])
# )
#
#
# # Multiple components can update everytime interval gets fired.
# @app.callback(Output('live-update-graph', 'figure'),
#               [Input('interval-component', 'n_intervals')])

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

d = get_vehicle_positions()
df = position_data_to_dataframe(d)

# def postion_dataframe_to_plotly():
    # d = get_vehicle_positions()
    # df = position_data_to_dataframe(d)
    #
    # df.head()
    #
    # df['text'] = df["vehicle_id"]
    #
    # scl = [ [0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],[0.5,"rgb(70, 100, 245)"],\
    # [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],[1,"rgb(220, 220, 220)"] ]
    #
    # data = [ dict(
    #     type = 'scattergeo',
    #     locationmode = 'USA-states',
    #     lon = df['longitude'],
    #     lat = df['latitude'],
    #     text = df['text'],
    #     mode = 'markers',
    #     marker = dict(
    #         size = 8,
    #         opacity = 0.8,
    #         reversescale = True,
    #         autocolorscale = False,
    #         symbol = 'square',
    #         line = dict(
    #             width=1,
    #             color='rgba(102, 102, 102)'
    #         )
    #         ))]
    # layout = dict(
    #     title = 'Current RIPTA Positions<br>(Hover for bus names and routes)',
    #     colorbar = True,
    #     geo = dict(
    #         scope='usa',
    #         projection=dict( type='albers usa' ),
    #         showland = True,
    #         landcolor = "rgb(250, 250, 250)",
    #         subunitcolor = "rgb(217, 217, 217)",
    #         countrycolor = "rgb(217, 217, 217)",
    #         countrywidth = 0.5,
    #         subunitwidth = 0.5
    #         ),
    #     )
    #
    # fig = dict( data=data, layout=layout )
    # url = py.iplot(data, filename='ripta-dashboard', sharing='public')

data = Data([
    Scattermapbox(
        lat=df['latitude'],
        lon=df['longitude'],
        mode='markers',
        marker=Marker(
            size=9
        ),
        text=df['vehicle_id'],
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

fig = dict(data=data, layout=layout)

app.layout = html.Div(children=[
    html.H1(children='Realtime RIPTA Locations'),

    html.Div(children='''
        A Dashboard for all RIPTA vehicles and routes.
    '''),

    dcc.Graph(
        figure=Figure(fig),
            style={'height': 700},
        id='live-update-graph'
        ),
    dcc.Interval(
        id='interval-component',
        interval=1*5000, # in milliseconds
        n_intervals=0
    )
])

# @app.callback(Output('live-update-graph', 'figure'),
#               [Input('interval-component', 'n_intervals')])
#
# def update_graph_live(n):
#     d = get_vehicle_positions()
#     df = position_data_to_dataframe(d)
#
#     return go.Figure(
#     data=[
#         go.Scattergeo(
#             lon=df['longitude'],
#             lat=df['latitude'],
#             name='Buses',
#             hovertext=(df['route_id'] + ", " + df['vehicle_id']),
#             marker=go.Marker(
#                 color='rgb(55, 83, 109)'
#             )
#         )
#     ],
#     layout=go.Layout(
#         title='All Current RIPTA Locations',
#         showlegend=True,
#         legend=go.Legend(
#             x=0,
#             y=1.0
#         ),
#         margin=go.Margin(l=40, r=0, t=40, b=30)
#     )
#     )


if __name__ == "__main__":
    app.run_server(debug=True)
