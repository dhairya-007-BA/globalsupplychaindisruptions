from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"

fact_path = PROCESSED_DIR / "fact_country_year_core_2016_2019_country_only.csv"


def make_tier(series: pd.Series) -> pd.Series:
    valid = series.dropna()
    if valid.empty:
        return pd.Series([np.nan] * len(series), index=series.index)

    q1 = valid.quantile(0.33)
    q2 = valid.quantile(0.67)

    def classify(x):
        if pd.isna(x):
            return np.nan
        if x <= q1:
            return "Low"
        elif x <= q2:
            return "Medium"
        return "High"

    return series.apply(classify)


def main():
    fact = pd.read_csv(fact_path)

    # Complete case flag
    fact["complete_case"] = (
        fact["exports_usd"].notna() &
        fact["port_teu"].notna() &
        fact["lsc_index"].notna()
    )

    # Log transforms
    fact["exports_log"] = fact["exports_usd"].apply(
        lambda x: np.log10(x) if pd.notna(x) and x > 0 else np.nan
    )

    fact["port_teu_log"] = fact["port_teu"].apply(
        lambda x: np.log10(x) if pd.notna(x) and x > 0 else np.nan
    )

    # Tiers
    fact["exports_tier"] = make_tier(fact["exports_usd"])
    fact["port_tier"] = make_tier(fact["port_teu"])
    fact["lsc_tier"] = make_tier(fact["lsc_index"])

    # Save
    output_path = PROCESSED_DIR / "fact_country_year_core_2016_2019_country_only_enhanced.csv"
    fact.to_csv(output_path, index=False)

    print("Saved:")
    print(output_path)

    print("\nShape:")
    print(fact.shape)

    print("\nComplete case count:")
    print(fact["complete_case"].sum())

    print("\nExports tier counts:")
    print(fact["exports_tier"].value_counts(dropna=False))

    print("\nPort tier counts:")
    print(fact["port_tier"].value_counts(dropna=False))

    print("\nLSC tier counts:")
    print(fact["lsc_tier"].value_counts(dropna=False))

    print("\nPreview:")
    print(fact.head(10))


if __name__ == "__main__":
    main()