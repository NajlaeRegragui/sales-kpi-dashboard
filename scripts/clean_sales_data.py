from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    generator = ROOT / "scripts" / "generate_sales_data.py"
    result = subprocess.run([sys.executable, str(generator)], cwd=ROOT)
    if result.returncode != 0:
        return result.returncode

    shutil.copyfile(ROOT / "data" / "raw" / "FactSales.csv", ROOT / "data" / "raw" / "sales_data_raw.csv")
    shutil.copyfile(
        ROOT / "data" / "cleaned" / "FactSales.csv",
        ROOT / "data" / "cleaned" / "sales_data_cleaned.csv",
    )
    print("Created data/raw/sales_data_raw.csv")
    print("Created data/cleaned/sales_data_cleaned.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
