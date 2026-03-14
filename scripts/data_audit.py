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


def print_divider(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def audit_exports():
    print_divider("EXPORTS AUDIT")
    df = pd.read_csv(exports_path)

    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("Unique country codes:", df["Country Code"].nunique())

    year_cols = [c for c in df.columns if "[YR" in c]
    print("Year columns:", year_cols)

    non_null_counts = df[year_cols].notna().sum()
    print("\nNon-null counts by year:")
    print(non_null_counts)


def audit_port_traffic():
    print_divider("PORT TRAFFIC AUDIT")
    df = pd.read_csv(port_path, skiprows=4)

    print("Shape:", df.shape)
    print("Columns:", list(df.columns[:10]))
    print("Unique country codes:", df["Country Code"].nunique())

    year_cols = [c for c in df.columns if c.isdigit()]
    print("Year columns:", year_cols)

    if year_cols:
        non_null_counts = df[year_cols].notna().sum()
        print("\nNon-null counts by year:")
        print(non_null_counts.tail(10))


def audit_lsc():
    print_divider("LSC AUDIT")
    df = pd.read_csv(lsc_path)

    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("Unique countries:", df["REF_AREA"].nunique())
    print("Frequency values:", df["FREQ"].dropna().unique())
    print("Time range:", df["TIME_PERIOD"].min(), "to", df["TIME_PERIOD"].max())

    if "OBS_VALUE" in df.columns:
        print("Non-null OBS_VALUE:", df["OBS_VALUE"].notna().sum())


def audit_oil():
    print_divider("BRENT OIL AUDIT")
    df = pd.read_csv(oil_path)

    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("Date range:", df["observation_date"].min(), "to", df["observation_date"].max())
    print("Null count:", df["DCOILBRENTEU"].isna().sum())


def audit_copper():
    print_divider("COPPER AUDIT")
    df = pd.read_csv(copper_path)

    print("Shape:", df.shape)
    print("Columns:", list(df.columns))
    print("Date range:", df["observation_date"].min(), "to", df["observation_date"].max())
    print("Null count:", df["PCOPPUSDM"].isna().sum())


def audit_lpi():
    print_divider("LPI AUDIT")
    xls = pd.ExcelFile(lpi_path)

    print("Sheets:", xls.sheet_names)

    for sheet in xls.sheet_names:
        try:
            df = pd.read_excel(lpi_path, sheet_name=sheet)
            print(f"\nSheet: {sheet}")
            print("Shape:", df.shape)
            print("Columns preview:", list(df.columns[:10]))
        except Exception as e:
            print(f"\nSheet: {sheet}")
            print("ERROR:", e)


def main():
    audit_exports()
    audit_port_traffic()
    audit_lsc()
    audit_oil()
    audit_copper()
    audit_lpi()


if __name__ == "__main__":
    main()
