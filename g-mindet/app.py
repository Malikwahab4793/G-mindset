import pandas as pd
import streamlit as st
import os
from io import BytesIO

st.set_page_config(page_title="📊 Class Assignment 1", layout='wide')

# Custom CSS for background and styling
st.markdown(
    """
    <style>
    body {
        background-color: #1e1e2f;
        color: white;
    }
    .main {
        background-color: #2e2e3e;
        padding: 20px;
        border-radius: 10px;
    }
    .stApp {
        background-color: #1e1e2f;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #ffcc00;
        text-align: center;
    }
    .footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        text-align: center;
        padding: 10px;
        background-color: #2e2e3e;
        color: #ccc;
        font-size: 14px;
    }
    .highlight {
        font-size: 18px;
        color: #00ffff;
        font-weight: 500;
        text-align: center;
        margin-top: 10px;
    }
    .custom-label {
        color: #00ffff !important;
        font-weight: bold;
    }
    .chat-box {
        margin-top: 30px;
        padding: 15px;
        background-color: #2e2e3e;
        border-radius: 10px;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Description
st.markdown("<div class='title'>📚 Student Marks Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='highlight'>✨ Transform your file between CSV and Excel formats with built-in data cleaning and visualization!</div>", unsafe_allow_html=True)

# File Uploader
st.markdown("<span class='custom-label'>📤 Upload your files (accepts CSV or Excel):</span>", unsafe_allow_html=True)
uploaded_files = st.file_uploader(" ", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.write(f"📄 **Preview of {file.name} Dataframe:**")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🧹 Data Cleaning Options")

        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates removed!")

            with col2:
                if st.button(f"🧼 Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values have been filled!")

        # Column selection
        st.subheader("🧩 Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Bar Chart for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # Conversion Options
        st.subheader("🔄 Conversion Option")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        if st.button(f"💾 Convert {file.name}"):
            buffer = BytesIO()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='xlsxwriter')
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

    st.success("🎉 All files processed successfully!")

# Gemini-style chatbot UI (frontend placeholder)
st.markdown("""
    <div class='chat-box'>
        <h4>🤖 Gemini Assistant</h4>
        <p><em>This is a placeholder for Gemini-style chat interface. Integrate Gemini API for actual functionality.</em></p>
        <input type='text' placeholder='Ask me anything about your data...' style='width: 100%; padding: 8px; border-radius: 5px; border: none; margin-top: 10px;'>
    </div>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
    <div class='footer'>
        🚀 Created by <strong>Malik Wahab</strong> ❤️
    </div>
""", unsafe_allow_html=True)
