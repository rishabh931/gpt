import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="📊 Screener Analyzer", layout="wide")

st.title("📊 Screener.in Company Fundamentals Analyzer")

st.markdown("""
Upload the Excel file you exported from **Screener.in**  
and get instant visualizations of key financials, ratios, and balance sheet trends.
""")

# Upload Excel
uploaded_file = st.file_uploader("Upload Screener.in Excel File", type=["xlsx"])

if uploaded_file:
    # Load all sheets
    try:
        data = pd.ExcelFile(uploaded_file)
        st.success("✅ File uploaded successfully!")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        st.stop()

    # Sidebar - available sheets
    st.sidebar.header("📑 Sheets Available")
    sheets = data.sheet_names
    selected_sheet = st.sidebar.selectbox("Select sheet to view raw data", sheets)
    df_preview = pd.read_excel(data, sheet_name=selected_sheet)
    st.sidebar.dataframe(df_preview.head())

    # ---- Profit & Loss ----
    if "Profit & Loss" in sheets:
        pl = pd.read_excel(data, sheet_name="Profit & Loss")
        st.header("💰 Profit & Loss Overview")

        try:
            year_col = pl.columns[0]
            sales_col = pl.columns[1]
            profit_col = pl.columns[2]

            fig = px.line(pl, x=year_col, y=[sales_col, profit_col],
                          markers=True, title="Sales vs Profit Over Time")
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("⚠️ Could not plot Profit & Loss sheet (check column names).")

    # ---- Balance Sheet ----
    if "Balance Sheet" in sheets:
        bs = pd.read_excel(data, sheet_name="Balance Sheet")
        st.header("📊 Balance Sheet Overview")

        try:
            year_col = bs.columns[0]
            equity_col = bs.columns[1]
            debt_col = bs.columns[2]

            fig2 = px.bar(bs, x=year_col, y=[equity_col, debt_col],
                          barmode="group", title="Equity vs Debt Over Time")
            st.plotly_chart(fig2, use_container_width=True)
        except Exception:
            st.warning("⚠️ Could not plot Balance Sheet sheet (check column names).")

    # ---- Ratios ----
    if "Ratios" in sheets:
        ratios = pd.read_excel(data, sheet_name="Ratios")
        st.header("📈 Key Financial Ratios")

        try:
            year_col = ratios.columns[0]
            roe_col = ratios.columns[1]
            roce_col = ratios.columns[2]
            pe_col = ratios.columns[3]

            fig3 = px.line(ratios, x=year_col,
                           y=[roe_col, roce_col, pe_col],
                           markers=True, title="ROE, ROCE & PE Trend")
            st.plotly_chart(fig3, use_container_width=True)
        except Exception:
            st.warning("⚠️ Could not plot Ratios sheet (check column names).")

    # ---- Cash Flow ----
    if "Cash Flow" in sheets:
        cf = pd.read_excel(data, sheet_name="Cash Flow")
        st.header("💵 Cash Flow Overview")

        try:
            year_col = cf.columns[0]
            op_col = cf.columns[1]
            inv_col = cf.columns[2]
            fin_col = cf.columns[3]

            fig4 = px.bar(cf, x=year_col,
                          y=[op_col, inv_col, fin_col],
                          barmode="group", title="Cash Flow Breakdown")
            st.plotly_chart(fig4, use_container_width=True)
        except Exception:
            st.warning("⚠️ Could not plot Cash Flow sheet (check column names).")

    st.success("✅ Analysis Complete! Explore charts above.")

else:
    st.info("👆 Please upload a Screener.in Excel file to begin.")
