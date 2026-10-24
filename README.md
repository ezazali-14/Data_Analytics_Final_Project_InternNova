# E-Commerce Sales & Customer Performance Analytics
**Final Capstone Project | InternNova Data Analytics Internship**  
**Author:** Thuregal Mohammed Ezaz Ali  
**Student ID:** INST26DA050134  
**Date:** October 2026  

---

## 1. Project Title
E-Commerce Sales & Customer Performance Analytics (End-to-End Retail Data Analytics Capstone)

---

## 2. Project Overview
This repository contains an end-to-end Data Analytics Capstone Project analyzing transactional performance for a multi-category retail platform. It covers data extraction, automated data cleaning in Python, statistical exploratory analysis, and an interactive business intelligence dashboard built with Microsoft Power BI.

---

## 3. Problem Statement
Retail organizations frequently face challenges in identifying which product categories and regional territories drive true profitability versus high top-line revenue with razor-thin margins. Uncontrolled discounting and broad, unsegmented marketing often result in misallocated resources. This project aims to:
- Identify primary revenue drivers versus margin contributors across product categories.
- Evaluate customer segment purchasing behavior across Consumer, Corporate, and Home Office groups.
- Assess the impact of promotional discount rates on net profitability.
- Deliver an interactive executive dashboard for real-time commercial monitoring and decision-making.

---

## 4. Dataset Description
The dataset captures retail e-commerce transactions across multiple regional markets:
- **Timeframe:** January 1, 2026 to June 30, 2026
- **Features (12):** `OrderID`, `OrderDate`, `CustomerID`, `Segment`, `Region`, `Product`, `Category`, `BasePrice`, `Quantity`, `Discount`, `Sales`, `Profit`
- **Volume:** 1,200 validated transactions across 12 product lines in 3 categories (Technology, Furniture, Office Supplies).

---

## 5. Tools Used
- **Version Control:** Git, GitHub
- **Programming & Data Manipulation:** Python (Pandas, NumPy)
- **Data Visualization:** Matplotlib, Seaborn
- **Business Intelligence & Modeling:** Microsoft Power BI Desktop (Power Query, DAX)
- **Integrated Development Environment:** Visual Studio Code (VS Code)

---

## 6. Data Cleaning Process
An automated data cleaning pipeline was implemented in `data_prep_and_eda.py`:
1. **Duplicate Elimination:** 15 duplicate transaction records were detected and dropped from the initial 1,215 rows.
2. **Missing Value Imputation:** 25 instances of `null` values in the `Discount` column were identified and imputed with a default baseline of `0.0`.
3. **Data Type Casting:** Explicit data types were assigned for Datetime (`OrderDate`), Integer (`Quantity`), and Floating Point numeric types (`Sales`, `Profit`, `BasePrice`, `Discount`).
4. **Validation:** Produced a clean dataset of 1,200 unique records exported directly to `data/ecommerce_cleaned_data.csv`.

---

## 7. Exploratory Data Analysis (EDA)
Summary statistics were extracted using Pandas `.describe()` across the 1,200 clean transactions:
- **Total Revenue:** ₹ 3,77,10,232.50 (~₹ 3.77 Cr)
- **Total Net Profit:** ₹ 44,05,115.80 (~₹ 44.05 Lakhs)
- **Average Order Value (AOV):** ₹ 31,425.19
- **Average Quantity per Order:** 2.90 units
- **Overall Operating Profit Margin:** 11.68%
- **Correlation Findings:** A strong positive correlation (0.85) between Sales and Profit; a negative correlation (-0.28) between applied Discount rates and Profit margins, demonstrating that heavy discounting erodes profit without proportionally scaling volume.

---

## 8. Visualizations & Power BI Dashboard

### Python Visualizations
Five statistical plots were generated and saved to the `visualizations/` directory:
1. `vis1_sales_profit_by_category.png`: Clustered bar chart showing Technology's heavy revenue share.
2. `vis2_segment_sales_share.png`: Donut chart highlighting Consumer (52.5%), Corporate (32.2%), and Home Office (15.3%).
3. `vis3_monthly_sales_trend.png`: Dual line plot tracking revenue expansion with a peak in February (~₹ 7.8M).
4. `vis4_correlation_heatmap.png`: Heatmap evaluating feature interdependence.
5. `vis5_regional_sales_distribution.png`: Boxplot identifying transaction outliers and variance across Central, East, South, and West territories.

### Power BI Executive Dashboard
A single-page reporting interface built in `Week6_Final_Analytics.pbix`:
- **4 Executive KPI Cards:** Total Sales (₹ 37.71M), Total Profit (₹ 4.41M), Total Orders (1K / 1,200), and Profit Margin % (11.68%).
- **Interactive Slicers:** Region buttons (Central, East, South, West) and a Date Range slider.
- **Dynamic Cross-Filtering:** Selecting any dimension filters the entire canvas in real time.

---

## 9. Key Insights & Business Recommendations

### 5 Key Insights
1. **Category Concentration:** Technology contributes 73.8% of gross revenue (₹ 2,78,38,260.00) and ₹ 34,38,810.00 in total profit.
2. **Margin Efficiency Leader:** Office Supplies delivers the highest profit margin (15.10%), outperforming Technology (12.35%) and Furniture (9.56%).
3. **Consumer Segment Dominance:** Individual consumers generate 52.49% of store turnover (₹ 19.80M).
4. **Seasonal Volatility:** Sales surged in February (~₹ 7.8M) driven by bulk purchases before stabilizing near ₹ 6.5M.
5. **AOV Profile:** High basket size of ₹ 31,425.19 indicates strong enterprise and high-ticket hardware adoption.

### 2 Data-Driven Business Recommendations
1. **Automated Cross-Selling of High-Margin Consumables:** Implement an automated recommendation engine at digital checkout pairing Technology hardware orders with complementary Office Supplies to lift blended transaction margins.
2. **Restructure Corporate Volume Pricing:** Replace flat upfront discounts with tiered post-purchase rebates for Corporate clients to safeguard cash margins on large orders.

---

## 10. Conclusion
This Capstone Project delivered a complete data analytics pipeline from raw CSV data to version control on GitHub, automated cleaning in Python, statistical exploratory analysis, and an interactive Power BI dashboard. The resulting artifacts provide retail stakeholders with clear visibility into profitability, customer segmentation, and inventory strategy.