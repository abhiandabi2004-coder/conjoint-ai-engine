import streamlit as st
import pandas as pd
from data_validator import validate_format
from data_processor import process_data
from conjoint_engine import run_conjoint
from ai_insights import generate_insights

st.set_page_config(page_title="Conjoint AI Engine", layout="wide")

st.title("Universal Conjoint Analysis Engine")

# -----------------------------
# TEMPLATE DOWNLOAD
# -----------------------------
st.sidebar.header("Download Template")

try:
    with open("sample_data/Conjoint_Template.xlsx", "rb") as file:
        st.sidebar.download_button(
            label="Download Excel Template",
            data=file,
            file_name="Conjoint_Template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
except:
    st.sidebar.info("Template file not found in sample_data folder.")

# -----------------------------
# FILE UPLOAD
# -----------------------------
st.header("Step 1: Upload Survey File")

uploaded_file = st.file_uploader(
    "Upload Excel or CSV file",
    type=["xlsx", "csv"]
)

if uploaded_file:

    # Read file
    if uploaded_file.name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)

    # Clean column names immediately
    df.columns = df.columns.str.strip()

    st.subheader("Preview Data")
    st.dataframe(df.head())

    # -----------------------------
    # RESPONSE COLUMN SELECTION
    # -----------------------------
    st.header("Step 2: Select Response Column")

    if "Respondent_ID" not in df.columns:
        st.error("Column 'Respondent_ID' is required.")
        st.stop()

    response_column = st.selectbox(
        "Select the Response Column (Rating or Choice)",
        [col for col in df.columns if col != "Respondent_ID"]
    )

    analysis_type = st.selectbox(
        "Select Analysis Type",
        ["Auto Detect", "Rating Based", "Choice Based"]
    )

    if st.button("Run Conjoint Analysis"):

        # -----------------------------
        # VALIDATION
        # -----------------------------
        expected_columns = df.columns.tolist()
        valid, message = validate_format(df, expected_columns)

        if not valid:
            st.error(message)
        else:
            st.success("Validation successful.")

            # -----------------------------
            # PROCESS DATA
            # -----------------------------
            try:
                data = process_data(df, response_column)

                results = run_conjoint(
                    data,
                    analysis_type
                )

                st.header("Results")

                st.subheader("Model Type")
                st.write(results["model_type"])

                st.subheader("Utilities")
                st.dataframe(results["utilities"])

                st.subheader("Attribute Importance (%)")
                st.dataframe(results["importance"])

                st.subheader("AI Recommendation")
                insight = generate_insights(results)
                st.write(insight)

            except Exception as e:
                st.error(f"Error during processing: {e}")
