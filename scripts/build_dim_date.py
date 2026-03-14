from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def main():
    years = [2016, 2017, 2018, 2019]

    dim_date = pd.DataFrame({
        "year": years,
        "year_label": [str(y) for y in years],
        "year_sort": years,
        "period_group": ["Core Window"] * len(years)
    })

    output_path = PROCESSED_DIR / "dim_date.csv"
    dim_date.to_csv(output_path, index=False)

    print("Saved:")
    print(output_path)

    print("\nShape:")
    print(dim_date.shape)

    print("\nPreview:")
    print(dim_date)


if __name__ == "__main__":
    main()