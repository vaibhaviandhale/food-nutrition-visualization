import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm

# CONFIG 
CSV_PATH = r"E:\anudip_project\food_nutrition.csv"   # change path if needed
OUT_DIR = "outputs"
os.makedirs(OUT_DIR, exist_ok=True)

pd.set_option('display.width', 120)

#LOAD 
df = pd.read_csv(CSV_PATH)
print("Loaded", len(df), "rows. Columns:", list(df.columns))
print("\nData preview:\n", df.head())

# Ensure numeric columns
for col in ["Calories", "Protein", "Carbs", "Fat"]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Basic stats
print("\nSummary statistics:")
print(df[["Calories","Protein","Carbs","Fat"]].describe().round(2))

# Helper to save figs
def save(fig, name):
    path = os.path.join(OUT_DIR, name)
    fig.savefig(path, dpi=200, bbox_inches='tight')
    print("Saved:", path)

# Graph A: Line (Calories trend) 
fig = plt.figure(figsize=(14,5))
plt.plot(df['Food'], df['Calories'], marker='o', linestyle='-', color='#2a9d8f')
plt.title("Calories in Different Foods")
plt.xlabel("Food Items")
plt.ylabel("Calories")
plt.xticks(rotation=80)
plt.grid(alpha=0.25, linestyle=':')
plt.tight_layout()
save(fig, "01_calories_line.png")
plt.show()

# Graph B: Bar (Top 20 Protein) 
top_protein = df.sort_values(by='Protein', ascending=False).head(20)
fig = plt.figure(figsize=(14,6))
bars = plt.bar(top_protein['Food'], top_protein['Protein'], color=cm.viridis(np.linspace(0.2,0.8,len(top_protein))))
plt.title("Top 20 Foods by Protein (g)")
plt.xlabel("Food Items")
plt.ylabel("Protein (g)")
plt.xticks(rotation=80)
plt.tight_layout()
save(fig, "02_top20_protein.png")
plt.show()

# ----------------- Graph C: Bar (Top 20 Carbs) -----------------
top_carbs = df.sort_values(by='Carbs', ascending=False).head(20)
fig = plt.figure(figsize=(14,6))
plt.bar(top_carbs['Food'], top_carbs['Carbs'], color=cm.inferno(np.linspace(0.2,0.8,len(top_carbs))))
plt.title("Top 20 Foods by Carbohydrates (g)")
plt.xlabel("Food Items")
plt.ylabel("Carbs (g)")
plt.xticks(rotation=80)
plt.tight_layout()
save(fig, "03_top20_carbs.png")
plt.show()

#  Graph D: Donut Chart 
chosen_food = "Egg"
if chosen_food not in df['Food'].values:
    chosen_food = df.loc[df['Calories'] < 400].sort_values(by='Calories', ascending=False).iloc[0]['Food']

row = df[df['Food'] == chosen_food].iloc[0]
labels = ['Protein (g)', 'Carbs (g)', 'Fat (g)']
vals = [row['Protein'], row['Carbs'], row['Fat']]

fig = plt.figure(figsize=(7,7))
wedges, texts, autotexts = plt.pie(vals, labels=labels, autopct='%1.1f%%', startangle=90, pctdistance=0.75)

# Donut hole
centre_circle = plt.Circle((0,0),0.50,fc='white')
fig.gca().add_artist(centre_circle)

plt.title(f"Macronutrient Donut: {row['Food']}")
plt.tight_layout()
save(fig, "04_donut_chosen_food.png")
plt.show()

# Graph E: Scatter (Calories vs Protein)
fig = plt.figure(figsize=(10,6))
sc = plt.scatter(df['Calories'], df['Protein'], s=60, c=df['Fat'], cmap='plasma', alpha=0.85, edgecolor='k')
plt.colorbar(sc, label='Fat (g)')
plt.title("Protein vs Calories (color = Fat)")
plt.xlabel("Calories")
plt.ylabel("Protein (g)")

# annotate top 6 by protein
top_annot = df.sort_values(by='Protein', ascending=False).head(6)
for _, r in top_annot.iterrows():
    plt.annotate(r['Food'], (r['Calories'], r['Protein']), textcoords="offset points", xytext=(5,5), fontsize=8)

plt.grid(alpha=0.2)
plt.tight_layout()
save(fig, "05_scatter_calories_protein.png")
plt.show()

# ----------------- Graph F: Multi-line (first 20 foods) -----------------
subset = df.head(20).reset_index(drop=True)
x = np.arange(len(subset))

fig = plt.figure(figsize=(14,6))
plt.plot(x, subset['Protein'], label='Protein (g)', marker='o')
plt.plot(x, subset['Carbs'], label='Carbs (g)', marker='s')
plt.plot(x, subset['Fat'], label='Fat (g)', marker='^')
plt.xticks(x, subset['Food'], rotation=80)
plt.title("Protein, Carbs & Fat (First 20 Foods)")
plt.xlabel("Food Items")
plt.ylabel("Grams")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()
save(fig, "06_multiline_first20.png")
plt.show()

# Graph G: Horizontal Bar (Top 20 Fat) 
top_fat = df.sort_values(by='Fat', ascending=False).head(20)
fig = plt.figure(figsize=(10,9))
plt.barh(top_fat['Food'], top_fat['Fat'], color=cm.magma(np.linspace(0.2,0.8,len(top_fat))))
plt.title("Top 20 Foods by Fat (g)")
plt.xlabel("Fat (g)")
plt.gca().invert_yaxis()
plt.tight_layout()
save(fig, "07_top20_fat.png")
plt.show()

#  Graph H: Boxplot (Distribution) 
fig = plt.figure(figsize=(10,6))
plt.boxplot([df['Calories'].dropna(), df['Protein'].dropna(), df['Carbs'].dropna(), df['Fat'].dropna()],
            labels=['Calories','Protein','Carbs','Fat'], patch_artist=True)
plt.title("Distribution of Macronutrients (Boxplots)")
plt.grid(alpha=0.2)
plt.tight_layout()
save(fig, "08_boxplots.png")
plt.show()

print("\nAll plots saved to folder:", OUT_DIR)
