# Project Guide — E-commerce Sales Analysis

This guide explains **everything** in this project, step by step, in simple words. If you are new to Data Science, start here. After reading this guide you will know:

- what this project does,
- what every file and folder means,
- what every column in the dataset means,
- how to run the project yourself,
- how the code works, line by line in plain English,
- and how to answer viva / presentation questions about it.

---

## 1. What is this project?

This project analyses the orders of an **online shop in Bangladesh** for one full year (2025). Each row in the data is one order: what was bought, in which city, how the customer paid, how much discount was given, and how much money (revenue) the shop earned from that order.

Using **Python** with three libraries — **Pandas**, **NumPy** and **Matplotlib** — the project answers these questions:

1. Which month of 2025 had the highest total revenue?
2. Which product category earns the most revenue?
3. Which city places the most valuable orders?
4. Which payment method do customers use most?
5. Do bigger discounts mean higher or lower revenue per order?

The workflow is the standard Data Science workflow:

**generate data → clean data → make summary tables → draw charts → write insights**

> ⚠️ **Important:** the dataset is **synthetic practice data**. That means a computer program
> invented the 600 orders using random numbers. No real shop and no real customers are involved.
> The numbers look realistic so you can practise the full workflow safely, but the results are
> **not real business findings**.

---

## 2. What is inside the project?

Here is every folder and file, one by one.

```text
ecommerce-sales-analysis/
├── README.md
├── PROJECT_GUIDE.md          ← this file
├── requirements.txt
├── .gitignore
├── data/
│   └── ecommerce_sales_dataset.csv
├── src/
│   ├── generate_dataset.py
│   └── analysis.py
├── notebooks/
│   └── ecommerce_sales_analysis.ipynb
└── outputs/
    ├── insights.md
    ├── tables/
    │   ├── summary_statistics.csv
    │   ├── monthly_revenue.csv
    │   ├── revenue_by_category.csv
    │   ├── revenue_by_city.csv
    │   └── correlation_matrix.csv
    └── charts/
        ├── monthly_revenue_trend.png
        ├── revenue_by_category.png
        ├── orders_by_payment_method.png
        └── discount_vs_revenue.png
```

- **README.md** — the short front page of the project: what it is, how to run it, sample charts.
- **PROJECT_GUIDE.md** — this file: the full beginner-friendly explanation of everything.
- **requirements.txt** — a list of the Python libraries the project needs (`pandas`, `numpy`, `matplotlib`, one per line). `pip` reads this file and installs them all at once.
- **.gitignore** — a small text file that tells Git which files **not** to upload to GitHub, such as `__pycache__/` (automatic Python cache files), `*.pyc`, `.ipynb_checkpoints/` (notebook backup files), `.DS_Store` (a macOS system file) and virtual-environment folders (`.venv/`, `venv/`). It keeps the repository clean.
- **data/ecommerce_sales_dataset.csv** — the dataset itself: 600 orders, 11 columns. A CSV file is a plain-text table: commas separate the columns. It is created by `src/generate_dataset.py`. You can open it in Excel or Google Sheets to look at it.
- **src/generate_dataset.py** — the program that **creates** the dataset (fake orders) and saves it as the CSV file above. Run this first.
- **src/analysis.py** — the main program. It reads the CSV, cleans it, builds all summary tables and charts, and writes the insights file. Run this second.
- **notebooks/ecommerce_sales_analysis.ipynb** — a Jupyter Notebook version of the analysis. A notebook lets you run code in small pieces (cells) and see each result right below the code. This one loads the dataset, shows the first rows, builds a revenue-by-category table, builds a monthly revenue table, and draws the monthly trend chart. Good for learning and for presenting interactively.
- **outputs/insights.md** — the written key results, created automatically by `analysis.py` (best month, top category, top city, the discount–revenue correlation).
- **outputs/tables/** — five CSV tables produced by the analysis (explained in section 7).
- **outputs/charts/** — four PNG chart images produced by the analysis (explained in section 7).

The `outputs/` files are **results**, not code. If you delete them, just run `analysis.py` again and they will be created again.

---

## 3. The dataset, column by column

The dataset has **600 rows** (one row = one order) and **11 columns**. The first rows look like this:

| order_id | order_date | month | product_category | unit_price_bdt | quantity | discount_percentage | payment_method | city | delivery_days | revenue_bdt |
|---|---|---|---|---|---|---|---|---|---|---|
| ORD-001 | 2025-09-06 | 9 | Home & Kitchen | 7580.58 | 1 | 26.87 | Nagad | Khulna | 1 | 5543.68 |
| ORD-002 | 2025-04-15 | 4 | Fashion | 4687.88 | 3 | 38.42 | Cash on Delivery | Chattogram | 7 | 8660.39 |
| ORD-003 | 2025-04-07 | 4 | Beauty | 3642.31 | 4 | 14.84 | Nagad | Dhaka | 4 | 12407.18 |

Now each column:

- **order_id** — a unique ID for each order. Example: `ORD-001`, `ORD-002`, … up to `ORD-600`. It is just a label; it is not used in calculations.
- **order_date** — the date the order was placed, written as year-month-day. Example: `2025-09-06` means 6 September 2025. All dates are in 2025.
- **month** — the month number taken from the date: `1` = January, …, `12` = December. Example: order `ORD-001` has month `9` because its date is in September. This column makes it easy to group orders by month.
- **product_category** — what kind of product was bought. There are 6 categories: `Electronics`, `Fashion`, `Grocery`, `Home & Kitchen`, `Beauty`, `Sports`.
- **unit_price_bdt** — the price of **one** item, in Bangladeshi Taka (BDT). The price depends on the category (see the price ranges in section 5). Example: `7580.58` means one item costs 7,580.58 taka.
- **quantity** — how many items are in the order: a whole number from **1 to 5**.
- **discount_percentage** — the discount given on the order, from **0% to 40%**. Example: `26.87` means the customer paid 26.87% less than the full price.
- **payment_method** — how the customer paid. Four options: `Cash on Delivery`, `bKash`, `Nagad`, `Card`.
- **city** — the delivery city. Six cities: `Dhaka`, `Chattogram`, `Khulna`, `Rajshahi`, `Sylhet`, `Barishal`.
- **delivery_days** — how many days the delivery took: a whole number from **1 to 7**.
- **revenue_bdt** — the money the shop actually earned from this order. It is **calculated**, not random:

  ```
  revenue_bdt = unit_price_bdt × quantity × (1 − discount_percentage / 100)
  ```

In words: price of one item, times the number of items, minus the discount. Check with `ORD-001`: 7580.58 × 1 × (1 − 26.87/100) = 7580.58 × 0.7313 ≈ **5543.68** ✓ And `ORD-002`: 4687.88 × 3 × (1 − 38.42/100) = 14,063.64 × 0.6158 ≈ **8660.39** ✓

---

## 4. How to run the project from zero

### Step 1 — Install Python

Install Python 3 from [python.org](https://www.python.org/downloads/) if you do not have it. Check it works by opening a terminal (Command Prompt / Terminal) and typing:

```bash
python --version
```

### Step 2 — Open the project folder in the terminal

```bash
cd ecommerce-sales-analysis
```

(All commands below are run from inside this project folder.)

### Step 3 — Install the libraries

```bash
pip install -r requirements.txt
```

This installs Pandas, NumPy and Matplotlib — the three libraries the code uses.

### Step 4 — Generate the dataset

```bash
python src/generate_dataset.py
```

You should see a message like `Dataset created: ... Rows: 600 | Columns: 11`. This creates (or re-creates) `data/ecommerce_sales_dataset.csv`.

### Step 5 — Run the analysis

```bash
python src/analysis.py
```

This prints `Analysis complete.` plus the best month, top category and top city.

### Step 6 — See the outputs

- Read the key results: open **`outputs/insights.md`**
- Look at the pictures: open the PNG files in **`outputs/charts/`**
- Look at the numbers: open the CSV files in **`outputs/tables/`** (they open in Excel / Google Sheets too)
- Optional: open **`notebooks/ecommerce_sales_analysis.ipynb`** in Jupyter or VS Code and run the cells one by one to explore interactively.

> Tip: you can run Step 4 and Step 5 again any time. The outputs are overwritten with
> fresh results. Because the random seed is fixed (see section 5), you get the **same**
> dataset and the **same** results every time.

---

## 5. Code explanation: `src/generate_dataset.py`

This file **creates the fake data**. We walk through it in the order it runs.

### 5.1 Imports and file paths

```python
from pathlib import Path
import numpy as np
import pandas as pd
```

- `numpy` (short name `np`) — for random numbers and maths.
- `pandas` (short name `pd`) — for building the table (DataFrame) and saving it as CSV.
- `Path` — for working with file paths safely.

```python
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "data" / "ecommerce_sales_dataset.csv"
```

This finds the project folder (one level above `src/`) and sets the exact place where the CSV will be saved: `data/ecommerce_sales_dataset.csv`. Using paths built from the file's own location means the script works no matter where you run it from.

### 5.2 The price ranges

```python
PRICE_RANGES = {
    "Electronics": (1500, 45000),
    "Fashion": (500, 6000),
    "Grocery": (100, 2500),
    "Home & Kitchen": (800, 15000),
    "Beauty": (300, 4000),
    "Sports": (700, 12000),
}
```

This is a **dictionary**: each category name points to a `(minimum, maximum)` price in BDT. Electronics are expensive (a phone can cost 45,000 taka), groceries are cheap. This is what makes the fake data look realistic.

### 5.3 The random seed — why 42?

```python
rng = np.random.default_rng(42)
n = 600
```

`rng` is the **random number generator**. The number `42` is the **seed**. Random numbers in a computer are not truly random — they follow a sequence that starts from the seed. If you use the **same seed**, you get the **same sequence** every time. That is very useful: anyone who runs this project gets exactly the same dataset and the same results, so results can be checked and reproduced. (42 is a popular choice; any number would work.) `n = 600` means we will create 600 orders.

### 5.4 Choosing the category for each order

```python
product_category = rng.choice(
    categories, size=n, p=[0.24, 0.22, 0.20, 0.14, 0.10, 0.10]
)
```

`rng.choice` picks one category for each of the 600 orders. The `p=` list gives the **probability** of each category: Electronics 24% of orders, Fashion 22%, Grocery 20%, Home & Kitchen 14%, Beauty 10%, Sports 10%. (They add up to 1.00 = 100%.) So Electronics appears most often — about 144 orders expected; in the actual data it has 152.

### 5.5 Prices, quantity and discount

```python
unit_price = np.array([rng.uniform(*PRICE_RANGES[cat]) for cat in product_category])
```

For every order, this takes that order's category, looks up its price range, and picks a random price inside it with `rng.uniform` (every value in the range is equally likely). The `*` in `*PRICE_RANGES[cat]` unpacks the pair `(1500, 45000)` into the two arguments `rng.uniform(1500, 45000)`.

```python
quantity = rng.integers(1, 6, size=n)
discount_percentage = np.round(rng.uniform(0, 40, size=n), 2)
```

- `quantity`: random whole numbers from 1 up to (not including) 6 → **1 to 5** items.
- `discount_percentage`: random numbers between 0 and 40, rounded to 2 decimal places.

### 5.6 Payment method, city and delivery days

```python
payment_method = rng.choice(["Cash on Delivery", "bKash", "Nagad", "Card"],
                            size=n, p=[0.38, 0.30, 0.14, 0.18])
city = rng.choice(["Dhaka", "Chattogram", "Khulna", "Rajshahi", "Sylhet", "Barishal"],
                  size=n, p=[0.42, 0.18, 0.11, 0.11, 0.10, 0.08])
delivery_days = rng.integers(1, 8, size=n)
```

Same `choice` idea, with realistic probabilities: Cash on Delivery is most common (38%), bKash next (30%); Dhaka gets the most orders (42%) because it is the biggest city. `delivery_days` is a random whole number from 1 to 7.

### 5.7 Order dates

```python
start = np.datetime64("2025-01-01")
order_date = start + rng.integers(0, 365, size=n)
order_date = pd.to_datetime(order_date)
month = order_date.month
```

Start at 1 January 2025 and add a random number of days (0–364) → a random date in 2025 for each order. Then the **month number** (1–12) is taken from the date and stored in its own column, so the analysis can group by month easily.

### 5.8 Revenue and saving the CSV

```python
revenue = unit_price * quantity * (1 - discount_percentage / 100)
```

This is the revenue formula from section 3, applied to all 600 orders at once. NumPy does the maths on whole columns (arrays) in one line — no loop needed.

```python
df = pd.DataFrame({ "order_id": ..., "order_date": ..., ... })
df.to_csv(DATA_PATH, index=False)
```

All the columns are put together into a Pandas **DataFrame** (a table). `order_id` values are made with a small loop: `ORD-001`, `ORD-002`, … Finally `to_csv` writes the table to the CSV file. `index=False` means "do not add an extra row-number column" — the file stays clean.

The last lines of the file (`if __name__ == "__main__": main()`) simply mean: "when someone runs this file directly, start the `main()` function."

---

## 6. Code explanation: `src/analysis.py`

This file **reads the data and produces every table, chart and the insights file**.

### 6.1 Setup

At the top it imports `matplotlib.pyplot` (short name `plt`) for charts, plus NumPy and Pandas, and sets the paths for the data file and the two output folders.

```python
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    plt.style.use("ggplot")
```

This picks a nice chart style (a light grid). If that style is not available in your Matplotlib version, it falls back to the `ggplot` style instead of crashing.

The helper function `save_bar_chart(...)` draws a bar chart from a Pandas Series and saves it as a PNG. It sets the title, axis labels, rotates the x labels by 25 degrees so long names fit, and saves at `dpi=160` (good image quality). Charts 2 and 3 reuse it, so their code stays short.

### 6.2 Loading and cleaning the data

```python
df = pd.read_csv(DATA_PATH, parse_dates=["order_date"])
```

Reads the CSV into a DataFrame. `parse_dates` tells Pandas to treat `order_date` as real dates, not plain text.

```python
df = df.drop_duplicates().copy()
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
df = df.dropna(subset=["revenue_bdt"])
```

Cleaning, in plain words:

1. `drop_duplicates()` — remove any fully repeated rows.
2. Find all numeric columns and force them to be numbers (`errors="coerce"` turns anything that is not a number into `NaN`, meaning "missing").
3. `dropna(subset=["revenue_bdt"])` — remove rows where revenue is missing, because revenue is the most important column in this project.

### 6.3 The summary tables (the `groupby` part)

**`summary_statistics.csv`** — one line of code:

```python
df.describe(include="all").round(2).to_csv(...)
```

`describe()` gives, for every numeric column: count, mean (average), standard deviation, minimum, quartiles and maximum. It is the quickest way to "meet" a new dataset.

**`monthly_revenue.csv`** — group by month:

```python
monthly = df.groupby("month").agg(
    orders=("order_id", "count"),
    total_revenue_bdt=("revenue_bdt", "sum"),
    avg_order_value_bdt=("revenue_bdt", "mean"),
).round(2)
```

`groupby("month")` splits the 600 orders into 12 groups, one per month. `.agg(...)` then calculates three things per group: how many orders (`count`), total revenue (`sum`) and average order value (`mean`). Result: a 12-row table.

**`revenue_by_category.csv`** — the same pattern grouped by `product_category`: orders, total revenue, and average discount per category, then `.sort_values("total_revenue_bdt", ascending=False)` puts the biggest category on top.

**`revenue_by_city.csv`** — the same pattern grouped by `city`: orders, total revenue and average order value per city, biggest city first.

**`correlation_matrix.csv`**:

```python
corr = df[corr_cols].corr(numeric_only=True).round(2)
```

For the five numeric columns (`unit_price_bdt`, `quantity`, `discount_percentage`, `delivery_days`, `revenue_bdt`) this computes the **correlation** between every pair. Correlation is a number from −1 to +1: near **+1** means "when one goes up, the other tends to go up", near **−1** means "when one goes up, the other tends to go down", and near **0** means "no clear relationship".

### 6.4 The four charts

- **Chart 1 — `monthly_revenue_trend.png` (line chart).** Plots the `monthly` table: month on the x-axis, total revenue on the y-axis, with a dot on each month (`ax.plot(..., marker="o")`). Made directly from the monthly table of section 6.3.
- **Chart 2 — `revenue_by_category.png` (bar chart).** Uses the `save_bar_chart` helper on the category table's total revenue, so the tallest bar is the top-earning category.
- **Chart 3 — `orders_by_payment_method.png` (bar chart).** `df["payment_method"].value_counts()` counts how many orders used each payment method, and the helper draws it as a purple bar chart.
- **Chart 4 — `discount_vs_revenue.png` (scatter chart).** One dot per order: discount % on the x-axis, revenue on the y-axis (`ax.scatter`). Then a **trend line** is fitted with NumPy:

  ```python
  slope, intercept = np.polyfit(df["discount_percentage"], df["revenue_bdt"], 1)
  ```

`polyfit` finds the straight line that best fits the cloud of dots. If the line slopes down, higher discounts tend to come with lower revenue, and vice versa.

### 6.5 Writing `insights.md`

At the end, the script pulls out the headline answers from the tables it just made:

```python
best_month = int(monthly["total_revenue_bdt"].idxmax())
top_category = by_category.index[0]
top_city = by_city.index[0]
discount_revenue_corr = corr.loc["discount_percentage", "revenue_bdt"]
```

- `idxmax()` — the month whose total revenue is the maximum.
- `index[0]` — the first row of the sorted category/city tables = the top one.
- `corr.loc[...]` — picks one cell from the correlation matrix.

These values are then placed into a Markdown text (an f-string) and written to `outputs/insights.md` with `INSIGHTS_PATH.write_text(...)`. So the insights file is **not typed by hand** — it is generated from the data, and it updates automatically if the data changes.

---

## 7. How to read the outputs

### The charts

- **monthly_revenue_trend.png** — Look for **peaks and dips**. A peak month (here month 7) is when the shop earned most; a steady upward line would mean growth, a flat wavy line means stable sales. Ask: "is there a seasonal pattern?"
- **revenue_by_category.png** — Compare bar heights. One very tall bar (Electronics) means the business depends heavily on one category. Ask: "where does the money come from?"
- **orders_by_payment_method.png** — Shows customer habits. Here Cash on Delivery and bKash dominate, which is typical for Bangladesh. Ask: "how do customers prefer to pay?"
- **discount_vs_revenue.png** — Look at the **direction of the dot cloud and the trend line**. Here it is almost flat, sloping very slightly down — discount and revenue have only a weak relationship in this data. A clear upward slope would mean discounts come with bigger orders; a clear downward slope would mean discounts mostly cut income.

### The tables

- **summary_statistics.csv** — Your first health check of the data: averages, min/max. Example: if max `delivery_days` were 700, you would know something is wrong.
- **monthly_revenue.csv** — 12 rows: orders, total revenue and average order value per month. Use it to find the best and worst months with exact numbers.
- **revenue_by_category.csv** — Categories ranked by revenue, with average discount. Use it to see whether high-revenue categories also give high discounts.
- **revenue_by_city.csv** — Cities ranked by revenue, with average order value. A city can have few orders but a high average order value — both columns matter.
- **correlation_matrix.csv** — A grid of numbers between −1 and +1. Find the `revenue_bdt` row/column to see what moves together with revenue (unit price and quantity correlate positively, because revenue is built from them; discount correlates weakly negatively — see the viva section).

---

## 8. Key results of this project

These are the actual results from `outputs/insights.md` (synthetic data, seed 42):

- Dataset size: **600 orders** across 2025.
- Total revenue in the dataset: **12,422,273.73 BDT**.
- The best month by revenue is **month 7 (July)** with **1,513,209.77 BDT**.
- The top product category by revenue is **Electronics** — **8,389,877.75 BDT from 152 orders** (about two-thirds of all revenue, because Electronics prices are much higher than other categories).
- The top city by revenue is **Dhaka** with **5,428,932.84 BDT** (Dhaka also had the most orders — 42% probability in the generator).
- Correlation between discount percentage and revenue: **−0.12** (a weak negative relationship — explained in the viva section below).

---

## 9. Viva / presentation help

Likely questions a teacher may ask, with short model answers.

**Q1. Why did you use Pandas?** Pandas is made for table data. With it I can load a CSV in one line, clean it, group rows with `groupby`, and calculate sums, counts and averages per group very easily. Doing the same work with plain Python lists would take much more code.

**Q2. Why NumPy?** NumPy handles numbers and arrays. Here it generates all the random data (`rng.choice`, `rng.uniform`, `rng.integers`), calculates revenue for all 600 rows in one line, and fits the trend line in the scatter chart with `np.polyfit`.

**Q3. What is `groupby`?** `groupby` splits a table into groups by a column's values — for example, all orders of one month together — then calculates something for each group, like the sum of revenue. It turns 600 rows into a small summary table, such as 12 rows (one per month).

**Q4. How is `revenue_bdt` calculated?** Revenue = unit price × quantity × (1 − discount/100). It is the money left after the discount is removed. Example: 4687.88 × 3 × (1 − 0.3842) ≈ 8660.39 BDT.

**Q5. What is correlation? What does −0.12 mean?** Correlation measures how two numeric columns move together, from −1 to +1. −0.12 between discount and revenue means a **weak negative** relationship: orders with bigger discounts earn *slightly* less on average, but the effect is small and the dots in the scatter chart are spread widely.

**Q6. Why does discount show a weak negative correlation with revenue in this project?** Two reasons. First, the discount directly cuts the price in the revenue formula, so a bigger discount mechanically reduces revenue for the same items. Second, in this synthetic data the discount was chosen **randomly and independently** — it is not linked to expensive products or big quantities. So the price-cutting effect wins, but only slightly, because revenue is mostly driven by unit price and quantity, which vary a lot. That is why the correlation is negative but weak (−0.12), not strong.

**Q7. Why did you use a random seed (42)?** So the "random" data is reproducible. With the same seed, anyone running the generator gets the identical dataset and identical results. Without a seed, every run would give different numbers and nobody could verify my results.

**Q8. Why is the data synthetic? Is that a problem?** Synthetic data is invented by a program to practise the workflow safely, without needing a real shop's private sales data. It is fine for learning and demonstration, but the findings (best month, top category) are **not real business results**. With real data, the same code would produce real findings.

**Q9. Does correlation prove that discounts *cause* lower revenue?** No. Correlation is not causation. Here we can explain the pattern from the revenue formula itself, but in real data a correlation alone never proves cause and effect — other factors (product price, quantity, season) also play a role.

**Q10. What does `describe()` do?** `df.describe()` gives a quick statistical summary of every numeric column: count, mean, standard deviation, minimum, the 25%/50%/75% values, and maximum. It is the fastest way to check whether data looks reasonable when you first load it.

---

## 10. What to learn next / how to extend

1. **Use real data.** Export real order data from an actual shop (or a public dataset) into the same CSV format. The analysis code will work unchanged — only the generator step is skipped.
2. **Add customer analysis.** Add a `customer_id` column and study repeat buyers: how many customers order more than once, and what is the average basket size?
3. **Predict revenue with Machine Learning.** Use scikit-learn to train a simple model that predicts `revenue_bdt` from category, quantity, discount and city — then compare its accuracy with the real values.
4. **Build a dashboard.** Turn the charts into an interactive Streamlit dashboard where a user can filter by month, city or category and see the tables update live.

---

*End of guide. Good luck with your presentation! 🎓*
