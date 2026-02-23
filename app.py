import streamlit as st
import pandas as pd
import plotly.express as px

# ==============================
# Page Setting
# ==============================
st.set_page_config(page_title="Cybersecurity Dashboard", layout="wide")

st.title("🔐 Cybersecurity Threat Detection Dashboard")
st.markdown("Interactive Dashboard with Filters, Charts and Statistics")

# ==============================
# Upload File
# ==============================
uploaded_file = st.file_uploader("📂 Upload CSV File", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    # ==============================
    # Sidebar Filters
    # ==============================
    st.sidebar.header("🔎 Filter Data")

    categorical_cols = df.select_dtypes(include="object").columns

    filtered_df = df.copy()

    for col in categorical_cols:
        unique_values = df[col].dropna().unique()
        selected_values = st.sidebar.multiselect(
            f"Filter by {col}",
            unique_values,
            default=unique_values
        )
        filtered_df = filtered_df[filtered_df[col].isin(selected_values)]

    # ==============================
    # Statistics Section
    # ==============================
    st.subheader("📊 Summary Statistics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Records", len(filtered_df))
    col2.metric("Total Columns", len(filtered_df.columns))
    col3.metric("Missing Values", filtered_df.isnull().sum().sum())

    # ==============================
    # Show Full Data
    # ==============================
    st.subheader("📄 Full Data Table")
    st.dataframe(filtered_df, use_container_width=True)

    # ==============================
    # Chart Section
    # ==============================
    st.subheader("📈 Data Visualization")

    numeric_cols = filtered_df.select_dtypes(include="number").columns
    categorical_cols = filtered_df.select_dtypes(include="object").columns

    if len(numeric_cols) > 0 and len(categorical_cols) > 0:

        col_x = st.selectbox("Select X-axis (Category)", categorical_cols)
        col_y = st.selectbox("Select Y-axis (Numeric)", numeric_cols)

        chart_type = st.radio(
            "Select Chart Type",
            ["Bar Chart", "Pie Chart", "Line Chart"]
        )

        if chart_type == "Bar Chart":
            grouped = filtered_df.groupby(col_x)[col_y].sum().reset_index()

            fig = px.bar(
                grouped,
                x=col_x,
                y=col_y,
                text_auto=True,
                color=col_y,
                color_continuous_scale="Turbo"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Pie Chart":
            grouped = filtered_df.groupby(col_x)[col_y].sum().reset_index()

            fig = px.pie(
                grouped,
                names=col_x,
                values=col_y,
                hole=0.4
            )
            fig.update_traces(textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Line Chart":
            grouped = filtered_df.groupby(col_x)[col_y].sum().reset_index()

            fig = px.line(
                grouped,
                x=col_x,
                y=col_y,
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Dataset must contain at least one categorical and one numeric column.")

else:
    st.info("Please upload a CSV file to start.")
