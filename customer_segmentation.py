
import pandas as pd
import numpy as np
import os

print("======================================")
print("   TASK 3 - CUSTOMER SEGMENTATION")
print("======================================")

# Load dataset
df = pd.read_csv("sales_data.csv")

# Convert Order_Date into date format
df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce")

# Remove records without essential RFM information
df = df.dropna(subset=["Customer_ID", "Order_ID", "Order_Date", "Total_Sales"])

# Snapshot date: one day after the latest order date
snapshot_date = df["Order_Date"].max() + pd.Timedelta(days=1)

# Calculate RFM values customer-wise
rfm = df.groupby("Customer_ID").agg(
    Recency=("Order_Date", lambda x: (snapshot_date - x.max()).days),
    Frequency=("Order_ID", "nunique"),
    Monetary=("Total_Sales", "sum")
).reset_index()

# Add customer details
details = df.groupby("Customer_ID").agg(
    Customer_Name=("Customer_Name", "first"),
    Age=("Age", "median"),
    Gender=("Gender", "first"),
    City=("City", "first")
).reset_index()

rfm = rfm.merge(details, on="Customer_ID", how="left")

# Create RFM scores from 1 to 5
# Lower Recency is better
rfm["R_Score"] = np.ceil(
    (1 - rfm["Recency"].rank(pct=True, method="average")) * 5
).clip(1, 5).astype(int)

# Higher Frequency and Monetary are better
rfm["F_Score"] = np.ceil(
    rfm["Frequency"].rank(pct=True, method="average") * 5
).clip(1, 5).astype(int)

rfm["M_Score"] = np.ceil(
    rfm["Monetary"].rank(pct=True, method="average") * 5
).clip(1, 5).astype(int)

# Customer segmentation
def assign_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif f >= 4 and m >= 3:
        return "Loyal Customers"
    elif r >= 4 and f >= 2:
        return "Potential Loyalists"
    elif r <= 2 and f >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2:
        return "Need Attention"
    else:
        return "Regular Customers"

rfm["Segment"] = rfm.apply(assign_segment, axis=1)

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Save customer-level RFM data
rfm.to_csv("outputs/customer_rfm.csv", index=False)

# Segment summary
segment_summary = rfm.groupby("Segment").agg(
    Customer_Count=("Customer_ID", "nunique"),
    Total_Revenue=("Monetary", "sum"),
    Average_Recency=("Recency", "mean"),
    Average_Frequency=("Frequency", "mean")
).reset_index()

segment_summary.to_csv(
    "outputs/customer_segments_summary.csv",
    index=False
)

# Calculate KPIs
total_revenue = df["Total_Sales"].sum()
total_orders = df["Order_ID"].nunique()
total_customers = df["Customer_ID"].nunique()
average_order_value = total_revenue / total_orders if total_orders else 0
total_units_sold = df["Quantity"].sum()

print("\nCUSTOMER SEGMENTATION COMPLETED!")
print("\nRFM DATA - FIRST 5 CUSTOMERS")
print(rfm.head().to_string(index=False))

print("\nCUSTOMER SEGMENT SUMMARY")
print(segment_summary.to_string(index=False))

print("\nBUSINESS KPIs")
print("Total Revenue:", round(total_revenue, 2))
print("Total Orders:", total_orders)
print("Total Customers:", total_customers)
print("Average Order Value:", round(average_order_value, 2))
print("Total Units Sold:", total_units_sold)

print("\nFiles saved inside outputs folder:")
print("1. customer_rfm.csv")
print("2. customer_segments_summary.csv")
print("\nAnalysis completed successfully!")
