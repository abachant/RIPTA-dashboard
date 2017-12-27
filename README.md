# RIPTA-dashboard
Visualizing realtime data from RIPTA

## Data Structure
### Vehicle Position Data
A giant dictionary with two keys: "header" and "entity".
"header" is another dictionary that contains metadata.
"entity" is a list of dictionaries.
Each "entity" contains a "vehicle" dictionary with data about a specific bus and location, speed, route etc.

### Trip Updates Data
A giant dictionary with two keys: "header" and "entity".
"header" is another dictionary that contains metadata.
"entity" is a list of dictionaries.
