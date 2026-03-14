from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"

exports_path = RAW_DIR / "P_Data_Extract_From_World_Development_Indicators" / "58203ffc-47c5-4b8c-aba3-93983d6f8fc1_Data.csv"
port_path = RAW_DIR / "API_IS" / "API_IS.SHP.GOOD.TU_DS2_en_csv_v2_186.csv"
lsc_path = RAW_DIR / "UNCTAD_LSC.csv"
oil_path = RAW_DIR / "DCOILBRENTEU.csv"
copper_path = RAW_DIR / "PCOPPUSDM.csv"
lpi_path = RAW_DIR / "International_LPI_from_2007_to_2023_0.xlsx"


def try_read_csv(path: Path, skiprows: int = 0):
    return pd.read_csv(path, skiprows=skiprows)

def main():
    print("\n--- FILE LOAD TEST START ---\n")

    for name, path in files_to_test.items():
        print(f"Testing: {name}")
        print(f"Path: {path}")

        if not path.exists():
            print("  -> FILE NOT FOUND\n")
            continue

        try:
            if path.suffix.lower() == ".xlsx":
                xls = pd.ExcelFile(path)
                print(f"  -> SUCCESS: Excel loaded")
                print(f"  -> Sheets: {xls.sheet_names}\n")
            else:
                # World Bank API-style files often need skiprows=4
                if "API_IS.SHP.GOOD.TU" in path.name:
                    df = try_read_csv(path, skiprows=4)
                else:
                    df = try_read_csv(path)

                print(f"  -> SUCCESS: CSV loaded")
                print(f"  -> Shape: {df.shape}")
                print(f"  -> Columns: {list(df.columns[:8])}\n")

        except Exception as e:
            print(f"  -> ERROR: {e}\n")

    print("--- FILE LOAD TEST END ---\n")

if __name__ == "__main__":
    main()
