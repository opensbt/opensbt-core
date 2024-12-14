# Example usage
from create_so import append_scenario_object
from create_start import StartPosition, append_start_position
from create_wp import ManeuverGroup, Waypoint, append_maneuver_group

input_file = './extract/blank.xosc'  # Replace with your OpenSCENARIO file path
user_name = "new_car"           # Replace with the desired name for the new ScenarioObject
file_path_new = './extract/alks_cut-in_out.xosc'  

append_scenario_object(input_file, user_name, file_path_new)

start_pos = StartPosition(
    entity_name=object,  # Replace with your entity name
    x=9.305662431294499,
    y=-5.405895133832167,
    z=0.0,
    h=2.885502313499262,
    p=0.0,
    r=0.0
)

append_start_position(file_path_new, start_pos, file_path_new)

times = [0.0, 0.1, 0.2, 0.3]
x_positions = [0.07048201901451069, -2.8929019513336, -5.792451795950327, -8.779218500581448]
y_positions = [0.16139164857664753, 0.9401358450007034, 1.7025625489442064, 2.487654651322864]
z_positions = [0.0, 0.0, 0.0, 0.0]
h_values = [2.8847042157881377, 2.8846547598336847, 2.884580269842682, 2.884501583777352]
p_values = [0.0, 0.0, 0.0, 0.0]
r_values = [0.0, 0.0, 0.0, 0.0]

# Creating waypoints from the arrays
waypoints = [Waypoint(time=times[i], x=x_positions[i], y=y_positions[i], z=z_positions[i], h=h_values[i], p=p_values[i], r=r_values[i]) for i in range(len(times))]

maneuver_group = ManeuverGroup(entity_name=object, waypoints=waypoints)

append_maneuver_group(file_path_new, maneuver_group, file_path_new)
