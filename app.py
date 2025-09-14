import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe, get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
import json


# --- Google Sheets setup ---
SHEET_NAME = "Dermatology_QA"
JSON_KEY_FILE = "service_account.json"  # Upload this JSON to your repo or Streamlit secrets

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
creds_dict = json.loads(st.secrets["google_creds"]["json"])
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

sheet = client.open(SHEET_NAME).sheet1
df = get_as_dataframe(sheet).fillna("")  # Load sheet as DataFrame

# --- Streamlit UI ---
st.title("🧴 Dermatology Q&A Entry Form")

category = st.selectbox("Select Category:", df["Category"].unique())
filtered_df = df[df["Category"] == category]

question = st.selectbox("Select Question:", filtered_df["Question"].tolist())
row_index = df[df["Question"] == question].index[0]

answer = st.text_area("Your Answer", value=df.loc[row_index, "Answer"])

if st.button("💾 Save Answer"):
    df.loc[row_index, "Answer"] = answer
    set_with_dataframe(sheet, df)  # Save back to Google Sheet
    st.success("✅ Answer saved successfully!")
