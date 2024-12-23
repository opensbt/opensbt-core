import json
import os
from extract.create_so import append_scenario_object
from extract.create_start import StartPosition, append_start_position
from extract.create_wp import ManeuverGroup, Waypoint, append_maneuver_group
from extract.update_env import update_paths
from opensbt.simulation.simulator import SimulationOutput


# simout = {
#     "simTime": 10,  # Total simulation time (seconds)
#     "times": [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0],  # Time steps (1 second intervals)
#     "location": {
#         "ego": [
#             [0.0, 0.0], [0.1, 0.1], [0.2, 0.2], [0.3, 0.3], [0.4, 0.4],
#             [0.5, 0.5], [0.6, 0.6], [0.7, 0.7], [0.8, 0.8], [0.9, 0.9]  # Position data for ego (x, y)
#         ],
#         "adversary": [
#             [10.0, 0.0], [9.9, 0.1], [9.8, 0.2], [9.7, 0.3], [9.6, 0.4],
#             [9.5, 0.5], [9.4, 0.6], [9.3, 0.7], [9.2, 0.8], [9.1, 0.9]  # Position data for adversary (x, y)
#         ]
#     },
#     "velocity": {
#         "ego": [
#             [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0],
#             [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0], [1, 1, 0]  # Velocity data for ego (vx, vy, vz)
#         ],
#         "adversary": [
#             [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0],
#             [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]  # Velocity data for adversary (vx, vy, vz)
#         ]
#     },
#     "speed": {
#         "ego": [1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4, 1.4],  # Speed magnitude for ego
#         "adversary": [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]  # Speed magnitude for adversary
#     },
#     "acceleration": {
#         "ego": [0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Acceleration for ego
#         "adversary": [0.05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Acceleration for adversary
#     },
#     "yaw": {
#         "ego": [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5],  # Heading for ego (in radians)
#         "adversary": [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]  # Heading for adversary (in radians)
#     },
#     "collisions": [],  # No collisions in this scenario
#     "actors": {  # Actor types mapped to ids
#         "ego": "ego",
#         "adversary": "adversary",
#         "vehicles": [],
#         "pedestrians": []
#     },
#     "otherParams": {  # Custom data
#         "car_width": 3,  # Car width in meters
#         "car_length": 5  # Car length in meters
#     }
# }
file_path = "/home/lev/Documents/testing/opensbt/opensbt-core/extract/data_in/simout_S37.49_29.71_3.86.json"

with open(file_path, 'r') as file:
    data = json.load(file)

simout = SimulationOutput.from_json(json.dumps(data))

input_file = './extract/blank.xosc'  # Replace with your OpenSCENARIO file path
# Create StartPosition and Waypoints for Ego Actor
road_network_path = "./examples/esmini/scenarios/cutin/straight_500m.xodr"
file_path_new = f'./extract/data_out/{os.path.splitext(os.path.basename(file_path).replace("simout", "scenario"))[0]}.xosc'  

for i, actor in enumerate(simout.location.keys()):
    
    location = simout.location[actor]
    yaw = simout.yaw[actor]

    times = simout.times
    
    if i > 0:
        input_file = file_path_new

    append_scenario_object(input_file, actor, file_path_new)

    # Initialize start position for Ego
    start_pos = StartPosition(
        entity_name=actor,
        x=location[0][0],  # First position (x)
        y=location[0][1],  # First position (y)
        z=0.0,  # Assume level ground
        h=0,  # Heading (initial)
        p=0.0,  # Pitch (level)
        r=0.0   # Roll (level)
    )

    # Update OpenSCENARIO paths for Ego scenario
    update_paths(file_path_new,
                controller_catalog_path=None,
                vehicle_catalog_path=None,
                pedestrian_catalog_path=None,
                road_network_path=road_network_path,
                output_file=file_path_new)

    append_start_position(file_path_new, start_pos, file_path_new)

    # Create waypoints for Ego actor from simulation data
    waypoints = [Waypoint(time=times[i], 
                            x=location[i][0], 
                            y=location[i][1], 
                            z=0.0,  # Assuming flat terrain
                            h=yaw[i], 
                            p=0.0, 
                            r=0.0) for i in range(len(times))]

    maneuver_group = ManeuverGroup(entity_name=actor,
                                    maneuver_name=actor + "_trajectory",
                                    waypoints=waypoints)

    append_maneuver_group(file_path_new, maneuver_group, file_path_new)