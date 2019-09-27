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

antf_spin_down_luminosities = np.loadtxt(
    tables_dir / "ANTF_spin_down_luminosity_pulsar_catalog.txt")

synchrotron_log10_x = np.loadtxt(
    tables_dir / "single_part_emissivity_x_store.txt")
synchrotron_log10_f_x = np.loadtxt(
    tables_dir / "single_part_emissivity_f_store.txt")
