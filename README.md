🍎 Food Nutrition Visualization
A Data Visualization Project Using Python, Pandas & Matplotlib

This project analyzes 50 different food items and visualizes their nutritional composition — including Calories, Protein, Carbohydrates, and Fat.
The goal is to understand patterns in nutrition data and identify foods that are high/low in specific nutrients.

📊 Project Features

This project includes:

✔ Line chart — Calories trend
✔ Bar charts — Top protein & carb foods
✔ Donut chart — Macronutrient distribution
✔ Scatter plot — Protein vs Calories (colored by Fat)
✔ Multi-line comparison — Protein, Carbs & Fat
✔ Horizontal bar chart — Top fatty foods
✔ Boxplots — Distribution of all nutrients

All graphs are stored in the outputs/ folder.

📁 Project Structure
food-nutrition-visualization/
│
├── food_nutrition.csv             → Dataset (50 food items)
├── food_nutrition.py              → Python code for all visualizations
│
└── outputs/                       → All generated graph images
    ├── 01_calories_line.png
    ├── 02_top20_protein.png
    ├── 03_top20_carbs.png
    ├── 04_donut_chosen_food.png
    ├── 05_scatter_calories_protein.png
    ├── 06_multiline_first20.png
    ├── 07_top20_fat.png
    ├── 08_boxplots.png

🧠 Problem Statement

The goal of this project is to explore nutrition patterns using data visualization techniques and answer questions like:

Which foods are high in calories?

Which foods contain the most protein?

Are calories related to fat content?

How do different foods compare in terms of macronutrients?

🧪 Technologies Used
Tool / Library	Purpose
Python	Main programming language
Pandas	Data loading & cleaning
Matplotlib	Graph plotting
NumPy	Numerical operations
📈 Example Insights

Some findings from the analysis:

High-calorie foods: Walnuts, Almonds, Bread, Paneer

High-protein foods: Chicken, Eggs, Almonds, Fish

High-carb foods: Rice, Bread, Pasta

High-fat foods: Ghee, Walnuts, Coconut, Cheese

Calories show strong correlation with Fat

Visualization helps make these insights clear and easy to understand.

🚀 How to Run This Project

Clone the repository:

git clone https://github.com/vaibhaviandhale/food-nutrition-visualization.git


Install dependencies:

pip install pandas matplotlib numpy


Run the Python script:

python food_nutrition.py


All charts will be saved inside the outputs/ folder automatically.

🏁 Conclusion

This project demonstrates how data visualization can help uncover useful nutritional insights.
Understanding food composition can guide healthier choices and highlight nutrient-rich foods.

If you found this useful, ⭐ please star the repository!
