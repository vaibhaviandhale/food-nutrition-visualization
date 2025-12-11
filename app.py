import os
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -----------------------------
# Config
# -----------------------------
st.set_page_config(page_title="NutriScope 360°", layout="wide", initial_sidebar_state="expanded")
DATA_PATH = "food_nutrition.csv"  # keep your CSV file here

# -----------------------------
# Theme helper (persist to ~/.streamlit/config.toml)
# -----------------------------
def write_streamlit_theme(base: str = "dark"):
    cfg_dir = os.path.join(os.path.expanduser("~"), ".streamlit")
    os.makedirs(cfg_dir, exist_ok=True)
    cfg_path = os.path.join(cfg_dir, "config.toml")

    if base.lower() == "dark":
        content = """
[theme]
base = "dark"
primaryColor = "#ef476f"
backgroundColor = "#0e1117"
secondaryBackgroundColor = "#1b1e24"
textColor = "#e6eef3"
font = "sans serif"
"""
    else:
        content = """
[theme]
base = "light"
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#000000"
font = "sans serif"
"""
    with open(cfg_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    return cfg_path

# -----------------------------
# Load & validate data
# -----------------------------
def load_data(path=DATA_PATH):
    try:
        df = pd.read_csv(path)
    except Exception as e:
        st.error(f"Cannot read CSV at {path}: {e}")
        st.stop()
    df = df.rename(columns=lambda c: c.strip())
    required = ["Food","Calories","Protein","Carbs","Fat"]
    for r in required:
        if r not in df.columns:
            st.error(f"CSV missing required column: {r}. Expected columns: {required}")
            st.stop()
    for col in ["Calories","Protein","Carbs","Fat"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Food"]).reset_index(drop=True)
    return df

df = load_data()

# -----------------------------
# Compact CSS to improve spacing (visual only)
# -----------------------------
compact_css = """
<style>
/* compact page padding */
[data-testid="stAppViewContainer"] { padding-top: 8px; padding-bottom: 8px; }
.block-container { padding-left:18px; padding-right:18px; }

/* Title sizes */
h1 { font-size: 22px !important; margin:0 !important; padding:0 !important; }
h2 { font-size: 18px !important; margin-top:6px !important; }

/* KPI numbers smaller */
.kpi-small { font-size:20px !important; font-weight:600 !important; color:inherit; }
.kpi-label { font-size:12px !important; color:inherit; }

/* Narrow sidebar a bit */
[data-testid="stSidebar"] { min-width: 240px; max-width:260px; }

/* Reduce spacing between Streamlit sections */
section .stButton, section .stSlider { margin-top:6px; margin-bottom:6px; }

/* Small card look for BMI */
.bmi-card { background:#f6f8fa; padding:16px; border-radius:8px; }
</style>
"""
st.markdown(compact_css, unsafe_allow_html=True)

# -----------------------------
# Sidebar: theme + filters
# -----------------------------
st.sidebar.title("NutriScope 360°")

# --- runtime CSS + permanent config option (you already used this) ---
css_dark = """
<style>
body, .stApp, .css-18e3th9 { background-color:#0e1117 !important; color:#e6eef3 !important; }
[data-testid="stSidebar"] { background-color:#0f1216 !important; color:#e6eef3 !important; }
.stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>input { background-color:#111214 !important; color:#e6eef3 !important; border:1px solid #222 !important; }
.stButton>button { background-color:#ef476f; color:white; border: none !important; }
[data-testid="stPlotlyChart"] { background-color: transparent !important; }
header { background-color: transparent !important; }
</style>
"""

css_light = """
<style>
body, .stApp, .css-18e3th9 { background-color:#ffffff !important; color:#0f1724 !important; }
[data-testid="stSidebar"] { background-color:#f7f8fa !important; color:#0f1724 !important; }
.stTextInput>div>div>input, .stSelectbox>div>div>div, .stNumberInput>div>input { background-color:#ffffff !important; color:#0f1724 !important; border:1px solid #ddd !important; }
.stButton>button { background-color:#1f77b4; color:white; border: none !important; }
[data-testid="stPlotlyChart"] { background-color: transparent !important; }
header { background-color: transparent !important; }
</style>
"""

if 'runtime_theme' not in st.session_state:
    st.session_state.runtime_theme = 'dark'

theme_choice = st.sidebar.radio("Theme", ["Dark", "Light"], index=0 if st.session_state.runtime_theme=='dark' else 1)

if theme_choice == "Dark":
    st.markdown(css_dark, unsafe_allow_html=True)
    plotly_template = "plotly_dark"
    st.session_state.runtime_theme = 'dark'
else:
    st.markdown(css_light, unsafe_allow_html=True)
    plotly_template = "plotly_white"
    st.session_state.runtime_theme = 'light'

if st.sidebar.button("Apply Theme (save & restart)"):
    cfg_path = write_streamlit_theme(theme_choice.lower())
    st.sidebar.success(f"Theme saved to: {cfg_path}")
    st.sidebar.info("Stop the app (Ctrl+C) and run `streamlit run improved_app.py` to apply permanently.")
    st.stop()

# -------- Filters --------
st.sidebar.header("Filters")
search = st.sidebar.text_input("Search food name", value="")
all_foods = sorted(df["Food"].unique().tolist())
selected_foods = st.sidebar.multiselect("Select foods", options=all_foods, default=all_foods[:8])

cal_min, cal_max = int(df["Calories"].min()), int(df["Calories"].max())
cal_range = st.sidebar.slider("Calories", cal_min, cal_max, (cal_min, cal_max))

pmax = int(df["Protein"].max())
prot_range = st.sidebar.slider("Protein (g)", 0, pmax, (0, pmax))

fmax = int(df["Fat"].max())
fat_range = st.sidebar.slider("Fat (g)", 0, fmax, (0, fmax))

# (Sidebar BMI controls commented out — we moved BMI to main page)
# st.sidebar.markdown("---")
# st.sidebar.header("BMI Quick")
# sb_w = st.sidebar.number_input("Weight (kg)", min_value=1.0, value=60.0, step=0.5)
# sb_h = st.sidebar.number_input("Height (cm)", min_value=30.0, value=165.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.caption("Tip: To change full UI theme permanently, set Streamlit Theme → Dark in Settings or use config file (see README).")

# -----------------------------
# Apply filters to data
# -----------------------------
df_filtered = df.copy()
if search:
    df_filtered = df_filtered[df_filtered["Food"].str.contains(search, case=False, na=False)]
if selected_foods:
    df_filtered = df_filtered[df_filtered["Food"].isin(selected_foods)]
df_filtered = df_filtered[df_filtered["Calories"].between(*cal_range)]
df_filtered = df_filtered[df_filtered["Protein"].between(*prot_range)]
df_filtered = df_filtered[df_filtered["Fat"].between(*fat_range)]

# -----------------------------
# Helper for styling plotly figures
# -----------------------------
def style_fig(fig, theme, height=420, margin_bottom=140):
    fig.update_layout(template=theme,
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)",
                      font_color=None,
                      height=height,
                      margin=dict(l=60, r=40, t=60, b=margin_bottom))
    fig.update_xaxes(tickangle=-45, automargin=True)
    return fig

# -----------------------------
# Main UI
# -----------------------------
st.markdown("## 🍎 NutriScope 360° — Nutrition Intelligence Dashboard")
st.markdown("Interactive visual analyses of Calories, Protein, Carbs and Fat for food items.")
st.markdown("---")

# KPIs
k1,k2,k3,k4 = st.columns(4)
k1.markdown("**Total foods**\n\n" + f"<div style='font-size:20px'>{len(df)}</div>", unsafe_allow_html=True)
k2.markdown("**Selected**\n\n" + f"<div style='font-size:20px'>{len(df_filtered)}</div>", unsafe_allow_html=True)
avg_c = f"{df_filtered['Calories'].mean():.1f}" if len(df_filtered)>0 else "N/A"
k3.markdown("**Avg Calories**\n\n" + f"<div style='font-size:20px'>{avg_c}</div>", unsafe_allow_html=True)
avg_p = f"{df_filtered['Protein'].mean():.1f} g" if len(df_filtered)>0 else "N/A"
k4.markdown("**Avg Protein**\n\n" + f"<div style='font-size:20px'>{avg_p}</div>", unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# Smart BMI + Calorie target + Meal recommendations
# (Replace the old BMI card with this block)
# -----------------------------
st.subheader("Personalized BMI & Meal Recommendations")

# Inputs
col_a, col_b, col_c = st.columns([1,1,1])
with col_a:
    sex = st.selectbox("Sex", ["Female", "Male"], index=0)
    age = st.number_input("Age (years)", min_value=10, max_value=120, value=22, step=1)
with col_b:
    weight = st.number_input("Weight (kg)", min_value=1.0, value=60.0, step=0.5, key="smart_w")
    height = st.number_input("Height (cm)", min_value=30.0, value=165.0, step=0.5, key="smart_h")
with col_c:
    activity = st.selectbox("Activity level", ["Sedentary (little/no exercise)", "Light (1-3 days/wk)", "Moderate (3-5 days/wk)", "Active (6-7 days/wk)"], index=1)
    goal = st.selectbox("Goal", ["Maintain weight", "Mild weight loss (~-500 kcal)", "Mild gain (~+300 kcal)"], index=0)

serve_mult = st.number_input("Serving multiplier (use 1 for default serving)", min_value=0.1, value=1.0, step=0.1)

# Buttons
if st.button("Calculate and Recommend"):
    # 1) BMI
    bmi = round(weight / ((height/100)**2), 1)
    bmi_cat = "Underweight" if bmi < 18.5 else ("Normal" if bmi < 25 else ("Overweight" if bmi < 30 else "Obese"))
    st.markdown(f"**BMI:** {bmi} — *{bmi_cat}*")

    # 2) BMR (Mifflin-St Jeor)
    if sex == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # 3) Activity factor
    act_map = {
        "Sedentary (little/no exercise)": 1.2,
        "Light (1-3 days/wk)": 1.375,
        "Moderate (3-5 days/wk)": 1.55,
        "Active (6-7 days/wk)": 1.725
    }
    tdee = bmr * act_map[activity]

    # 4) Goal adjustment
    if goal == "Maintain weight":
        target_cal = tdee
    elif goal == "Mild weight loss (~-500 kcal)":
        target_cal = max(1200, tdee - 500)  # avoid too-low
    else:
        target_cal = tdee + 300

    target_cal = int(round(target_cal))
    st.markdown(f"**Estimated maintenance (TDEE):** {int(round(tdee))} kcal/day — **Target calories**: {target_cal} kcal/day")

    # 5) Meal split (you can tweak ratios)
    meal_split = {
        "Breakfast": 0.25,
        "Lunch": 0.35,
        "Dinner": 0.30,
        "Snacks": 0.10
    }
    meal_targets = {m: int(target_cal * frac) for m, frac in meal_split.items()}

    st.write("### Meal targets (kcal)")
    mt_cols = st.columns(len(meal_targets))
    for col, (m, kcalv) in zip(mt_cols, meal_targets.items()):
        col.metric(m, f"{kcalv} kcal")

    # 6) Recommendation logic — score foods and pick items per meal
    # We'll create a score depending on goal & bmi category
    df_score = df.copy()
    max_cal = df_score["Calories"].max() if df_score["Calories"].max() > 0 else 1
    max_pro = df_score["Protein"].max() if df_score["Protein"].max() > 0 else 1
    max_fat = df_score["Fat"].max() if df_score["Fat"].max() > 0 else 1

    # Score function: different emphasis for loss/gain/maintain
    def compute_score(row):
        cal = row["Calories"]
        pro = row["Protein"]
        fat = row["Fat"]
        if goal == "Mild weight loss (~-500 kcal)":
            # prefer higher protein, lower calories & moderate fat
            return (pro / max_pro) * 0.6 + (1 - (cal / max_cal)) * 0.3 + (1 - (fat / max_fat)) * 0.1
        elif goal == "Mild gain (~+300 kcal)":
            # prefer calorie-dense & protein rich
            return (cal / max_cal) * 0.5 + (pro / max_pro) * 0.4 + (fat / max_fat) * 0.1
        else:
            # maintain: balanced
            return (pro / max_pro) * 0.5 + (1 - abs(cal - (tdee/len(meal_targets))) / max_cal) * 0.4 + (1 - (fat / max_fat)) * 0.1

    df_score["score"] = df_score.apply(compute_score, axis=1)

    # Meal recommender: pick top foods and estimate small serving counts to approach meal target
    def recommend_for_meal(df_in, meal_kcal, top_n=6):
        # choose candidates with reasonable calories (avoid extremely high single items for small meals)
        candidates = df_in.sort_values("score", ascending=False).head(top_n).copy()
        # estimate servings = clip(meal_kcal / calories, 0.25..2)
        recs = []
        for _, r in candidates.iterrows():
            base_cal = r["Calories"] * serve_mult
            if base_cal <= 0:
                continue
            # propose a serving count to fill part of meal (we won't exceed 2 servings per item by default)
            est_serv = meal_kcal / base_cal
            est_serv = max(0.25, min(round(est_serv, 2), 2.0))  # between 0.25 and 2
            est_kcal = round(base_cal * est_serv)
            est_pro = round(r["Protein"] * serve_mult * est_serv, 1)
            recs.append({
                "Food": r["Food"],
                "Servings": est_serv,
                "Calories": est_kcal,
                "Protein": est_pro,
                "Fat": r["Fat"] * serve_mult * est_serv
            })
        # take top 3 items for brevity (could be combined)
        return pd.DataFrame(recs).head(3)

    # 7) Prepare and display per-meal tables
    st.write("### Suggested meal items (servings approximate)")
    for meal, kcal_target in meal_targets.items():
        st.write(f"**{meal} — target: {kcal_target} kcal**")
        # filter by reasonable calories for meal: allow whole df but score will favor right ones
        meal_rec = recommend_for_meal(df_score, kcal_target, top_n=12)
        if meal_rec.empty:
            st.write("No suggestions found for this meal.")
        else:
            # format and show
            meal_rec_display = meal_rec.copy()
            meal_rec_display["Calories"] = meal_rec_display["Calories"].astype(int)
            meal_rec_display["Protein"] = meal_rec_display["Protein"].astype(float)
            st.table(meal_rec_display.reset_index(drop=True))

    # 8) Daily summary: sum of suggested kcal & protein (approx)
    st.write("### Daily recommendation summary (approx)")
    combined_rows = []
    for meal, kcal_target in meal_targets.items():
        rec_df = recommend_for_meal(df_score, kcal_target, top_n=12)
        if not rec_df.empty:
            combined_rows.append(rec_df.head(3))
    if combined_rows:
        total_df = pd.concat(combined_rows, ignore_index=True)
        total_kcal = int(total_df["Calories"].sum())
        total_pro = round(total_df["Protein"].sum(), 1)
        st.markdown(f"**Estimated calories from suggested items:** {total_kcal} kcal  \n**Estimated protein:** {total_pro} g")
    else:
        st.info("No combined meal suggestions available.")

    # 9) Small caveat
    st.caption("Notes: servings are approximate and use dataset per-serving values. This is a rule-based suggestion for demo/educational use, not medical advice.")
st.markdown("---")


# Line chart
st.subheader("Calories by Food (sorted)")
df_sorted = df.sort_values("Calories", ascending=False).reset_index(drop=True)
fig_line = px.line(df_sorted, x="Food", y="Calories", title=None)
fig_line = style_fig(fig_line, plotly_template, height=360, margin_bottom=140)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("---")

# Donut
st.subheader("Macronutrient Donut")
if len(df_filtered) == 0:
    st.info("No foods selected — adjust filters or select foods.")
else:
    choice = st.selectbox("Choose a food", df_filtered["Food"].tolist(), index=0)
    row = df[df["Food"]==choice].iloc[0]
    fig_p = px.pie(names=["Protein","Carbs","Fat"], values=[row["Protein"], row["Carbs"], row["Fat"]], hole=0.45, title=None)
    fig_p = style_fig(fig_p, plotly_template, height=320, margin_bottom=40)
    st.plotly_chart(fig_p, use_container_width=True)

st.markdown("---")

# Two column charts
c1, c2 = st.columns([1.6,1])
with c1:
    st.subheader("Top Protein (bar)")
    top_n = st.slider("Top N foods for bars", 5, 25, 10)
    top_prot = df.sort_values("Protein", ascending=False).head(top_n)
    fig_bp = px.bar(top_prot, x="Food", y="Protein")
    fig_bp = style_fig(fig_bp, plotly_template, height=360, margin_bottom=120)
    st.plotly_chart(fig_bp, use_container_width=True)

    st.subheader("Top Carbs (bar)")
    top_carbs = df.sort_values("Carbs", ascending=False).head(top_n)
    fig_bc = px.bar(top_carbs, x="Food", y="Carbs")
    fig_bc = style_fig(fig_bc, plotly_template, height=300, margin_bottom=80)
    st.plotly_chart(fig_bc, use_container_width=True)

with c2:
    st.subheader("Protein vs Calories (color = Fat)")
    df_sc = df_filtered if len(df_filtered) > 0 else df
    fig_sc = px.scatter(df_sc, x="Calories", y="Protein", color="Fat", size="Fat", hover_name="Food")
    fig_sc = style_fig(fig_sc, plotly_template, height=760, margin_bottom=120)
    st.plotly_chart(fig_sc, use_container_width=True)

st.markdown("---")

# Multiline and boxplots
r1, r2 = st.columns([2,1])
with r1:
    st.subheader("Protein, Carbs & Fat (first 20)")
    subset = df.head(20).melt(id_vars="Food", value_vars=["Protein","Carbs","Fat"])
    fig_ml = px.line(subset, x="Food", y="value", color="variable", markers=True)
    fig_ml = style_fig(fig_ml, plotly_template, height=360, margin_bottom=120)
    st.plotly_chart(fig_ml, use_container_width=True)

with r2:
    st.subheader("Nutrient Distributions")
    melt = df.melt(value_vars=["Calories","Protein","Carbs","Fat"], var_name="Nutrient", value_name="Value")
    fig_box = px.box(melt, x="Nutrient", y="Value")
    fig_box = style_fig(fig_box, plotly_template, height=360, margin_bottom=120)
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")
st.subheader("Filtered Data")
st.dataframe(df_filtered.reset_index(drop=True), height=320)
st.markdown("---")
st.caption("NutriScope 360° — built with Streamlit & Plotly")
