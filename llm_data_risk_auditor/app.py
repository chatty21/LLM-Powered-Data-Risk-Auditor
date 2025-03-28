import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from modules.data_profile import generate_profile_summary
from modules.llm_analyzer import analyze_risks_with_llm

st.set_page_config(page_title="LLM Data Risk Auditor", layout="wide")

hour = datetime.now().hour
is_dark_mode = hour < 6 or hour > 18
panel_bg = "rgba(0, 0, 0, 0.7)"
panel_text = "#f2f2f2"
title_glow = "#39ff14"

st.markdown(f"""
    <style>
        .stApp {{
            background-image: url('https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=1920&q=80');
            background-size: cover;
            background-position: center;
            animation: backgroundFade 20s infinite alternate ease-in-out;
        }}
        .main-title {{
            font-size: 2.5em;
            font-weight: bold;
            color: {panel_text};
            background: {panel_bg};
            padding: 1.2rem;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 10px;
            animation: slideInDown 1s ease-in-out;
            text-shadow: 0 0 8px {title_glow}, 0 0 15px {title_glow};
        }}
        .section-title {{
            font-size: 1.3em;
            color: {panel_text};
            margin-top: 30px;
            border-bottom: 2px solid {title_glow};
            padding-bottom: 4px;
            animation: fadeIn 1.2s ease-in-out;
        }}
        .block-container {{
            background: {panel_bg};
            backdrop-filter: blur(10px);
            border-radius: 14px;
            padding: 1.5rem;
            color: {panel_text};
            font-size: 0.96em;
            animation: fadeIn 1s ease-in-out;
        }}
        .stButton>button {{
            background-color: {title_glow};
            color: black;
            font-weight: bold;
            font-size: 0.9em;
            border-radius: 12px;
            padding: 0.5em 1.1em;
            transition: transform 0.3s ease, background-color 0.3s ease;
            animation: fadeInUp 1s ease-in-out;
        }}
        .stButton>button:hover {{
            transform: scale(1.05);
            background-color: #00cc88;
        }}
        .stMarkdown, .stText, .stDataFrame {{
            color: {panel_text};
            font-size: 0.94em;
        }}
        @keyframes fadeInUp {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes slideInDown {{
            from {{ opacity: 0; transform: translateY(-50px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        @keyframes backgroundFade {{
            from {{ filter: brightness(0.7); }}
            to {{ filter: brightness(1); }}
        }}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧠 LLaMA 2-Powered Data Risk Auditor</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("📂 Upload CSV or JSON file", type=["csv", "json"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_json(uploaded_file)
        st.success("✅ File uploaded successfully!")

        st.markdown('<div class="section-title">📄 Dataset Preview</div>', unsafe_allow_html=True)
        st.dataframe(df.head())

        st.markdown('<div class="section-title">📈 Dataset Summary</div>', unsafe_allow_html=True)
        summary_text = generate_profile_summary(df)
        st.markdown(summary_text)
        st.download_button("📥 Download Summary", summary_text, "dataset_summary.md", "text/markdown")

        st.markdown('<div class="section-title">📉 Missing Values by Column</div>', unsafe_allow_html=True)
        missing_counts = df.isnull().sum()
        missing_counts = missing_counts[missing_counts > 0]
        if not missing_counts.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            missing_counts.plot(kind='bar', ax=ax, color=title_glow)
            ax.set_ylabel("Missing Values")
            st.pyplot(fig)
        else:
            st.info("✅ No missing values detected.")

        if 'IsReturned' in df.columns:
            st.markdown('<div class="section-title">⚖️ Class Imbalance: IsReturned</div>', unsafe_allow_html=True)
            class_counts = df['IsReturned'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(6, 4))
            class_counts.plot(kind='bar', ax=ax2, color=['#00bfff', '#ff4c4c'])
            ax2.set_ylabel("Count")
            ax2.set_title("Return Status Distribution")
            st.pyplot(fig2)

        st.markdown('<div class="section-title">🧯 Missing Data Heatmap</div>', unsafe_allow_html=True)
        if df.isnull().sum().sum() > 0:
            fig3, ax3 = plt.subplots(figsize=(10, 4))
            sns.heatmap(df.head(500).isnull(), cbar=False, ax=ax3, cmap="coolwarm")
            st.pyplot(fig3)
        else:
            st.info("✅ No missing data to display.")

        st.markdown('<div class="section-title">🧬 High Cardinality Columns</div>', unsafe_allow_html=True)
        high_card_cols = df.nunique().sort_values(ascending=False)
        high_card_cols = high_card_cols[high_card_cols > 1000]
        if not high_card_cols.empty:
            fig4, ax4 = plt.subplots(figsize=(8, 4))
            high_card_cols.head(5).plot(kind='bar', ax=ax4, color='#ffcc00')
            ax4.set_ylabel("Unique Values")
            st.pyplot(fig4)

        st.markdown('<div class="section-title">📊 Numeric Column Distributions</div>', unsafe_allow_html=True)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if numeric_cols:
            selected_col = st.selectbox("Choose a column to visualize", numeric_cols)
            fig5, ax5 = plt.subplots(figsize=(8, 4))
            sns.histplot(df[selected_col], bins=50, kde=True, ax=ax5, color=title_glow)
            ax5.set_title(f"Distribution of {selected_col}")
            st.pyplot(fig5)

        st.markdown('<div class="section-title">🧠 Correlation Heatmap</div>', unsafe_allow_html=True)
        if len(numeric_cols) >= 2:
            top_corr = df[numeric_cols].corr().abs().unstack().sort_values(ascending=False)
            top_features = list(set([i[0] for i in top_corr[:50].index] + [i[1] for i in top_corr[:50].index]))
            corr = df[top_features].corr()
            fig6, ax6 = plt.subplots(figsize=(12, 6))
            sns.heatmap(corr, annot=False, cmap="viridis", ax=ax6)
            plt.xticks(rotation=90)
            plt.yticks(rotation=0)
            st.pyplot(fig6)

        st.markdown('<div class="section-title">🤖 Analyze with LLaMA 2</div>', unsafe_allow_html=True)
        if st.button("🧠 Run Local LLM Analysis"):
            with st.spinner("Analyzing dataset locally using LLaMA 2..."):
                try:
                    result = analyze_risks_with_llm(summary_text)
                    st.subheader("📋 LLaMA 2 Risk Analysis")
                    st.markdown(result)
                    st.download_button("📥 Download Risk Report", result, "llm_risk_analysis.md", "text/markdown")
                except Exception as e:
                    st.error(f"❌ LLaMA Error: {str(e)}")

    except Exception as e:
        st.error(f"❌ Error reading the file: {e}")
else:
    st.markdown(
        "<p style='color:#fff; background-color:rgba(0,0,0,0.5); padding:0.75rem; border-radius:8px; "
        "font-size:1.05rem; text-align:center; font-weight:600; box-shadow: 0 0 10px #39ff14;'>"
        "📌 Please upload a <strong>CSV</strong> or <strong>JSON</strong> file to begin.</p>",
        unsafe_allow_html=True
    )
