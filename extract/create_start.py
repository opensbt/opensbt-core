import xml.etree.ElementTree as ET
from xml.dom import minidom

class StartPosition:
    def __init__(self, entity_name, x, y, z=0.0, h=0.0, p=0.0, r=0.0):
        self.entity_name = entity_name
        self.x = x
        self.y = y
        self.z = z
        self.h = h
        self.p = p
        self.r = r

    def to_xml(self):
        """Generate an XML element for the start position."""
        private = ET.Element("Private", entityRef=self.entity_name)

        private_action = ET.SubElement(private, "PrivateAction")
        teleport_action = ET.SubElement(private_action, "TeleportAction")
        position = ET.SubElement(teleport_action, "Position")
        world_position = ET.SubElement(position, "WorldPosition", {
            "x": str(self.x),
            "y": str(self.y),
            "z": str(self.z),
            "h": str(self.h),
            "p": str(self.p),
            "r": str(self.r)
        })

        return private

def prettify_xml(element):
    """Return a pretty-printed XML string for the given Element, without extra blank lines."""
    rough_string = ET.tostring(element, encoding="utf-8")
    parsed = minidom.parseString(rough_string)
    pretty_xml = parsed.toprettyxml(indent="    ")

    # Remove extra blank lines
    pretty_xml = "\n".join([line for line in pretty_xml.splitlines() if line.strip()])

    return pretty_xml

def append_start_position(file_path, start_position, file_path_new):
    """Append a start position to the <Actions> section of an OpenSCENARIO file."""
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Find the Actions element
    actions = root.find(".//Actions")
    if actions is None:
        actions = ET.SubElement(root, "Actions")

    # Create a new start position
    new_position = start_position.to_xml()

    # Append the new position
    actions.append(new_position)

    # Prettify and save the updated XML
    with open(file_path_new, "w", encoding="utf-8") as f:
        f.write(prettify_xml(root))

    print(f"Appended start position for entity '{start_position.entity_name}' to {file_path_new}")

if __name__ == "main":
    # Example usage
    # Example usage
    input_file = './extract/alks_cut-in_out.xosc'  # Replace with your OpenSCENARIO file path
    object = "new_car"
    file_path_new = './extract/alks_cut-in_out_start.xosc'  

    start_pos = StartPosition(
        entity_name=object,  # Replace with your entity name
        x=9.305662431294499,
        y=-5.405895133832167,
        z=0.0,
        h=2.885502313499262,
        p=0.0,
        r=0.0
    )

    append_start_position(input_file, start_pos, file_path_new)

