
import streamlit as st
import pandas as pd

# Page title
st.set_page_config(page_title="BCS Batch Finder", layout="centered")
st.title("📘 BCS Batch Finder")
st.write("Enter your ID to find your BCS batch (Admin or Ex-Economic).")

# Load Excel data
@st.cache_data
def load_data():
    try:
        return pd.read_excel('_Batch Searcher for Use.xlsx', sheet_name='Batchdata')
    except Exception as e:
        st.error(f"Error loading Excel file: {e}")
        return pd.DataFrame()

df = load_data()

# Input box
user_id = st.text_input("Enter your ID number:")

# Logic to find the batch
def find_batch(user_id):
    try:
        user_id = int(user_id)
    except ValueError:
        return "❌ Please enter a valid number."

    for _, row in df.iterrows():
        if row['BCS Administration Start'] <= user_id <= row['BCS Administration End']:
            return f"✅ {user_id} belongs to **{row['Batch']}** (BCS Administration)"
        
        if pd.notna(row['Ex-Economic Start']) and pd.notna(row['Ex-Economic End']):
            if row['Ex-Economic Start'] <= user_id <= row['Ex-Economic End']:
                return f"✅ {user_id} belongs to **{row['Batch']}** (Ex-Economic)"
    
    return "❌ No matching batch found for this ID."

# Show result
if user_id:
    result = find_batch(user_id)
    st.markdown(result)
