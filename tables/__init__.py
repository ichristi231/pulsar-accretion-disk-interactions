from pathlib import Path
import numpy as np

tables_dir = Path.cwd() / "tables"
sgr_a_observations_frequency = np.loadtxt(
    tables_dir / "sgr_a_observations_frequency.txt")
sgr_a_observations_luminosity = np.loadtxt(
    tables_dir / "sgr_a_observations_luminosity.txt")
