import xml.etree.ElementTree as ET
from xml.dom import minidom

class Waypoint:
    def __init__(self, time, x, y, z=0.0, h=0.0, p=0.0, r=0.0):
        self.time = time
        self.x = x
        self.y = y
        self.z = z
        self.h = h
        self.p = p
        self.r = r

    def to_xml(self):
        """Generate an XML element for a waypoint (vertex)."""
        vertex = ET.Element("Vertex", time=str(self.time))
        position = ET.SubElement(vertex, "Position")
        ET.SubElement(position, "WorldPosition", {
            "x": str(self.x),
            "y": str(self.y),
            "z": str(self.z),
            "h": str(self.h),
            "p": str(self.p),
            "r": str(self.r)
        })
        return vertex

class ManeuverGroup:
    def __init__(self, entity_name, waypoints, maneuver_name="ego trajectory", act_name="Main act"):
        self.entity_name = entity_name
        self.waypoints = waypoints
        self.maneuver_name = maneuver_name
        self.act_name = act_name

    def to_xml(self):
        """Generate an XML structure for a maneuver group with waypoints."""
        # Act element
        act = ET.Element("Act", name=self.act_name)

        # ManeuverGroup element
        maneuver_group = ET.SubElement(act, "ManeuverGroup", name="ego", maximumExecutionCount="1")

        # Actors element
        actors = ET.SubElement(maneuver_group, "Actors", selectTriggeringEntities="false")
        ET.SubElement(actors, "EntityRef", entityRef=self.entity_name)

        # Maneuver element
        maneuver = ET.SubElement(maneuver_group, "Maneuver", name=self.maneuver_name)
        
        # Event element
        event = ET.SubElement(maneuver, "Event", name="event", priority="overwrite", maximumExecutionCount="1")
        
        # Action element
        action = ET.SubElement(event, "Action", name=self.maneuver_name)

        # PrivateAction -> RoutingAction -> FollowTrajectoryAction -> TrajectoryRef
        private_action = ET.SubElement(action, "PrivateAction")
        routing_action = ET.SubElement(private_action, "RoutingAction")
        follow_trajectory_action = ET.SubElement(routing_action, "FollowTrajectoryAction")
        trajectory_ref = ET.SubElement(follow_trajectory_action, "TrajectoryRef")
        trajectory = ET.SubElement(trajectory_ref, "Trajectory", name=self.maneuver_name, closed="false")

        # ParameterDeclarations element
        ET.SubElement(trajectory, "ParameterDeclarations")

        # Shape -> Polyline -> Vertex elements (waypoints)
        shape = ET.SubElement(trajectory, "Shape")
        polyline = ET.SubElement(shape, "Polyline")

        # Add waypoints (vertices)
        for waypoint in self.waypoints:
            polyline.append(waypoint.to_xml())

        # TimeReference -> Timing
        time_reference = ET.SubElement(follow_trajectory_action, "TimeReference")
        ET.SubElement(time_reference, "Timing", domainAbsoluteRelative="relative", scale="1.0", offset="0.0")
        ET.SubElement(follow_trajectory_action, "TrajectoryFollowingMode", followingMode="position")

        # StartTrigger
        start_trigger = ET.SubElement(event, "StartTrigger")
        condition_group = ET.SubElement(start_trigger, "ConditionGroup")
        condition = ET.SubElement(condition_group, "Condition", name="Start Condition of Event", delay="0.0", conditionEdge="rising")
        by_value_condition = ET.SubElement(condition, "ByValueCondition")
        ET.SubElement(by_value_condition, "SimulationTimeCondition", value="1.0", rule="greaterThan")

        return act

def prettify_xml(element):
    """Return a pretty-printed XML string for the given Element, without extra blank lines."""
    rough_string = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    pretty_xml = parsed.toprettyxml(indent="    ")

    # Remove extra blank lines
    pretty_xml = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])

    return pretty_xml

def append_maneuver_group(file_path, maneuver_group, file_path_new):
    """Append a maneuver group with waypoints to the <Actions> section of an OpenSCENARIO file."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the Actions element
    actions = root.find(".//Actions")
    if actions is None:
        actions = ET.SubElement(root, "Actions")

    # Create a new maneuver group
    new_maneuver_group = maneuver_group.to_xml()

    # Append the new maneuver group
    actions.append(new_maneuver_group)

    # Prettify and save the updated XML
    with open(file_path_new, "w", encoding="utf-8") as f:
        f.write(prettify_xml(root))

    print(f"Appended maneuver group for entity '{maneuver_group.entity_name}' to {file_path_new}")

if __name__ == "main":
    # Example usage
    input_file = './extract/alks_cut-in_out_start.xosc'  # Replace with your OpenSCENARIO file path
    object = "new_car"
    file_path_new = './extract/alks_cut-in_out_start_wp.xosc'  

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

    append_maneuver_group(input_file, maneuver_group, file_path_new)
