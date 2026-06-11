import os
import subprocess

# Define the array of target directories
directories = [
    "l_0p15_w_1p6",
    "l_0p25_w_1p6",
    "l_1p0_w_1p6",
    "l_20p0_w_0p64",
    "l_0p19_w_7p0",
    "l_100p0_w_100p0",
    "l_1p0_w_3p0",
    "l_8p0_w_1p6"
]

# Get the script's current directory as the absolute base
base_dir = os.getcwd()

for folder in directories:
    folder_path = os.path.join(base_dir, folder)
    
    # Check if the directory actually exists
    if os.path.isdir(folder_path):
        os.chdir(folder_path)
        
        # Files to run sequentially
        spice_files = ["vd_varVg.spice", "vg_varVd.spice"]
        
        for spice_file in spice_files:
            if os.path.isfile(spice_file):
               
                
                # Generate corresponding log name (e.g., vd_varVg.log)
                log_file_name = spice_file.replace(".spice", ".log")
                
                # Run ngspice in batch mode (-b) and pipe stdout/stderr directly to the log file
                with open(log_file_name, "w") as log_file:
                    subprocess.run(
                        ["ngspice", "-b", spice_file], 
                        stdout=log_file, 
                        stderr=subprocess.STDOUT
                    )
            else:
                print(f" Warning: {spice_file} not found!")
                
        # Move back to base directory before checking the next folder
        os.chdir(base_dir)
    else:
        print(f"Error: Directory {folder} does not exist. Skipping.")

print("DONEEEE")