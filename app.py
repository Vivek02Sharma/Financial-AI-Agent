import streamlit as st
import requests
import pandas as pd
import io

st.set_page_config(page_title = "Financial AI Agent", layout = "wide")

api = "http://localhost:8000"

def upload_file_to_backend(file_bytes, filename, file_type):
    files = {"file": (filename, file_bytes, file_type)}
    response = requests.post(f"{api}/upload", files = files, timeout = 600)
    return response.json()

def query_backend(prompt):
    response = requests.post(f"{api}/query", json = {"prompt": prompt}, timeout = 600)
    return response.json()

st.title("Financial AI Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "uploaded_filename" not in st.session_state:
    st.session_state.uploaded_filename = None
if "df_preview" not in st.session_state:
    st.session_state.df_preview = None

st.sidebar.header("Upload your data file")
uploaded_file = st.sidebar.file_uploader("Choose a CSV or Excel file", type = ["csv", "xls", "xlsx"], accept_multiple_files = False)

if uploaded_file and uploaded_file.name != st.session_state.uploaded_filename:
    st.session_state.uploaded_filename = uploaded_file.name
    st.session_state.df_preview = None

if uploaded_file and st.sidebar.button("Process file"):
    file_bytes = uploaded_file.read()  # Read once
    upload_response = upload_file_to_backend(io.BytesIO(file_bytes), uploaded_file.name, uploaded_file.type)

    if upload_response.get("status") == "success":
        st.sidebar.success("File uploaded successfully")
        st.sidebar.write("Columns detected:")
        st.sidebar.json(upload_response.get("columns", []))

        try:
            if uploaded_file.name.lower().endswith(".csv"):
                st.session_state.df_preview = pd.read_csv(io.BytesIO(file_bytes))
            else:
                st.session_state.df_preview = pd.read_excel(io.BytesIO(file_bytes))
        except Exception:
            st.session_state.df_preview = None
            st.sidebar.error("Error reading the uploaded file.")
    else:
        st.sidebar.error(upload_response.get("message", "Unknown error while uploading."))

st.header("Chat with your data")

if st.session_state.df_preview is not None:
    with st.expander("Preview first 5 rows"):
        st.dataframe(st.session_state.df_preview.head())

if uploaded_file is None:
    st.info("Upload a data file first, then start asking questions.")
    st.stop()

for m in st.session_state.chat_history:
    if m["role"] == "user":
        st.chat_message(m["role"]).markdown(m["content"])
    else:
        st.chat_message(m["role"]).json(m["content"])

user_prompt = st.chat_input("Ask a question about your data")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    query_response = query_backend(user_prompt)

    if query_response.get("status") == "success":
        assistant_msg = query_response["result"]
    else:
        assistant_msg = {"error": query_response.get("message", "An error occurred while querying.")}

    st.chat_message("assistant").json(assistant_msg)
    st.session_state.chat_history.append({"role": "assistant", "content": assistant_msg})
