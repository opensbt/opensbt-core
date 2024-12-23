import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(element):
    """Return a pretty-printed XML string for the given Element, without extra blank lines."""
    rough_string = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    pretty_xml = parsed.toprettyxml(indent="    ")

    # Remove extra blank lines
    pretty_xml = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])

    return pretty_xml

def update_paths(xml_file, 
                 vehicle_catalog_path, 
                 pedestrian_catalog_path, 
                 controller_catalog_path, 
                 road_network_path, 
                 output_file):
    try:
        # Parse the XML file
        tree = ET.parse(xml_file)
        root = tree.getroot()
        if vehicle_catalog_path is not None:
            # Update vehicle catalog path
            vehicle_catalog = root.find(".//VehicleCatalog/Directory")
            if vehicle_catalog is not None:
                vehicle_catalog.set("path", vehicle_catalog_path)
                print("Vehicle Catalog Updated.")

        if pedestrian_catalog_path is not None:
            # Update pedestrian catalog path
            pedestrian_catalog = root.find(".//PedestrianCatalog/Directory")
            if pedestrian_catalog is not None:
                pedestrian_catalog.set("path", pedestrian_catalog_path)
                print("Pedestrian Catalog Updated.")

        if controller_catalog_path is not None:
            # Update controller catalog path
            controller_catalog = root.find(".//ControllerCatalog/Directory")
            if controller_catalog is not None:
                controller_catalog.set("path", controller_catalog_path)
                print("Controller Catalog Updated.")

        if road_network_path is not None:
            # Update road file path
            road_file = root.find(".//RoadNetwork/LogicFile")
            if road_file is not None:
                road_file.set("filepath", road_network_path)
                print("RoadNetwork Updated.")
            else:
                print("Warning: No <LogicFile> found in <RoadNetwork>.")

        # Prettify and save the updated XML
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prettify_xml(root))

        print(f"Updated XML saved to {output_file}")

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")