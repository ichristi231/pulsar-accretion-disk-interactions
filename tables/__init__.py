from pathlib import Path
import numpy as np

tables_dir = Path.cwd() / "tables"
sgr_a_observations = np.loadtxt(
    tables_dir / "sgr_a_observations.txt")
