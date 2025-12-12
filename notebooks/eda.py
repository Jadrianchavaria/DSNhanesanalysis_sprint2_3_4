import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned data
df = pd.read_csv("cleaned_data_safe.csv")



# ---- Univariate Analysis ---- #

# 1. Age distribution
plt.figure(figsize=(10, 6))
sns.histplot(df["RIDAGEYR"].dropna(), bins=30, kde=True)
plt.title("Age Distribution")
plt.xlabel("Age (years)")
plt.ylabel("Count")
plt.show()

# 2. BMI distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["BMXBMI"].dropna(), bins=30, kde=True)
plt.title("BMI Distribution")
plt.xlabel("BMI")
plt.ylabel("Count")
plt.show()

# 3. A1C LBXGH distribution
plt.figure(figsize=(8, 5))
sns.histplot(df["LBXGH"].dropna(), bins=30, kde=True)
plt.title("Hemoglobin A1C Distribution")
plt.xlabel("A1C%")
plt.ylabel("Count")
plt.show()

# ---- Bivariate Analysis ---- #

# Scatterplot BMI vs A1C
plt.figure(figsize=(7, 5))
sns.scatterplot(x=df["BMXBMI"], y=df["LBXGH"])
plt.title("Relationship Between BMI and A1C")
plt.xlabel("BMI (kg/m^2)")
plt.ylabel("A1C (%)")
plt.show()

# Boxplot: A1C by gender
plt.figure(figsize=(8, 5))
sns.boxplot(x=df["RIAGENDR"], y=df["LBXGH"])
plt.title("A1C Levels by Gender (1 = Male, 2 = Female)")
plt.xlabel("Gender")
plt.ylabel("A1C%")
plt.show()

# ---- Correlation Heatmap of Metabolic Variables ---- #

metabolic_vars = ["BMXBMI", "BMXWAIST", "BPXSY1", "BPXDI1", "LBXGH", "LBDHDD", "LBXTR"]

plt.figure(figsize=(10, 7))
sns.heatmap(df[metabolic_vars].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap of Metabolic Variables")
plt.show()
