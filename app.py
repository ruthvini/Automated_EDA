import streamlit as st
import pandas as pd
import os
from ydata_profiling import ProfileReport
from streamlit.components.v1 import html

# Page config
st.set_page_config(page_title="EDA Engine", layout="wide")

st.title("📊 EDA Engine")
st.markdown("Upload a CSV or Excel file to generate an automatic EDA report.")

# Upload file
uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # Read file into DataFrame
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format!")
            st.stop()

        st.subheader("🔹 Data Preview")
        st.dataframe(df.head())

        st.subheader("📈 Generating EDA Report...")
        profile = ProfileReport(df, title="EDA Report", explorative=True)

        # Save report to temp file
        output_path = "eda_output.html"
        profile.to_file(output_path)

        # Show inside Streamlit
        with open(output_path, "r", encoding='utf-8') as f:
            html(f.read(), height=1000, scrolling=True)

        # Download option
        with open(output_path, "rb") as f:
            st.download_button(
                label="📥 Download EDA Report",
                data=f,
                file_name="eda_report.html",
                mime="text/html"
            )

    except Exception as e:
        st.error(f"⚠️ Error while processing file: {e}")
