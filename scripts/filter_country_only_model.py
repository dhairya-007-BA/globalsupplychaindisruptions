from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

dim_country_path = PROCESSED_DIR / "dim_country.csv"
fact_path = PROCESSED_DIR / "fact_country_year_core_2016_2019.csv"


def main():
    dim_country = pd.read_csv(dim_country_path)
    fact = pd.read_csv(fact_path)

    print("Original dim_country shape:", dim_country.shape)
    print("Original fact shape:", fact.shape)

    # Keep only rows that look like real countries
    dim_country_country_only = dim_country[
        dim_country["region"].notna() &
        dim_country["income_group"].notna()
    ].copy()

    dim_country_country_only = dim_country_country_only.drop_duplicates(
        subset=["country_code"]
    ).reset_index(drop=True)

    valid_country_codes = dim_country_country_only["country_code"].unique()

    fact_country_only = fact[
        fact["country_code"].isin(valid_country_codes)
    ].copy()

    # Save outputs
    dim_output = PROCESSED_DIR / "dim_country_country_only.csv"
    fact_output = PROCESSED_DIR / "fact_country_year_core_2016_2019_country_only.csv"

    dim_country_country_only.to_csv(dim_output, index=False)
    fact_country_only.to_csv(fact_output, index=False)

    print("\nSaved:")
    print(dim_output)
    print(fact_output)

    print("\nFiltered dim_country shape:", dim_country_country_only.shape)
    print("Filtered fact shape:", fact_country_only.shape)

    print("\nUnique countries in dim_country_country_only:")
    print(dim_country_country_only["country_code"].nunique())

    print("\nUnique countries in fact_country_year_core_2016_2019_country_only:")
    print(fact_country_only["country_code"].nunique())

    print("\nRows with all 3 metrics in country-only fact:")
    all_three = fact_country_only[
        fact_country_only["exports_usd"].notna() &
        fact_country_only["port_teu"].notna() &
        fact_country_only["lsc_index"].notna()
    ]
    print(all_three.shape[0])

    print("\nUnique countries with all 3 metrics:")
    print(all_three["country_code"].nunique())

    print("\nPreview of filtered dim_country:")
    print(dim_country_country_only.head(10))

    print("\nPreview of filtered fact:")
    print(fact_country_only.head(10))


if __name__ == "__main__":
    main()
