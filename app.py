import streamlit as st
import pandas as pd

FILE_PATH = "dermatology_questions.xlsx"

# Load data
df = pd.read_excel(FILE_PATH)

st.title("🧴 Dermatology Q&A Entry Form")

# Select category first
category = st.selectbox("Select Category:", df["Category"].unique())
filtered_df = df[df["Category"] == category]

# Select question
question = st.selectbox("Select Question:", filtered_df["Question"].tolist())
row_index = df[df["Question"] == question].index[0]

# Input answer
answer = st.text_area("Your Answer", value=df.loc[row_index, "Answer"] if "Answer" in df.columns else "")

# Save button
if st.button("💾 Save Answer"):
    # If 'Answer' column does not exist, create it
    if "Answer" not in df.columns:
        df["Answer"] = ""
    df.loc[row_index, "Answer"] = answer
    df.to_excel(FILE_PATH, index=False)
    st.success("✅ Answer saved successfully!")
