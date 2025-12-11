# NutriScope 360° – Food Nutrition Intelligence Dashboard
Dark Mode • Streamlit Interactive Edition • Professional Documentation

---

## Overview
NutriScope 360° is a modern nutrition analytics dashboard that transforms raw food nutrient data into interactive insights.  
Built using Streamlit and optimized for a clean dark-themed interface, it helps users understand macronutrient variations, calorie distribution, and overall nutritional patterns.

This project is suitable for:
- Students
- Educators
- Data analysts
- Nutritionists
- Fitness professionals

---

## Key Features

Core Visualizations:
- Calories Trend Line
- Top Protein-Rich Foods
- Highest Carbohydrate Foods
- Top Fat-Dense Foods
- Macronutrient Donut Chart
- Protein vs Calories Scatter Plot (Color-coded by Fat)
- Multi-Nutrient Line Comparison
- Nutrient Distribution Boxplots

Intelligent Features:
- BMI Calculator (on dashboard)
- Meal Recommendations
- Food Search and Filters
- Light/Dark Mode Toggle
- Dashboard PDF Export (outputs.pdf)

---

## Project Structure

food-nutrition-visualization/
|
|-- app.py                   # Streamlit Nutrition Dashboard
|-- food_nutrition.csv       # Dataset (50 food items)
|-- requirements.txt         # Required Python libraries
|-- README.md                # Project documentation
|
|-- outputs.pdf              # Dashboard screenshot (exported PDF)

---

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly
- NumPy

---

## Installation and Setup

1. Clone the repository:
   git clone https://github.com/vaibhaviandhale/food-nutrition-visualization.git
   cd food-nutrition-visualization

2. Install dependencies:
   pip install -r requirements.txt

3. Run the dashboard:
   streamlit run app.py

---

## Dashboard Preview

Download the full dashboard PDF here:
outputs.pdf

(You can also add screenshots in a screenshots/ folder if needed.)

---

## Insights Generated

- High-calorie foods include almonds, walnuts, bread, and paneer.
- High-protein foods include chicken, eggs, and almonds.
- Carbohydrate-rich foods include rice, pasta, and bread.
- Fat content shows a strong correlation with total calories.
- Nutrient variation is highest in carbohydrates and fats.

---

## Future Enhancements

- Add advanced food recommendation model.
- Add support for user-uploaded custom food datasets.
- Add recipe recommendation engine.
- Add interactive food comparison mode.

---

## Author
Vaibhavi Andhale  
Python Developer • Data Visualization  
Anudip Foundation

---

## License
Open-source for educational and research use.
