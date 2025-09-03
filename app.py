import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Screener Analyzer", layout="wide")

st.title("📊 Dynamic Screener.in Fundamentals Analyzer")

st.markdown("""
Upload your **Screener.in Excel export** and interactively explore financial data.  
You can select any metric from Profit & Loss, Balance Sheet, or Cash Flow and see its trend.
""")

# Upload Excel
uploaded_file = st.file_uploader("Upload Screener.in Excel File", type=["xlsx"])

def clean_sheet(xls, sheet_name):
    """Reads Screener.in sheet and reshapes for plotting"""
    try:
        df = pd.read_excel(xls, sheet_name=sheet_name, header=2)
        df = df.dropna(how="all")  # drop empty rows
        df = df.loc[:, ~df.columns.duplicated()]  # remove duplicate cols
        df = df.set_index(df.columns[0])  # Narration as index
        df = df.T  # transpose -> Years as rows
        df.index.name = "Year"
        df = df.apply(pd.to_numeric, errors="coerce")
        return df
    except Exception as e:
        st.warning(f"⚠️ Could not process {sheet_name}: {e}")
        return None

if uploaded_file:
    xls = pd.ExcelFile(uploaded_file)
    st.success("✅ File uploaded successfully!")

    available_sheets = [s for s in ["Profit & Loss", "Balance Sheet", "Cash Flow", "Quarters"] if s in xls.sheet_names]
    selected_sheet = st.sidebar.radio("📑 Select a sheet", available_sheets)

    df = clean_sheet(xls, selected_sheet)

    if df is not None:
        # Sidebar metric selector
        metrics = df.columns.tolist()
        selected_metrics = st.sidebar.multiselect("📊 Select metrics to plot", metrics, default=metrics[:2])

        st.subheader(f"📈 {selected_sheet} Trends")

        if selected_metrics:
            fig = px.line(df, x=df.index, y=selected_metrics, markers=True,
                          title=f"{selected_sheet} - Selected Metrics")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("👆 Please select at least one metric to plot.")

        # Show raw table
        with st.expander("🔍 Show raw cleaned data"):
            st.dataframe(df)
else:
    st.info("👆 Please upload a Screener.in Excel file to begin.")

