import streamlit as st
import pandas as pd

# App Title
st.title("Data App Assignment, on Oct 7th")

# Load Data
df = pd.read_csv("Superstore_Sales_utf8.csv", parse_dates=["Order_Date"])

# Ensure Order_Date is in datetime format
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Display Data
st.write("### Input Data and Examples")
st.dataframe(df)

# Bar chart of Sales by Category
st.bar_chart(df, x="Category", y="Sales")

# Fix: Exclude datetime columns before aggregation
numerical_columns = df.select_dtypes(include=['number']).columns

# Aggregated sales by Category
st.dataframe(df.groupby("Category")[numerical_columns].sum())
st.bar_chart(df.groupby("Category", as_index=False)[numerical_columns].sum(), x="Category", y="Sales", color="#04f")

# Aggregating by time
df.set_index('Order_Date', inplace=True)
sales_by_month = df.filter(items=['Sales']).groupby(pd.Grouper(freq='M')).sum()

st.dataframe(sales_by_month)
st.line_chart(sales_by_month, y="Sales")

# Reset index to ensure 'Order_Date' is accessible after filtering
df.reset_index(inplace=True)

# Your Additions
st.write("## Enhanced Features")

# (1) Dropdown to select Category
selected_category = st.selectbox("Select a Category", df["Category"].unique())

# Filter dataframe by selected category
filtered_df = df[df["Category"] == selected_category]

# (2) Multi-select for Sub-Category based on selected Category
selected_subcategories = st.multiselect(
    "Select Sub-Categories", 
    filtered_df["Sub_Category"].unique()
)

# Further filter dataframe based on selected subcategories
if selected_subcategories:
    filtered_df = filtered_df[filtered_df["Sub_Category"].isin(selected_subcategories)]

    # Ensure Order_Date is still a column before setting as index
    filtered_df.set_index("Order_Date", inplace=True)

    # (3) Aggregate sales data by month
    sales_by_month = (
        filtered_df
        .groupby(pd.Grouper(freq="M"))["Sales"]
        .sum()
    )

    # Line Chart for Sales
    st.write("### Sales Over Time for Selected Sub-Categories")
    st.line_chart(sales_by_month, y="Sales")

    # (4) Calculate Metrics
    total_sales = filtered_df["Sales"].sum()
    total_profit = filtered_df["Profit"].sum()
    profit_margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0

    # (5) Calculate overall average profit margin
    overall_profit_margin = (df["Profit"].sum() / df["Sales"].sum()) * 100
    profit_margin_delta = profit_margin - overall_profit_margin

    # Display Metrics
    st.write("### Key Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric(
        "Profit Margin (%)",
        f"{profit_margin:.2f}%",
        f"{profit_margin_delta:.2f}%",  # Delta
    )

else:
    st.write("⚠️ Please select at least one Sub-Category to view data.")
