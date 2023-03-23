import streamlit as st
import pandas as pd
import xlwings as xw
import tkinter as tk
from tkinter import filedialog
import pythoncom
import win32com
import re
from typing import Any,Dict
# from explorer_df import dataframe_explorer
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
    try:
        sheet_names = wb.sheet_names
        lst_sheets =[]
        lst_tables = []
        lst_range_header = []
        lst_row_data = []
        lst_range_data = []
        for i in range(1,len(sheet_names)):
            table_names = wb.sheets[sheet_names[i]].tables
            if len(table_names) > 0:
                for j in table_names:
                    range_header = re.sub('[$]','', wb.sheets[sheet_names[i]].tables[j.name].header_row_range.address)
                    range_data = wb.sheets[sheet_names[i]].range(j.name).address
                    row_data = re.sub('[$]|[A-Z]','',range_data)
                    lst_sheets.append(sheet_names[i])
                    lst_tables.append(j.name)
                    lst_range_header.append(range_header)
                    lst_range_data.append(range_data)
                    lst_row_data.append(row_data)
            else:
                lst_sheets.append(sheet_names[i])
                lst_tables.append('')
                lst_range_header.append('')
                lst_range_data.append('')
                lst_row_data.append('')
                
        dict_df = {
            'Sheet Name': lst_sheets,
            'Table Name': lst_tables,
            'Range Headers':lst_range_header,
            'RAnge Data': lst_range_data,
            'Row Data': lst_row_data
        }
        df = pd.DataFrame(dict_df)
        df['Have Table'] = df['Table Name'].map(lambda x: False if x == 'No Table' else True)
        
        wb.close()
        app.kill()
        del app
    except pythoncom.com_error as error:
        wb.close()
        app.kill()
        del app
    return df


st.header("Phân tích file Excel & Xuất Report")
col1, col2 = st.columns(2)


# Đặt button File Picker vào cột trái
with col1:
    input_path = st.text_input('Nhập File Path')

# Đặt button Folder Picker vào cột phải
with col2:
    output_path = st.text_input('Nhập Output Path')
data = get_detail_workbook(input_path)
# if input_path is not None:
# df = get_detail_workbook(input_path)
random_base = pd.util.hash_pandas_object(data)
with st.sidebar:
    st.header("Chọn sheet và table")
    to_filter_columns = st.multiselect(
                "Filter dataframe on",
                data.columns,
                key=f"{random_base}_multiselect",
            )
    filters: Dict[str, Any] = dict()
    left, right = st.columns((3, 20))
    for col in to_filter_columns:
        left.write(4)
        lst = data[col].unique()
        filters[col] = right.multiselect(
                        f"Chọn {col}",
                        data[col].unique(),
                        default=lst[0],
                        key=f"{random_base}_{col}",
                        max_selections=1
                    )
        data = data[data[col].isin(filters[col])]
    
st.table(data)
        


