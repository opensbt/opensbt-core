import subprocess
scenario = "./extract/alks_cut-in_out_start_wp.xosc" 
scenario = "./extract/blank.xosc" 

esmini_path = "/home/lev/Documents/testing/opensbt/opensbt-core/examples/esmini/esmini-demo_linux/esmini/bin/esmini"
# Define the command as a list
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
    print("Error:")
    print(result.stderr)
except subprocess.CalledProcessError as e:
    print(f"Command failed with return code {e.returncode}")
    print(f"Error: {e.stderr}")
except FileNotFoundError:
    print("The specified executable or file paths do not exist.")

