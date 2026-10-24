import numpy as np
import pandas as pd

# Set fixed seed for reproducibility
np.random.seed(42)

n_records = 1200

order_ids = [f"ORD-2026-{1000 + i}" for i in range(n_records)]
dates = pd.date_range(start="2026-01-01", end="2026-06-30", periods=n_records)

customers = [f"CUST-{100 + i}" for i in range(120)]
segments = ["Consumer", "Corporate", "Home Office"]
segment_weights = [0.52, 0.31, 0.17]

regions = ["Central", "East", "South", "West"]
region_weights = [0.28, 0.32, 0.18, 0.22]

products = {
    "Laptop": ("Technology", 52000, 0.18),
    "Smartphone": ("Technology", 28000, 0.20),
    "Monitor": ("Technology", 14000, 0.15),
    "Wireless Mouse": ("Technology", 950, 0.25),
    "Office Chair": ("Furniture", 8500, 0.16),
    "Executive Desk": ("Furniture", 19500, 0.14),
    "Bookshelf": ("Furniture", 6200, 0.18),
    "Desk Lamp": ("Furniture", 1600, 0.22),
    "Paper Ream": ("Office Supplies", 350, 0.24),
    "Binder Pack": ("Office Supplies", 220, 0.22),
    "Storage Box": ("Office Supplies", 650, 0.19),
    "Stapler Set": ("Office Supplies", 380, 0.20),
}

product_names = list(products.keys())
prod_choices = np.random.choice(product_names, size=n_records)

data = []
for i in range(n_records):
  p_name = prod_choices[i]
  cat, base_price, target_margin = products[p_name]
  cust = np.random.choice(customers)
  seg = np.random.choice(segments, p=segment_weights)
  reg = np.random.choice(regions, p=region_weights)
  qty = np.random.randint(1, 6)

  # Realistic discounts: 0%, 5%, 10%, 15%, 20%
  disc = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], p=[0.4, 0.2, 0.2, 0.1, 0.1])
  gross_sales = base_price * qty
  net_sales = round(gross_sales * (1 - disc), 2)

  # Profit calculation with discount impact
  cost = gross_sales * (1 - target_margin)
  profit = round(net_sales - cost, 2)

  data.append({
      "OrderID": order_ids[i],
      "OrderDate": dates[i].strftime("%Y-%m-%d"),
      "CustomerID": cust,
      "Segment": seg,
      "Region": reg,
      "Product": p_name,
      "Category": cat,
      "BasePrice": base_price,
      "Quantity": qty,
      "Discount": disc,
      "Sales": net_sales,
      "Profit": profit,
  })

df_raw = pd.DataFrame(data)

# Inject deliberate imperfections for Task 3 data cleaning
# 1. Null values in Discount
df_raw.loc[np.random.choice(df_raw.index, size=25, replace=False), "Discount"] = (
    np.nan
)
# 2. Add duplicate rows
duplicates = df_raw.iloc[:15].copy()
df_raw = pd.concat([df_raw, duplicates], ignore_index=True)

# Save Raw Uncleaned Dataset
df_raw.to_csv("data/ecommerce_raw_data.csv", index=False)
print("--> Saved raw dataset: data/ecommerce_raw_data.csv")
print(f"    Raw Shape: {df_raw.shape}")

# ==========================================
# TASK 3: DATA INSPECTION & CLEANING PIPELINE
# ==========================================
print("\n--- TASK 3: INSPECTING & CLEANING DATA ---")
print(f"1. Total initial records: {len(df_raw)}")
print(f"2. Duplicate records detected: {df_raw.duplicated().sum()}")

# Drop duplicates
df_clean = df_raw.drop_duplicates().copy()
print(f"   Shape after removing duplicates: {df_clean.shape}")

# Handle Missing Values
null_discounts = df_clean["Discount"].isnull().sum()
print(f"3. Null values in 'Discount' column: {null_discounts}")
df_clean["Discount"] = df_clean["Discount"].fillna(0.0)
print("   Filled null discounts with 0.0")

# Enforce correct data types
df_clean["OrderDate"] = pd.to_datetime(df_clean["OrderDate"])
df_clean["Quantity"] = df_clean["Quantity"].astype(int)
df_clean["BasePrice"] = df_clean["BasePrice"].astype(float)
df_clean["Sales"] = df_clean["Sales"].astype(float)
df_clean["Profit"] = df_clean["Profit"].astype(float)

# Save Cleaned Dataset
df_clean.to_csv("data/ecommerce_cleaned_data.csv", index=False)
print("--> Saved clean dataset: data/ecommerce_cleaned_data.csv")
print(f"    Clean Dataset Shape: {df_clean.shape}")
print(
    f"    Total Sales: ₹{df_clean['Sales'].sum():,.2f} | Total Profit: ₹{df_clean['Profit'].sum():,.2f}"
)

# ==========================================
# TASK 4 & TASK 5: EXPLORATORY DATA ANALYSIS (EDA) & VISUALIZATIONS
# ==========================================
import matplotlib.pyplot as plt
import seaborn as sns

print("\n--- TASK 4: EXPLORATORY DATA ANALYSIS (DESCRIPTIVE STATS) ---")
print(df_clean.describe())

# 1. Visualization 1: Sales & Profit by Product Category (Bar Chart)
plt.figure(figsize=(8, 5))
cat_perf = df_clean.groupby("Category")[["Sales", "Profit"]].sum().reset_index()
cat_perf_melted = pd.melt(cat_perf, id_vars=["Category"], value_vars=["Sales", "Profit"], 
                          var_name="Metric", value_name="Amount_INR")

sns.barplot(data=cat_perf_melted, x="Category", y="Amount_INR", hue="Metric", palette=["#1f77b4", "#2ca02c"])
plt.title("Total Sales and Profit by Product Category", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Product Category", fontsize=11)
plt.ylabel("Amount in INR (₹)", fontsize=11)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"₹{x*1e-6:.1f}M"))
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("visualizations/vis1_sales_profit_by_category.png", dpi=300)
plt.close()
print("Saved: visualizations/vis1_sales_profit_by_category.png")

# 2. Visualization 2: Sales Contribution by Customer Segment (Donut Chart)
plt.figure(figsize=(6, 6))
seg_sales = df_clean.groupby("Segment")["Sales"].sum()
colors = ['#2b5c8f', '#e67e22', '#27ae60']
plt.pie(seg_sales, labels=seg_sales.index, autopct='%1.1f%%', startangle=140, 
        colors=colors, wedgeprops=dict(width=0.45, edgecolor='w', linewidth=2))
plt.title("Sales Contribution by Customer Segment", fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig("visualizations/vis2_segment_sales_share.png", dpi=300)
plt.close()
print("Saved: visualizations/vis2_segment_sales_share.png")

# 3. Visualization 3: Monthly Revenue & Profit Trend (Dual Line Chart)
df_clean['YearMonth'] = df_clean['OrderDate'].dt.to_period('M').astype(str)
monthly_trend = df_clean.groupby('YearMonth')[['Sales', 'Profit']].sum().reset_index()

plt.figure(figsize=(9, 4.8))
plt.plot(monthly_trend['YearMonth'], monthly_trend['Sales'], marker='o', linewidth=2.5, color='#1f77b4', label='Revenue (Sales)')
plt.plot(monthly_trend['YearMonth'], monthly_trend['Profit'], marker='s', linewidth=2, color='#2ca02c', linestyle='--', label='Profit')
plt.title("Monthly Sales and Profit Trend (Jan 2026 - Jun 2026)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Month", fontsize=11)
plt.ylabel("Amount in INR (₹)", fontsize=11)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"₹{x*1e-6:.1f}M"))
plt.legend(frameon=True)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("visualizations/vis3_monthly_sales_trend.png", dpi=300)
plt.close()
print("Saved: visualizations/vis3_monthly_sales_trend.png")

# 4. Visualization 4: Correlation Heatmap
plt.figure(figsize=(7, 5))
corr_cols = ['Quantity', 'Discount', 'BasePrice', 'Sales', 'Profit']
corr_matrix = df_clean[corr_cols].corr()
sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='Blues', cbar=True, square=True, linewidths=0.5)
plt.title("Correlation Matrix of Numeric Features", fontsize=13, fontweight='bold', pad=12)
plt.tight_layout()
plt.savefig("visualizations/vis4_correlation_heatmap.png", dpi=300)
plt.close()
print("Saved: visualizations/vis4_correlation_heatmap.png")

# 5. Visualization 5: Sales Distribution Across Geographic Regions (Boxplot / Outliers)
plt.figure(figsize=(8, 4.8))
sns.boxplot(data=df_clean, x='Region', y='Sales', palette='Set2')
plt.title("Order Sales Distribution and Outliers across Regions", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Geographic Region", fontsize=11)
plt.ylabel("Sales per Order (₹)", fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("visualizations/vis5_regional_sales_distribution.png", dpi=300)
plt.close()
print("Saved: visualizations/vis5_regional_sales_distribution.png")

print("\n--- ALL 5 VISUALIZATIONS GENERATED SUCCESSFULLY IN visualizations/ ---")