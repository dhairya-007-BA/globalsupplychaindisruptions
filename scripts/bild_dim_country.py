from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

country_meta_path = RAW_DIR / "API_IS" / "Metadata_Country_API_IS.SHP.GOOD.TU_DS2_en_csv_v2_186.csv"
fact_path = PROCESSED_DIR / "fact_country_year_core_2016_2019.csv"


def main():
    meta = pd.read_csv(country_meta_path)
    fact = pd.read_csv(fact_path)

    print("Metadata columns:")
    print(list(meta.columns))

    # Keep only likely useful columns if they exist
    desired_cols = [
        "Country Code",
        "TableName",
        "Region",
        "IncomeGroup",
        "SpecialNotes"
    ]

    available_cols = [col for col in desired_cols if col in meta.columns]
    dim_country = meta[available_cols].copy()

    # Rename columns
    rename_map = {
        "Country Code": "country_code",
        "TableName": "country_name",
        "Region": "region",
        "IncomeGroup": "income_group",
        "SpecialNotes": "special_notes"
    }

    dim_country = dim_country.rename(columns=rename_map)

    # Keep only countries that appear in the fact table
    fact_countries = fact["country_code"].dropna().unique()
    dim_country = dim_country[dim_country["country_code"].isin(fact_countries)].copy()

    # Remove duplicates if any
    dim_country = dim_country.drop_duplicates(subset=["country_code"]).reset_index(drop=True)

    output_path = PROCESSED_DIR / "dim_country.csv"
    dim_country.to_csv(output_path, index=False)

    print("\nSaved:")
    print(output_path)

    print("\nShape:")
    print(dim_country.shape)

    print("\nPreview:")
    print(dim_country.head(10))

    if "region" in dim_country.columns:
        print("\nRegion counts:")
        print(dim_country["region"].value_counts(dropna=False))

    if "income_group" in dim_country.columns:
        print("\nIncome group counts:")
        print(dim_country["income_group"].value_counts(dropna=False))


if __name__ == "__main__":
    main()
