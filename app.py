
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(
    page_title="AI Business Data Analyst",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Powered Business Data Analyst")
st.caption("Analyze business datasets, generate insights and make data-driven decisions.")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["Dashboard", "Data Explorer", "Data Quality", "SQL Query", "AI Assistant", "Business Insights"]
)

# Dataset Upload
st.sidebar.subheader("Upload Dataset")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV or Excel",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.session_state["df"] = df

elif "df" not in st.session_state:
    st.info("👈 Upload a CSV or Excel dataset to get started.")
    st.stop()

df = st.session_state["df"]

# Dashboard
if page == "Dashboard":

    st.subheader("Business Analytics Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Records", f"{len(df):,}")
    col2.metric("Total Columns", len(df.columns))
    col3.metric("Missing Values", int(df.isnull().sum().sum()))
    col4.metric("Duplicate Rows", int(df.duplicated().sum()))

    st.subheader("Dataset Preview")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Column Data Types")
    st.dataframe(
        pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str).values,
            "Missing Values": df.isnull().sum().values
        }),
        use_container_width=True
    )

# Data Explorer
elif page == "Data Explorer":

    st.subheader("Explore Your Dataset")

    st.dataframe(df, use_container_width=True)

    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include="all").T, use_container_width=True)

# Data Quality
elif page == "Data Quality":

    st.subheader("Data Quality Analysis")

    st.write("Missing Values")
    missing = df.isnull().sum().reset_index()
    missing.columns = ["Column", "Missing Count"]
    missing = missing[missing["Missing Count"] > 0]

    if missing.empty:
        st.success("No missing values found!")
    else:
        st.dataframe(missing, use_container_width=True)

    st.write("Duplicate Records")

    duplicates = int(df.duplicated().sum())

    if duplicates == 0:
        st.success("No duplicate records found!")
    else:
        st.warning(f"{duplicates} duplicate records detected.")

    if st.button("Remove Duplicate Rows"):
        df = df.drop_duplicates()
        st.session_state["df"] = df
        st.success("Duplicate rows removed!")

# Business Insights
elif page == "Business Insights":

    st.subheader("Business Data Overview")

    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()

    if numeric_columns:

        selected_column = st.selectbox(
            "Select a metric",
            numeric_columns
        )

        fig = px.histogram(
            df,
            x=selected_column,
            title=f"Distribution of {selected_column}"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.metric(
            f"Average {selected_column}",
            round(df[selected_column].mean(), 2)
        )

        st.metric(
            f"Maximum {selected_column}",
            round(df[selected_column].max(), 2)
        )

    else:
        st.warning("No numerical columns available for analysis.")

elif page == "AI Assistant":

    from ai_assistant import get_ai_response

    st.subheader("🤖 AI Business Data Assistant")

    question = st.text_area(
        "Ask questions about your dataset",
        placeholder="Which product generates the highest revenue?"
    )

    if st.button("Generate Insights"):

        if question.strip():

            with st.spinner("Analyzing your dataset..."):

                answer = get_ai_response(question, df)

            st.markdown("### AI Analysis")
            st.write(answer)

        else:
            st.warning("Please enter a question.")        

# SQL Query Module

elif page == "SQL Query":

    from sql_engine import execute_query

    st.subheader("SQL Query Explorer")

    st.write("Table name: `business_data`")

    query = st.text_area(
        "Write your SQL query",
        value="SELECT * FROM business_data LIMIT 10;",
        height=150
    )

    if st.button("Execute Query"):

        result, error = execute_query(df, query)

        if error:
            st.error(error)

        else:
            st.success("Query executed successfully!")
            st.dataframe(result, use_container_width=True)
            st.write(f"Rows returned: {len(result)}")
