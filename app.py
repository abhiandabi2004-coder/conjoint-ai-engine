import streamlit as st
import pandas as pd
from data_processor import process_data
from conjoint_engine import run_conjoint
from ai_insights import generate_insights

st.set_page_config(page_title="Conjoint AI Engine", layout="wide")

st.title("Universal Conjoint Analysis Engine")

# =====================================================
# STEP 1 — DEFINE STRUCTURE
# =====================================================

st.header("Step 1: Define Survey Structure")

num_attributes = st.number_input(
    "How many attributes do you want to analyze?",
    min_value=1,
    max_value=20,
    step=1
)

attribute_names = []

for i in range(int(num_attributes)):
    name = st.text_input(f"Enter name for Attribute {i+1}")
    if name:
        attribute_names.append(name.strip())

response_column = st.text_input("Enter Response Column Name (e.g., Rating or Choice)")

analysis_type = st.selectbox(
    "Select Analysis Type",
    ["Auto Detect", "Rating Based", "Choice Based"]
)

if st.button("Confirm Structure"):

    if len(attribute_names) != num_attributes:
        st.error("Please enter all attribute names.")
    elif not response_column:
        st.error("Please enter response column name.")
    else:
        st.session_state["attributes"] = attribute_names
        st.session_state["target"] = response_column.strip()
        st.session_state["analysis_type"] = analysis_type
        st.success("Structure confirmed. Now upload your dataset.")

# =====================================================
# STEP 2 — UPLOAD FILE
# =====================================================

if "attributes" in st.session_state:

    st.header("Step 2: Upload Survey File")

    uploaded_file = st.file_uploader("Upload Excel or CSV file", type=["xlsx", "csv"])

    if uploaded_file:

        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        # Clean column names
        df.columns = df.columns.str.strip()

        st.subheader("Preview Data")
        st.dataframe(df.head())

        expected_columns = (
            ["Respondent_ID"]
            + st.session_state["attributes"]
            + [st.session_state["target"]]
        )

        # Clean expected columns
        expected_columns = [col.strip() for col in expected_columns]

        if list(df.columns) != expected_columns:
            st.error(f"""
            Column mismatch.
            Expected:
            {expected_columns}
            
            Found:
            {list(df.columns)}
            """)
        else:
            st.success("File format validated successfully.")

            try:
                data = process_data(df, st.session_state["target"])

                results = run_conjoint(
                    data,
                    st.session_state["analysis_type"]
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
                st.error(f"Error during analysis: {e}")
