import subprocess
import os
import argparse

def run_scenario(esmini_path, scenario):
    # Check if paths exist
    if not os.path.isfile(esmini_path):
        print(f"Error: esmini executable not found at {esmini_path}")
        return
    
    if not os.path.isfile(scenario):
        print(f"Error: Scenario file not found at {scenario}")
        return

    # Define the command
    command = [
        esmini_path,
        "--window", "60", "60", "800", "400",
        "--osc", scenario
    ]

    try:
        # Run the command
        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Print the output and error (if any)
        print("Output:")
        print(result.stdout)
        if result.stderr:
            print("Error (non-fatal):")
            print(result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Execution failed (code {e.returncode}): {e.stderr}")
    except FileNotFoundError:
        print("The specified executable or file paths do not exist.")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run esmini with OpenSCENARIO file.")
    parser.add_argument("--scenario", help="Path to the OpenSCENARIO (.xosc) file",
                        default="./examples/esmini/scenarios/cutin/alks_cut-in.xosc")
    
    args = parser.parse_args()

    esmini_path = "./examples/esmini/esmini-demo_linux/esmini/bin/esmini"
    run_scenario(esmini_path, args.scenario)