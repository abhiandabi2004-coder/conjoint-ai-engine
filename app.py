import streamlit as st
import pandas as pd
from data_validator import validate_format
from data_processor import process_data
from conjoint_engine import run_conjoint
from ai_insights import generate_insights

st.set_page_config(page_title="Universal Conjoint Engine", layout="wide")

st.title("Universal Conjoint Analysis Engine")

# -------------------------------
# STEP 1 — DEFINE STRUCTURE
# -------------------------------

st.header("Step 1: Define Survey Structure")

num_attributes = st.number_input(
    "Number of Attributes",
    min_value=1,
    max_value=20,
    step=1
)

attribute_names = []

for i in range(int(num_attributes)):
    name = st.text_input(f"Name of Attribute {i+1}")
    if name:
        attribute_names.append(name)

target_column = st.text_input("Response Column Name (Rating / Choice)")

analysis_type = st.selectbox(
    "Analysis Type",
    ["Auto Detect", "Rating Based", "Choice Based"]
)

if st.button("Confirm Structure"):
    if len(attribute_names) == num_attributes and target_column:
        st.session_state["attributes"] = attribute_names
        st.session_state["target"] = target_column
        st.session_state["analysis_type"] = analysis_type
        st.success("Structure saved. Upload file below.")
    else:
        st.error("Complete all fields before confirming.")


# -------------------------------
# STEP 2 — FILE UPLOAD
# -------------------------------

if "attributes" in st.session_state:

    st.header("Step 2: Upload Survey File")

    uploaded_file = st.file_uploader("Upload Excel or CSV", type=["xlsx", "csv"])

    if uploaded_file:

        if uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        st.write("Preview Data", df.head())

        expected_columns = (
            ["Respondent_ID"]
            + st.session_state["attributes"]
            + [st.session_state["target"]]
        )

        valid, message = validate_format(df, expected_columns)

        if not valid:
            st.error(message)
        else:
            st.success("File format validated.")

            data = process_data(
                df,
                st.session_state["target"]
            )

            results = run_conjoint(
                data,
                st.session_state["analysis_type"]
            )

            st.subheader("Model Type")
            st.write(results["model_type"])

            st.subheader("Utilities")
            st.write(results["utilities"])

            st.subheader("Attribute Importance (%)")
            st.write(results["importance"])

            insight = generate_insights(results)
            st.subheader("AI Recommendation")
            st.write(insight)