import streamlit as st
import pandas as pd
import xlwings as xw
import tkinter as tk
from tkinter import filedialog
import pythoncom
import win32com
from typing import Any,Dict
from explorer_df import dataframe_explorer
xl=win32com.client.Dispatch("Excel.Application",pythoncom.CoInitialize())


def button_callbacks():
    st.session_state.button_clicked = True


def browse_file():
        # Hiển thị hộp thoại lựa chọn tệp và lấy đường dẫn của tệp
    root = tk.Tk()
    root.withdraw()

    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    # Folder picker button
    st.write('Please select a file:')
    clicked2 = st.button('Folder Picker',key ='button2')
    if clicked2:
        folder_path = filedialog.askopenfilename(master=root)
        dirname = st.text_input('Selected folder:', folder_path,key='h2')
    return dirname

def out_put_path():
    # Set up tkinter
    root = tk.Tk()
    root.withdraw()

    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    # Folder picker button
    st.write('Please select a file:')
    clicked2 = st.button('Folder Picker',key ='button2')
    if clicked2:
        folder_path = filedialog.askdirectory(master=root)
        dirname = st.text_input('Selected folder:', folder_path,key='h2')
    return dirname
    
    
def get_detail_workbook(input_path):
    app = xw.App(visible=False)
    wb = xw.Book(input_path)
    sheet_names = wb.sheet_names

    lst_sheets =[]
    lst_tables = []
    for i in sheet_names:
        table_names = wb.sheets[i].tables
        for j in table_names:
            lst_sheets.append(i)
            lst_tables.append(j.name)
            
    dict_df = {
        'Sheet': lst_sheets,
        'Table': lst_tables
    }
    df = pd.DataFrame(dict_df)
    wb.close()
    app.kill()
    del app
    return df

col1, col2 = st.columns(2)

# Đặt button File Picker vào cột trái
with col1:
    input_path = st.text_input('Nhập File Path')

# Đặt button Folder Picker vào cột phải
with col2:
    output_path = st.text_input('Nhập Output Path')

# if input_path is not None:
df = get_detail_workbook(input_path)
random_base = pd.util.hash_pandas_object(df)
with st.sidebar:
    st.header("Chọn sheet và table")
    to_filter_columns = st.multiselect(
                "Filter dataframe on",
                df.columns,
                key=f"{random_base}_multiselect",
            )
    filters: Dict[str, Any] = dict()
    left, right = st.columns((3, 20))
    for col in to_filter_columns:
        left.write(4)
        lst = df[col].unique()
        filters[col] = right.multiselect(
                        f"Values for {col}",
                        df[col].unique(),
                        default=lst[0],
                        key=f"{random_base}_{col}",
                        max_selections=1
                    )
        df = df[df[col].isin(filters[col])]
        


