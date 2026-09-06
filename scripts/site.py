"""Bootstrap includes before Quarto scans a fresh checkout."""
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / 'scripts/optimize-images.py')], cwd=root, check=True)
subprocess.run([sys.executable, str(root / 'scripts/build-content.py')], cwd=root, check=True)
raise SystemExit(subprocess.call(['quarto', *(sys.argv[1:] or ['render'])], cwd=root))
