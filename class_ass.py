import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("Superstore Performance Analysis and Visalization App")

st. set_page_config(page_title= "Data Analysis Visualsation App", layout="wide")

st.caption("An interactive Streamlit app for analyzing and visualizing the performance of a Superstore sales dataset.")

st.divider()

# st.markdown("##### This app is created to analyze and visualize the performance analysis of the superstore"
#             "dataset. The dataset contains the sales data of a superstore, including information about the products, customers, and sales transactions. The app provides various visualizations and insights to help understand the trends and patterns in the data.")

with st.expander("Click to view the dataset"):
    data = pd.read_excel('superstore.xls')
    st.write(data)

count_order, count_product_id, count_customer, total_sales, total_quan, net_rev, total_profit = st.columns(7)

with count_order:
    st.metric("Total Orders", data["Order ID"].nunique())

with count_product_id:
    st.metric("Total Products", data["Product ID"].nunique())

with count_customer:
    st.metric("Total Customers", data["Customer ID"].nunique())

with total_sales:
    st.metric("Total Sales", f"${data['Sales'].sum():,.2f}")

with total_quan:
    st.metric("Total Quantity Sold", data["Quantity"].sum())

with net_rev:
    data["Net Revenue"] = (data["Sales"]*data["Quantity"]) - (data["Discount"]*data["Sales"]*data["Quantity"])
    st.metric("Net Revenue", f"${data['Net Revenue'].sum():,.2f}")

with total_profit:
    st.metric("Total Profit", f"${data['Profit'].sum():,.2f}")

table_col, chart_col = st.columns(2)

with table_col:
    sales_tab, profit_tab, description = st.tabs(["Sales by Category", "Profit by Category", "Description"])

    with sales_tab:
        st.header("Sales by Category")
        sales_category = data.groupby("Category")["Sales"].sum().sort_values(ascending=False)
        st.dataframe(sales_category)

    with profit_tab:
        st.header("Profit by Category")
        profit_category = data.groupby("Category")["Profit"].sum().sort_values(ascending=False)
        st.dataframe(profit_category)

    with description:
            st.header("Sales Description")

            total_sales = data["Sales"].sum()
            total_orders = data["Order ID"].nunique()
            total_customers = data["Customer ID"].nunique()

            top_category = (
                data.groupby("Category")["Sales"]
                .sum()
                .idxmax()
            )

            top_region = (
                data.groupby("Region")["Sales"]
                .sum()
                .idxmax()
            )

            st.markdown(
                f"""
                The Superstore recorded a total sales value of **${total_sales:,.2f}**
                from **{total_orders:,} orders**, serving **{total_customers:,} unique customers**.

                Sales performance is strongest in the **{top_category}** category, which
                contributes the highest share of revenue. Regionally, the **{top_region}**
                region leads in overall sales, indicating higher customer demand and
                purchasing activity in that area.
                """
            )


with chart_col:
    sales_chart_tab, profit_chart_tab = st.tabs(["Sales by Category Chart", "Profit by Category Chart"])

    with sales_chart_tab:
        st.header("Sales by Category Chart")
        sales_category = data.groupby("Category")["Sales"].sum().reset_index()
        fig = px.bar(sales_category, x="Category", y="Sales", title="Sales by Category")
        st.plotly_chart(fig, use_container_width=True)

    with profit_chart_tab:
        st.header("Profit by Category Chart")
        profit_category = data.groupby("Category")["Profit"].sum().reset_index()
        fig = px.bar(profit_category, x="Category", y="Profit", title="Profit by Category")
        st.plotly_chart(fig, use_container_width=True)

timeseries_col, piechart_col = st.columns(2)
with timeseries_col:
    st.header("Sales Over Time")
    data["Order Date"] = pd.to_datetime(data["Order Date"])
    sales_time = data.groupby("Order Date")["Sales"].sum()
    st.line_chart(sales_time)

with piechart_col:
    st.header("Sales Distribution by Category")
    sales_category = data.groupby("Category")["Sales"].sum()
    fig = px.pie(sales_category, values="Sales", names=sales_category.index, title="Sales Distribution by Category")
    st.plotly_chart(fig)


    st.divider()
st.subheader("Advanced Analysis")

customer, country, product = st.tabs(
    ["Customer Analysis", "Country Analysis", "Product Analysis"]
)


with customer:
    st.subheader("Customer Analysis")
    customer_count = (data.groupby("Category")["Customer ID"].nunique().reset_index(name="Customer Count")
.sort_values(by="Customer Count", ascending=False))
    st.dataframe(customer_count, use_container_width=True)


with country:
    st.subheader("Country Analysis")
    region_tab1, region_tab2 = st.tabs(["Region Stats", "Country Stats"])
 
    with region_tab1:
        st.markdown("### Regional Performance Summary")
        region_stats = (
            data.groupby("Region").agg(Total_Sales=("Sales", "sum"),Customer_Count=("Customer ID", "nunique"),Product_Count=("Product Name", "nunique"))).reset_index()
        st.dataframe(region_stats, use_container_width=True)


    with region_tab2:
        st.markdown("### Country Performance by Segment, State & City")
        country_stats = (
            data.groupby(["Country", "Segment"]).agg(Total_Sales=("Sales", "sum"),Customer_Count=("Customer ID", "nunique"),State_Count=("State", "nunique"),City_Count=("City", "nunique")).reset_index())
        st.dataframe(country_stats, use_container_width=True)


with product:
    st.subheader("Best Performing Products")
    prod_tab1, prod_tab2, prod_tab3 = st.tabs(["By Region", "By Segment", "By Category"])
    top_n = 10
    with prod_tab1:
        st.markdown("### Top Products by Region")
        region_product = (data.groupby(["Region", "Product Name"]).agg(Total_Sales=("Sales", "sum"),Total_Profit=("Profit", "sum")).reset_index())
        top_region_products = (region_product.sort_values(["Region", "Total_Sales"], ascending=[True, False]).groupby("Region").head(top_n))
        st.dataframe(top_region_products, use_container_width=True)

    with prod_tab2:
        st.markdown("### Top Products by Segment")
        segment_product = (data.groupby(["Segment", "Product Name"]).agg(Total_Sales=("Sales", "sum"),Total_Profit=("Profit", "sum")).reset_index())
        top_segment_products = (segment_product.sort_values(["Segment", "Total_Sales"], ascending=[True, False]).groupby("Segment").head(top_n))
        st.dataframe(top_segment_products, use_container_width=True)

    
    with prod_tab3:
        st.markdown("### Top Products by Category")
        category_product = (data.groupby(["Category", "Product Name"]).agg(Total_Sales=("Sales", "sum"),
                Total_Profit=("Profit", "sum")).reset_index())
        top_category_products = (category_product.sort_values(["Category", "Total_Sales"], ascending=[True, False]).groupby("Category").head(top_n))
        st.dataframe(top_category_products, use_container_width=True)
