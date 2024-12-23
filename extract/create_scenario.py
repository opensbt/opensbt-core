# Example usage
from extract.create_so import append_scenario_object
from extract.create_start import StartPosition, append_start_position
from extract.create_wp import ManeuverGroup, Waypoint, append_maneuver_group
from extract.update_env import update_paths

input_file = './extract/blank.xosc'  # Replace with your OpenSCENARIO file path
user_name = "new_car"           # Replace with the desired name for the new ScenarioObject
file_path_new = './extract/alks_cut-in_out.xosc'  
road_network_path = "./examples/esmini/scenarios/cutin/straight_500m.xodr"


update_paths(input_file,
             controller_catalog_path=None,
             vehicle_catalog_path=None,
             pedestrian_catalog_path=None,
             road_network_path = road_network_path, 
             output_file= file_path_new)

append_scenario_object(file_path_new, user_name, file_path_new)

n = 50
v = 10

times = [0.1 * i for i in range(1,n)]
x_positions = [0.3 + i for i in range(n)]
y_positions = [0.4] * n
z_positions = [0] * n
h_values = [0] * n
p_values = [0] * n
r_values = [0] * n

start_pos = StartPosition(
    entity_name=user_name,  
    x=0.305662431294499,
    y=0.405895133832167,
    z=0.0,
    h=0,
    p=0.0,
    r=0.0
)

append_start_position(file_path_new, start_pos, file_path_new)

# Creating waypoints from the arrays
waypoints = [Waypoint(time=times[i], 
                      x=x_positions[i], 
                      y=y_positions[i], 
                      z=z_positions[i], 
                      h=h_values[i], 
                      p=p_values[i], 
                      r=r_values[i]) for i in range(len(times))]

maneuver_group = ManeuverGroup(entity_name=user_name,
                               maneuver_name=user_name + "trajectory",
                                waypoints=waypoints)

append_maneuver_group(file_path_new, maneuver_group, file_path_new)
