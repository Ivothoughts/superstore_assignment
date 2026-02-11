import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

st.title("Data visualization App")
st.set_page_config(page_title="Data Viz App", layout="wide")

with st.expander("About this app"):
    data = pd.read_csv('train.csv')
    # data = st.file_uploader("Upload your CSV file", type=["csv"])
    # if data is not None:
    #     data = pd.read_csv(data)

    st.write(data)

left_column, right_column = st.columns(2)

with left_column:
    st.header("Data Header")
    st.dataframe(data)

#EDA - Exploratory Data Analysis

    tab1, tab2, tab3 = st.tabs(["Tab 1", "Tab 2", "Tab 3"])

    with tab1:
        st.subheader("Gender Analysis")
        gender = data['Sex'].value_counts()
        st.dataframe(gender)
        # st.bar_chart(gender)

    with tab2:
        st.subheader("Age Analysis")
        age_tab1, age_tab2 = st.tabs(["Age stats", "Age chart"])
        with age_tab1:
            age = data['Age'].describe()
            st.dataframe(age)
        with age_tab2:
            st.markdown("### Gender with the Highest Age")
            age_gender = data.groupby('Sex')['Age'].max ()
            st.write(age_gender)

    with tab3:
        st.markdown("### Gender by the number of Survived Distribution")
        # data['Survived'] = data['Survived'].map({0: 'Non-Survivied', 1: 'Survived'})
        data["alive_status"] = np.where(data["Survived"]== 1, "Survived", "Non-Survivied")
        survived_gender = pd.pivot_table(data, index='Sex', columns='Survived', values='PassengerId', aggfunc='count')
        st.dataframe(survived_gender)

# -----------------------Second column------------------------------------
with right_column:
    st.header("Data Visualization")

    st.subheader("Passenger Class Distribution")
    pClass = data["Pclass"].value_counts()
    st.bar_chart(pClass)

    tab_rig1, tab_rig2 = st.tabs(["Survival Status", "Age Distribution"])

    with tab_rig1:
        st.subheader("Survival Status Distribution")
        survived = data['Survived'].value_counts()
        # st.pie_chart(survived)
        st.bar_chart(survived)

    with  tab_rig2:
        st.subheader("Age Distribution Histogram")
        age_data = data['Age'].dropna()
        # st.bar_chart(age_data.value_counts(bins=10).sort_index())
        st.plotly_chart(
            px.histogram(age_data, x='Age', nbins=30, title='Age Distribution')
        )