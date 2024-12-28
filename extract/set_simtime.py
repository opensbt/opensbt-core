import xml.etree.ElementTree as ET

def update_simulation_time(xml_path, new_value):
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Find the first StopTrigger under Storyboard
    stop_trigger = root.find(".//Storyboard/StopTrigger")
    
    if stop_trigger is not None:
        # Find the first SimulationTimeCondition under this StopTrigger
        sim_time = stop_trigger.find(".//SimulationTimeCondition")
        
        if sim_time is not None:
            sim_time.set("value", str(new_value))
            print(f"Updated SimulationTimeCondition to {new_value}.")
        else:
            print("SimulationTimeCondition not found under StopTrigger.")
    else:
        print("StopTrigger not found under Storyboard.")
    
    # Write the updated XML back to file
    tree.write(xml_path)
