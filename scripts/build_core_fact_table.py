from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

exports_path = PROCESSED_DIR / "exports_2016_2019.csv"
port_path = PROCESSED_DIR / "port_traffic_2016_2019.csv"
lsc_path = PROCESSED_DIR / "lsc_yearly_2016_2019.csv"


def main():
    exports = pd.read_csv(exports_path)
    port = pd.read_csv(port_path)
    lsc = pd.read_csv(lsc_path)

    # Start from exports as the base table
    fact = exports.merge(
        port[["country_code", "year", "port_teu"]],
        on=["country_code", "year"],
        how="left"
    )

    fact = fact.merge(
        lsc[["country_code", "year", "lsc_index"]],
        on=["country_code", "year"],
        how="left"
    )

    # Fill country name from LSC only if missing in exports
    lsc_names = lsc[["country_code", "year", "country_name"]].rename(
        columns={"country_name": "lsc_country_name"}
    )

    fact = fact.merge(
        lsc_names,
        on=["country_code", "year"],
        how="left"
    )

    fact["country_name"] = fact["country_name"].fillna(fact["lsc_country_name"])
    fact = fact.drop(columns=["lsc_country_name"])

    # Availability flags
    fact["has_exports"] = fact["exports_usd"].notna()
    fact["has_port_traffic"] = fact["port_teu"].notna()
    fact["has_lsc"] = fact["lsc_index"].notna()

    # Save
    output_path = PROCESSED_DIR / "fact_country_year_core_2016_2019.csv"
    fact.to_csv(output_path, index=False)

    # Reporting
    print("Saved:")
    print(f" - {output_path}")

    print("\nShape:")
    print(fact.shape)

    print("\nNon-null summary:")
    print("Exports:", fact["exports_usd"].notna().sum())
    print("Port traffic:", fact["port_teu"].notna().sum())
    print("LSC:", fact["lsc_index"].notna().sum())

    all_three = fact[
        fact["exports_usd"].notna() &
        fact["port_teu"].notna() &
        fact["lsc_index"].notna()
    ]

    print("\nRows with all 3 metrics:")
    print(all_three.shape[0])

    print("\nUnique countries in final table:")
    print(fact["country_code"].nunique())

    print("\nUnique countries with all 3 metrics:")
    print(all_three["country_code"].nunique())

    print("\nMissingness by metric:")
    print(fact[["exports_usd", "port_teu", "lsc_index"]].isna().sum())

    print("\nPreview:")
    print(fact.head(10))


if __name__ == "__main__":
    main()
