#!/usr/bin/env python3
"""
Author: Yassir Boulaamane, PhD
Affiliation: Laboratory of Innovative Technologies, National School of Applied Sciences of Tangier, Abdelmalek Essaadi University, Tetouan, Morocco
Description:
    This script automates the docking of multiple ligands using AutoDock Vina.
    It processes ligand files in the specified directory, runs docking simulations,
    extracts the best binding affinity scores, and writes the results to a CSV file.
    Debug logs and console outputs are also saved for reference.

    The script prompts the user to input grid box coordinates and sizes,
    making it adaptable to different proteins without manual script changes.

Thank you for using this script.
"""

# ASCII art displayed separately as a raw string
ascii_art = r"""
____   ____ __                  _________                                   
\   \ /   /|__| ____ _____     /   _____/ ___________   ____   ____   ____  
 \   Y   / |  |/    \\__  \    \_____  \_/ ___\_  __ \_/ __ \_/ __ \ /    \ 
  \     /  |  |   |  \/ __ \_  /        \  \___|  | \/\  ___/\  ___/|   |  \
   \___/   |__|___|  (____  / /_______  /\___  >__|    \___  >\___  >___|  /
                   \/     \/          \/     \/            \/     \/     \/ 
"""

# Print ASCII art
print(ascii_art)

import os
import subprocess
import csv
import re
import sys

# Define constants
RECEPTOR = "receptor.pdbqt"
DOCKING_DIR = "./ligands"  # Input ligands directory
OUTPUT_DIR = "./docked_ligands"  # Output docked ligands directory
CONSOLE_OUTPUT = "docking_console_output.txt"
OUTPUT_CSV = "docking_scores.csv"
DEBUG_LOG = "debug_log.txt"

# Function to write debug information
def write_debug(message):
    with open(DEBUG_LOG, 'a') as debug_file:
        debug_file.write(message + "\n")
    print(message)

# Print script information to console
print("Author: Yassir Boulaamane, PhD")
print("Affiliation: Laboratory of Innovative Technologies, National School of Applied Sciences of Tangier, Abdelmalek Essaadi University, Tetouan, Morocco")
print("Description:")
print("    This script automates the docking of multiple ligands using AutoDock Vina.")
print("    It processes ligand files in the specified directory, runs docking simulations,")
print("    extracts the best binding affinity scores, and writes the results to a CSV file.")
print("    The script prompts the user to input grid box coordinates and sizes,")
print("    making it adaptable to different proteins without manual script changes.\n")
print("Thank you for using this script.\n")


# Create output directory if it doesn't exist
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
    write_debug(f"Created output directory: {OUTPUT_DIR}")

# Clear previous console output
with open(CONSOLE_OUTPUT, 'w') as console_file:
    pass  # Using 'pass' to create an empty file


# Function to get grid box coordinates and sizes from the user
def get_grid_coordinate(prompt):
    while True:
        user_input = input(f"{prompt}: ")
        if user_input.strip() == '':
            return "0.0"  # Default value used silently without displaying it in the prompt
        else:
            try:
                return str(float(user_input))
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

# Prompt user for grid box coordinates and sizes
print("Please enter the grid box coordinates and sizes for AutoDock Vina.")

center_x = get_grid_coordinate("Enter center_x")
center_y = get_grid_coordinate("Enter center_y")
center_z = get_grid_coordinate("Enter center_z")
size_x = get_grid_coordinate("Enter size_x")
size_y = get_grid_coordinate("Enter size_y")
size_z = get_grid_coordinate("Enter size_z")

write_debug(f"Grid box settings: center_x={center_x}, center_y={center_y}, center_z={center_z}, size_x={size_x}, size_y={size_y}, size_z={size_z}")

# Prepare to write to the CSV
try:
    with open(OUTPUT_CSV, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Ligand", "Best Affinity"])
        csvfile.flush()  
        os.fsync(csvfile.fileno())  
        write_debug("CSV file opened and header written")

        # Check if the docking directory exists
        if not os.path.isdir(DOCKING_DIR):
            write_debug("Error: Docking directory does not exist: " + DOCKING_DIR)
            sys.exit(1)

        ligand_count = 0
        for ligand in os.listdir(DOCKING_DIR):
            if ligand.endswith(".pdbqt") and '_docked' not in ligand:
                ligand_count += 1
                ligand_path = os.path.join(DOCKING_DIR, ligand)
                ligand_name = os.path.splitext(ligand)[0]
                docked_file = os.path.join(OUTPUT_DIR, f"{ligand_name}_docked.pdbqt")

                write_debug("Processing ligand: " + ligand_name)

                command = [
                    "vina",
                    "--receptor", RECEPTOR,
                    "--ligand", ligand_path,
                    "--out", docked_file,
                    "--center_x", center_x,
                    "--center_y", center_y,
                    "--center_z", center_z,
                    "--size_x", size_x,
                    "--size_y", size_y,
                    "--size_z", size_z,
                    "--exhaustiveness", "8"
                ]

                try:
                    vina_output = subprocess.check_output(command, stderr=subprocess.STDOUT).decode('utf-8')
                    write_debug("Vina command executed successfully for " + ligand_name)

                    with open(CONSOLE_OUTPUT, 'a') as console_file:
                        console_file.write(f"Docking results for {ligand_name}:\n")
                        console_file.write(vina_output)
                        console_file.write("\n\n")

                    match = re.search(r'^\s*1\s+([-\d.]+)', vina_output, re.MULTILINE)
                    if match:
                        best_score = float(match.group(1))
                        csv_writer.writerow([ligand_name, best_score])
                        csvfile.flush()  
                        os.fsync(csvfile.fileno())  
                        write_debug(f"Written to CSV: {ligand_name}, {best_score}")
                    else:
                        write_debug("Could not find best affinity score for " + ligand_name)
                        csv_writer.writerow([ligand_name, "N/A"])
                        csvfile.flush()  
                        os.fsync(csvfile.fileno())  

                except subprocess.CalledProcessError as e:
                    write_debug(f"Error occurred while docking {ligand_name}: {e}")
                    with open(CONSOLE_OUTPUT, 'a') as console_file:
                        console_file.write(f"Error docking {ligand_name}: {e}\n\n")
                    csv_writer.writerow([ligand_name, "Error"])
                    csvfile.flush()  
                    os.fsync(csvfile.fileno())  

        write_debug(f"Processed {ligand_count} ligands")

except IOError as e:
    write_debug("Error opening or writing to CSV file: " + str(e))
except Exception as e:
    write_debug("Unexpected error: " + str(e))

write_debug(f"Script completed. Check {OUTPUT_CSV} for results.")
