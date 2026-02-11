import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("Superstore Performance Analysis and Visalization App")

st. set_page_config(page_title= "Data Analysis Visualsation App", layout="wide")

st.caption("An interactive Streamlit app for analyzing and visualizing the performance of a Superstore sales dataset.")

st.divider()

st.markdown("##### This app is created to analyze and visualize the performance analysis of the superstore"
            "dataset. The dataset contains the sales data of a superstore, including information about the products, customers, and sales transactions. The app provides various visualizations and insights to help understand the trends and patterns in the data.")

with st.expander("Get to know about this app"):
    data = pd.read_excel('superstore.xls')
    st.write(data)

sales_trend = (
    data.groupby("Order Date", as_index=False)["Sales"]
    .sum()
)
fig = px.line(
    sales_trend,
    x= "Order Date",
    y= "Sales",
    # markers=True,
    title="Sales Trend"
)
st.plotly_chart(fig, use_container_width=True)

left_column,right_column = st.columns(2) 

with left_column:
    st.header ("Data Header")
    st.dataframe(data)

    customer, country, product = st.tabs(["Customer Analysis", "Country Analysis", "Product Analysis"])

    with customer:
        st.subheader("Customer Analysis")

        customer_count = (data.groupby("Category")["Customer ID"].nunique().reset_index(name="Customer Count").sort_values(by="Customer Count"))
        
        st.dataframe(customer_count, use_container_width=True)

    with country:
        st.subheader("Country Analysis")
        region_tab1, region_tab2 = st.tabs(["Region stats", "Counry stats "])


        with region_tab1:
            st.markdown("### Regional Performance Summary")

            region_stats = (
            data.groupby("Region")
            .agg(
                Total_Sales=("Sales", "sum"),
                Customer_Count=("Customer ID", "nunique"),
                Product_Count=("Product Name", "nunique")
            )
            .reset_index()
        )

            st.dataframe(region_stats, use_container_width=True)

        with region_tab2:
            st.markdown("### Country Performance by Segment, State & City")

            country_stats = (
            data.groupby(["Country", "Segment"])
            .agg(
                Total_Sales=("Sales", "sum"),
                Customer_Count=("Customer ID", "nunique"),
                State_Count=("State", "nunique"),
                City_Count=("City", "nunique")
            )
            .reset_index()
        )

            st.dataframe(country_stats, use_container_width=True)




