import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load CSV
df = pd.read_csv("diff_dataset_with_discrepancy.csv")

# For classifying file types (focusing on the 4 required categories)
def classify_file(filepath):
    if pd.isna(filepath):
        return "Other"
    
    filepath = str(filepath).lower()
    
    if "test" in filepath:
        return "Test Code"
    elif "readme" in filepath:
        return "README"
    elif "license" in filepath:
        return "LICENSE"
    elif filepath.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c', '.rb', '.go', '.cs', '.php')):
        return "Source Code"
    else:
        return "Other"

# Apply classification (use new_file_path if exists, otherwise old_file_path)
df["file_type"] = df["new_file_path"].fillna(df["old_file_path"]).apply(classify_file)

# Required categories
required_types = ["Source Code", "Test Code", "README", "LICENSE"]
results = {}

# Calculate stats
for file_type in required_types:
    type_files = df[df["file_type"] == file_type]
    total_count = len(type_files)
    mismatch_count = len(type_files[type_files["discrepancy"] == "YES"])
    mismatch_rate = (mismatch_count / total_count * 100) if total_count > 0 else 0
    
    results[file_type] = {
        "Total Files": total_count,
        "Mismatches": mismatch_count,
        "Mismatch Rate (%)": mismatch_rate
    }

# Convert to DataFrame for display
stats_df = pd.DataFrame(results).T
print("="*60)
print("  REPORT")
print("="*60)
print(stats_df.round(3))
print()

# Print mismatches for each category
print("📈 Requested Statistics:")
for file_type in required_types:
    count = results[file_type]["Mismatches"]
    total = results[file_type]["Total Files"]
    rate = results[file_type]["Mismatch Rate (%)"]
    print(f"• #Mismatches for {file_type} files: {count} out of {total} ({rate:.1f}%)")

# =============================
# Bar Graphs
# =============================

# 1. Mismatch counts
mismatch_counts = [results[ft]["Mismatches"] for ft in required_types]
plt.figure(figsize=(8, 5))
bars1 = plt.bar(required_types, mismatch_counts, color="skyblue", edgecolor="black")
plt.title("Number of Mismatches by File Type", fontsize=14, fontweight="bold")
plt.ylabel("Mismatches")
plt.xticks(rotation=45)

# Add values
for bar, count in zip(bars1, mismatch_counts):
    if count > 0:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 str(count), ha="center", va="bottom", fontweight="bold")

plt.tight_layout()
plt.show()

# 2. Mismatch percentages
mismatch_rates = [results[ft]["Mismatch Rate (%)"] for ft in required_types]
plt.figure(figsize=(8, 5))
bars2 = plt.bar(required_types, mismatch_rates, color="lightgreen", edgecolor="black")
plt.title("Mismatch Rate by File Type (%)", fontsize=14, fontweight="bold")
plt.ylabel("Mismatch Rate (%)")
plt.xticks(rotation=45)

# Add values
for bar, rate in zip(bars2, mismatch_rates):
    if rate > 0:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f"{rate:.1f}%", ha="center", va="bottom", fontweight="bold")

plt.tight_layout()
plt.show()
