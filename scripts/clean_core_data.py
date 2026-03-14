from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

exports_path = RAW_DIR / "P_Data_Extract_From_World_Development_Indicators" / "58203ffc-47c5-4b8c-aba3-93983d6f8fc1_Data.csv"
port_path = RAW_DIR / "API_IS" / "API_IS.SHP.GOOD.TU_DS2_en_csv_v2_186.csv"
lsc_path = RAW_DIR / "UNCTAD_LSC.csv"


def clean_exports() -> pd.DataFrame:
    df = pd.read_csv(exports_path)

    year_cols = [c for c in df.columns if "[YR" in c]

    df_long = df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_cols,
        var_name="year_raw",
        value_name="exports_usd"
    )

    df_long["year"] = df_long["year_raw"].str.extract(r"(\d{4})").astype(int)
    df_long["exports_usd"] = pd.to_numeric(df_long["exports_usd"], errors="coerce")

    df_long = df_long.rename(columns={
        "Country Name": "country_name",
        "Country Code": "country_code"
    })

    df_long = df_long[
        (df_long["year"] >= 2016) &
        (df_long["year"] <= 2019)
    ][["country_name", "country_code", "year", "exports_usd"]]

    return df_long


def clean_port_traffic() -> pd.DataFrame:
    df = pd.read_csv(port_path, skiprows=4)

    year_cols = [c for c in df.columns if c.isdigit()]

    df_long = df.melt(
        id_vars=["Country Name", "Country Code"],
        value_vars=year_cols,
        var_name="year",
        value_name="port_teu"
    )

    df_long["year"] = df_long["year"].astype(int)
    df_long["port_teu"] = pd.to_numeric(df_long["port_teu"], errors="coerce")

    df_long = df_long.rename(columns={
        "Country Name": "country_name",
        "Country Code": "country_code"
    })

    df_long = df_long[
        (df_long["year"] >= 2016) &
        (df_long["year"] <= 2019)
    ][["country_name", "country_code", "year", "port_teu"]]

    return df_long


def clean_lsc() -> pd.DataFrame:
    df = pd.read_csv(lsc_path)

    df = df[["REF_AREA", "REF_AREA_LABEL", "TIME_PERIOD", "OBS_VALUE"]].copy()

    df["year"] = df["TIME_PERIOD"].str.extract(r"(\d{4})").astype(int)
    df["OBS_VALUE"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")

    df = df[
        (df["year"] >= 2016) &
        (df["year"] <= 2019)
    ]

    df_yearly = (
        df.groupby(["REF_AREA", "REF_AREA_LABEL", "year"], as_index=False)["OBS_VALUE"]
        .mean()
    )

    df_yearly = df_yearly.rename(columns={
        "REF_AREA": "country_code",
        "REF_AREA_LABEL": "country_name",
        "OBS_VALUE": "lsc_index"
    })

    return df_yearly


def main():
    exports = clean_exports()
    port = clean_port_traffic()
    lsc = clean_lsc()

    exports.to_csv(PROCESSED_DIR / "exports_2016_2019.csv", index=False)
    port.to_csv(PROCESSED_DIR / "port_traffic_2016_2019.csv", index=False)
    lsc.to_csv(PROCESSED_DIR / "lsc_yearly_2016_2019.csv", index=False)

    print("Saved:")
    print(" - data/processed/exports_2016_2019.csv", exports.shape)
    print(" - data/processed/port_traffic_2016_2019.csv", port.shape)
    print(" - data/processed/lsc_yearly_2016_2019.csv", lsc.shape)

    print("\nNon-null summary:")
    print("Exports:", exports['exports_usd'].notna().sum())
    print("Port traffic:", port['port_teu'].notna().sum())
    print("LSC:", lsc['lsc_index'].notna().sum())


if __name__ == "__main__":
    main()
