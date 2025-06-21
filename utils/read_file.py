import pandas as pd
from fastapi import UploadFile

def file_to_dataframe(file: UploadFile) -> pd.DataFrame:
    filename = file.filename.lower()
    if filename.endswith(".csv"):
        return pd.read_csv(file.file)
    elif filename.endswith(".xls"):
        return pd.read_excel(file.file, engine = "xlrd")
    elif filename.endswith(".xlsx"):
        return pd.read_excel(file.file, engine = "openpyxl")
    else:
        raise ValueError("Unsupported file type. Upload CSV or Excel only.")
