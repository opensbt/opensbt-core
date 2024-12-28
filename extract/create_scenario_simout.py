import json
import os
from pathlib import Path
from extract.create_so import append_scenario_object
from extract.create_start import StartPosition, append_start_position
from extract.create_wp import ManeuverGroup, Waypoint, append_maneuver_group
from extract.update_env import update_paths
from opensbt.simulation.simulator import SimulationOutput
from extract.set_simtime import update_simulation_time

def extract_xosc(simout: SimulationOutput,
                 road_network_path: str,
                 file_path_new: str,
                 input_file = './extract/blank.xosc',  # use a fresh xosc file
                 time_step = 0.1 # in seconds
                 ):
    # create folder

    Path(os.path.dirname(os.path.normpath(file_path_new))).mkdir(exist_ok=True,
                                                                 parents=True)
    for i, actor in enumerate(simout.location.keys()):
        
        location = simout.location[actor]
        yaw = simout.yaw[actor]

        times = simout.times
        
        if i > 0:
            input_file = file_path_new

        append_scenario_object(input_file, 
                            so_name = actor,
                            asset_name = actor,
                            entry_name = "car_red" if "ego" in actor else "car_white",
                            file_path_new = file_path_new)

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
                                r=0.0)]
        last_time = times[0]

        for i, time in enumerate(times):
            if time - last_time < time_step:
                # skip
                pass
            else:          
                waypoints.append(Waypoint(time=time, 
                                    x=location[i][0], 
                                    y=location[i][1], 
                                    z=0.0,  # Assuming flat terrain
                                    h=yaw[i], 
                                    p=0.0, 
                                    r=0.0))
                last_time = time


        maneuver_group = ManeuverGroup(entity_name=actor,
                                        maneuver_name=actor + "_trajectory",
                                        waypoints=waypoints)

        append_maneuver_group(file_path_new, maneuver_group, file_path_new)

    update_simulation_time(file_path_new, new_value=times[i-1] - times[0])

if __name__ == "__main__":
    file_path = "/home/lev/Documents/testing/opensbt/opensbt-core/extract/data_in/simout_S37.49_29.71_3.86.json"
    sim_time = 10

    with open(file_path, 'r') as file:
        data = json.load(file)

    simout = SimulationOutput.from_json(json.dumps(data))

    # Create StartPosition and Waypoints for Ego Actor
    road_network_path = "./examples/esmini/scenarios/cutin/straight_500m.xodr"
    file_path_new = f'./extract/data_out/{os.path.splitext(os.path.basename(file_path).replace("simout", "scenario"))[0]}.xosc'  

    extract_xosc(simout, 
                 road_network_path,
                file_path_new,
                sim_time
                )