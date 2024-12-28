from xml.dom import minidom
import xml.etree.ElementTree as ET

class ScenarioObject:
    def __init__(self, so_name: str, asset_name: str,  asset_type: str, 
                 width=1.8, height=1.2, length=3.0, category="car", 
                 catalog_name = None, entry_name = None,
                 **kwargs):
        self.so_name = so_name
        self.so_name = asset_name
        self.asset_type = asset_type
        self.width = width
        self.height = height
        self.length = length
        self.category = category
        self.additional_attributes = kwargs  # Store remaining attributes (optional: performance, axles, etc.)

        self.catalog_name = catalog_name
        self.entry_name = entry_name

    def to_xml(self):
        """Generate an XML element for the ScenarioObject."""
        scenario_obj = ET.Element("ScenarioObject", name=self.so_name)
        if self.catalog_name is not None and self.entry_name is not None:
            ET.SubElement(scenario_obj, "CatalogReference", catalogName=self.catalog_name, entryName=self.entry_name)
        
        if self.asset_type.lower() == "vehicle":
            # Vehicle element
            asset = ET.SubElement(scenario_obj, "Vehicle", name=self.so_name, vehicleCategory=self.category)
        elif self.asset_type.lower() == "pedestrian":
            asset = ET.SubElement(scenario_obj, "Pedestrian", name=self.so_name, pedestrianCategory=self.category)
        else:
            return ValueError("Unkown type.")
        
        ET.SubElement(asset, "ParameterDeclarations")

        # BoundingBox
        bounding_box = ET.SubElement(asset, "BoundingBox")
        center = ET.SubElement(bounding_box, "Center")
        center.set("x", "0.0")
        center.set("y", "0.0")
        center.set("z", "0.6016365736334145")  # Default z value
        dimensions = ET.SubElement(bounding_box, "Dimensions")
        dimensions.set("width", str(self.width))
        dimensions.set("height", str(self.height))
        dimensions.set("length", str(self.length))

        # Performance
        performance = self.additional_attributes.get("performance", {"maxSpeed": "67.0", "maxDeceleration": "9.5", "maxAcceleration": "10.0"})
        perf_element = ET.SubElement(asset, "Performance")
        for attr, value in performance.items():
            perf_element.set(attr, str(value))

        if self.asset_type.lower() == "vehicle":
            # Axles
            axles = self.additional_attributes.get("axles", {
                "FrontAxle": {"maxSteering": "0.48", "wheelDiameter": "0.684", "trackWidth": "1.672", "positionX": "0.0", "positionZ": "0.0"},
                "RearAxle": {"maxSteering": "0.0", "wheelDiameter": "0.684", "trackWidth": "1.672", "positionX": "0.0", "positionZ": "0.0"},
            })
            axles_element = ET.SubElement(asset, "Axles")
            for axle_name, axle_attributes in axles.items():
                axle_element = ET.SubElement(axles_element, axle_name)
                for attr, value in axle_attributes.items():
                    axle_element.set(attr, str(value))

        # Properties
        properties = self.additional_attributes.get("properties", {"control": "external"})
        props_element = ET.SubElement(asset, "Properties")
        for prop_name, prop_value in properties.items():
            ET.SubElement(props_element, "Property", name=prop_name, value=prop_value)

        # ObjectController
        controller_name = self.additional_attributes.get("controller_name", "DefaultDriver")
        obj_controller = ET.SubElement(scenario_obj, "ObjectController")
        controller = ET.SubElement(obj_controller, "Controller", name=controller_name)
        ET.SubElement(controller, "ParameterDeclarations")
        ET.SubElement(controller, "Properties")

        return scenario_obj
    
def prettify_xml(element):
    """Return a pretty-printed XML string for the given Element, without extra blank lines."""
    rough_string = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    pretty_xml = parsed.toprettyxml(indent="    ")

    # Remove extra blank lines
    pretty_xml = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])

    return pretty_xml

def append_scenario_object(file_path, 
                        so_name,
                        asset_name,
                        file_path_new,
                        asset_type="vehicle",
                        category="car",
                        catalog_name="VehicleCatalog",
                        entry_name="car_green"):
    """Append a new ScenarioObject to an existing OpenSCENARIO file."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the Entities element
    entities = root.find(".//Entities")
    if entities is None:
        entities = ET.SubElement(root, "Entities")

    # Create a new ScenarioObject
    new_object = ScenarioObject(so_name = so_name,
                                asset_name = asset_name,
                                asset_type = asset_type,
                                category=category,
                                catalog_name=catalog_name,
                                entry_name=entry_name).to_xml()

    # Append the new object
    entities.append(new_object)

    # Prettify and save the updated XML
    with open(file_path_new, "w", encoding="utf-8") as f:
        f.write(prettify_xml(root))

if __name__ == "__main__":
    # Example usage
    input_file = './extract/alks_cut-in.xosc'  # Replace with your OpenSCENARIO file path
    so_name = "new_car"           # Replace with the desired name for the new ScenarioObject
    file_path_new = './extract/alks_cut-in_out.xosc'  
    append_scenario_object(input_file, 
                           so_name,
                           so_name, 
                           file_path_new)