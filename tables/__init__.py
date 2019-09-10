from pathlib import Path
import numpy as np

tables_dir = Path.cwd() / "tables"
sgr_a_observations_radio_frequency = np.loadtxt(
    tables_dir / "sgr_a_observations_radio_frequency.txt")
sgr_a_observations_radio_luminosity = np.loadtxt(
    tables_dir / "sgr_a_observations_radio_luminosity.txt")

sgr_a_observations_xray_frequency = np.loadtxt(
    tables_dir / "sgr_a_observations_xray_frequency.txt")
sgr_a_observations_xray_luminosity = np.loadtxt(
    tables_dir / "sgr_a_observations_xray_luminosity.txt")

sgr_a_observations_IR_frequency = np.loadtxt(
    tables_dir / "sgr_a_observations_IR_frequency.txt")
sgr_a_observations_IR_luminosity = np.loadtxt(
    tables_dir / "sgr_a_observations_IR_luminosity.txt")
