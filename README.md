# RIPTA-dashboard
Visualizing realtime data from RIPTA's API using Dash.  

PRs Welcome!  

An example of the interface:  
<img src="https://i.imgur.com/yyCFtfQ.png" alt="closeup of hovertext">  

An animation sped up for effect:  
<img src="https://i.imgur.com/TEcu88o.gif" alt="animation of RIPTA-dashboard">

## Requirements
### Accounts
* [Plotly](https://plot.ly/accounts/login/?action=login)
* [Mapbox](https://www.mapbox.com/signin/)

### Python Packages
* pandas
* numpy
* matplotlib
* plotly
* dash
* dash_core_components
* dash_html_components

## Instructions
### Setting Up Credentials
1. If you don't already have one, setup an account with [Plotly](https://plot.ly/accounts/login/?action=login) and with [Mapbox](https://www.mapbox.com/signin/).
2. Copy `config-template.json` to `config.json`:
    * `cp config-template.json config.json`
3. In `config.json` add in your [Plotly username and API Key](https://plot.ly/settings/api) and your [Mapbox access token](https://www.mapbox.com/account/).

### Running Locally
1. run `python app.py`
2. press `control + c` to terminate

## Data Structure
### Vehicle Position Data
A dictionary with two keys: "header" and "entity".
"header" is another dictionary that contains metadata.
"entity" is a list of dictionaries.
Each "entity" contains a "vehicle" dictionary with data about a specific bus and location, speed, route etc.

### Trip Updates Data
A dictionary with two keys: "header" and "entity".
"header" is another dictionary that contains metadata.
"entity" is a list of dictionaries.
Each "entity" is dictionary whose value is a list of other dictionaries, each of which contains data about a specific bus route including it stops and their delay times and the particular bus (vehicle_id) that is on the route.  

## Dash
Learn more about [Dash](https://plot.ly/dash/).  

View their [documentation](https://github.com/plotly/dash).
