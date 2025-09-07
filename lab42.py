import pandas as pd

input_csv = "diff_dataset.csv"
output_csv = "diff_dataset_with_discrepancy.csv"

df = pd.read_csv(input_csv)

df["discrepancy"] = df.apply(
    lambda d: "NO" if d["diff_myers"] == d["diff_hist"] else "YES",
    axis=1
)

df.to_csv(output_csv, index=False)

print(f"Discrepancy column added and saved to {output_csv}")