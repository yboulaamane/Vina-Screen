
# VinaScreen

`VinaScreen.py` is a Python script designed to automate the docking of multiple ligands using AutoDock Vina. It processes ligand files in a specified directory, runs docking simulations, extracts the best binding affinity scores, and writes the results to a CSV file. This script also saves debug logs and console outputs for reference.

## Features

- **Automated Docking**: Dock multiple ligands against a single receptor.
- **Customizable Grid Box**: Prompts the user to input grid box coordinates and sizes, making it adaptable to various proteins.
- **Result Extraction**: Automatically extracts the best binding affinity and saves it in a CSV file.
- **Logging**: Generates a debug log and a console output file for tracking docking progress and potential errors.

## Prerequisites

Before running `VinaScreen.py`, ensure you have:

- [Smina](https://github.com/mwojcikowski/smina) or AutoDock Vina installed and in your system path.
- Python 3.x.
- Necessary Python libraries: `argparse`, `os`, `subprocess`, `csv`, and `re`.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/YOUR_USERNAME/VinaScreen.git
   cd VinaScreen
   ```

2. Ensure `Smina` or `AutoDock Vina` is installed and accessible in your system path.

3. Make the script executable:

   ```bash
   chmod +x VinaScreen.py
   ```

## Setting Up the Docking Folder

To start, create a `docking` folder structured as follows:

- Place a receptor file named `receptor.pdbqt` in the root of the `docking` folder.
- Create a `ligands/` subfolder containing all ligand files in `.pdbqt` format.

Your directory structure should look like this:

```
docking/
├── receptor.pdbqt
└── ligands/
    ├── ligand1.pdbqt
    ├── ligand2.pdbqt
    └── ...
```

## Usage

Run `VinaScreen.py` and follow the prompts for grid box settings:

```bash
python VinaScreen.py
```

When prompted, enter the grid box center coordinates and sizes for AutoDock Vina:

- **center_x, center_y, center_z**: Coordinates of the grid box center.
- **size_x, size_y, size_z**: Dimensions of the grid box in Ångstroms.

The script will process each ligand in the `ligands/` folder and output results to:

- `docking_scores.csv`: A CSV file with ligand names and binding affinities.
- `docked_ligands/`: A directory containing the docked ligand files.
- `debug_log.txt`: A log file capturing debug messages.
- `docking_console_output.txt`: A text file with console outputs for each docking.

## Output

The `docking_scores.csv` file will have columns:

- **Ligand**: Name of the ligand.
- **Best Affinity**: The best binding affinity (in kcal/mol) obtained for each ligand.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
