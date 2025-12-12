import pandas as pd

def try_read(path):
    # try utf-8, then latin1
    for enc in ("utf-8", "latin1", "ISO-8859-1"):
        try:
            df = pd.read_csv(path, encoding=enc)
            print(f"Read {path} with encoding {enc} -> shape {df.shape}")
            # trim whitespace from column names
            df.columns = df.columns.str.strip()
            return df
        except Exception as e:
            print(f"Failed to read {path} with {enc}: {e}")
    raise ValueError(f"Could not read {path} with common encodings")

# 1) Load files (adjust names if necessary)
demo = try_read("demographic.csv")
diet = try_read("diet.csv")
exam = try_read("examination.csv")
labs = try_read("labs.csv")
meds = try_read("medications.csv")
quest = try_read("questionnaire.csv")

# 2) Quick checks for SEQN presence and unique counts
for name, df in [("demo", demo), ("diet", diet), ("exam", exam),
                 ("labs", labs), ("meds", meds), ("quest", quest)]:
    print(name, "columns sample:", list(df.columns)[:10])
    if "SEQN" in df.columns:
        print(f"  {name} unique SEQN:", df["SEQN"].nunique())
    else:
        print(f"  WARNING: SEQN not in {name} columns!")

# 3) Merge safely: start with demographics and left-merge others
df = demo.copy()
for other, label in [(diet, "diet"), (exam, "exam"), (labs, "labs"),
                     (meds, "meds"), (quest, "quest")]:
    if "SEQN" in other.columns:
        df = df.merge(other, on="SEQN", how="left", suffixes=("", f"_{label}"))
        print("After merging", label, "shape:", df.shape)
    else:
        print("Skipping merge for", label, "because SEQN missing")

# 4) Clean column names again (just in case)
df.columns = df.columns.str.strip()

# 5) Choose metabolic columns that exist in the merged DF
candidate_metabolic = ["BMXWAIST","BPXSY1","BPXDI1","LBXGH","LBXGLU","LBDHDD","LBDLDL","LBXTR"]
metabolic_cols = [c for c in candidate_metabolic if c in df.columns]
print("Metabolic columns found:", metabolic_cols)

# 6) Filter to adults if age variable exists
if "RIDAGEYR" in df.columns:
    df = df[df["RIDAGEYR"] >= 18]
    print("After filtering adults shape:", df.shape)
else:
    print("RIDAGEYR (age) not found; skipping adult filter")

# 7) Drop rows missing ALL metabolic measures (keep rows that have at least one)
if metabolic_cols:
    before = df.shape[0]
    df = df.dropna(subset=metabolic_cols, how="all")
    after = df.shape[0]
    print(f"Dropped rows with no metabolic data: {before-after} rows removed")
else:
    print("No metabolic columns available to filter on; df unchanged")

# 8) Final sample size
print("Final sample size (N):", df.shape[0])

# 9) Save a cleaned file (safe)
df.to_csv("cleaned_data_safe.csv", index=False)
print("Saved cleaned_data_safe.csv")


print(df.columns.tolist())



missing = df.isnull().mean() * 100
print(missing)
