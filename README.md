# RIPTA-dashboard
Visualizing realtime data from RIPTA's API using Dash.  

PRs Welcome!  

[Imgur](https://i.imgur.com/yyCFtfQ.png)  

[Imgur](https://i.imgur.com/TEcu88o.gifv)

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
