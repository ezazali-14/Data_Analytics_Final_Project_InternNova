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