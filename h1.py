import streamlit as st
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

today = datetime.today().date()
year = today.year
month = today.month
day = today.day

df = pd.read_excel('H1.xlsx')

# Design cho page
st.set_page_config(
    page_title="Distribution Reporting Splitfile",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tạo menu
# selected = option_menu(
#     menu_title=None,  # required
#     options=["Dashboard","View File","Transform to Database",],  # required
#     icons=["bar-chart-line",'table',"input-cursor-text"],  # optional
#     menu_icon="cast",  # optional
#     default_index=0,  # optional
#     orientation="horizontal",
#     styles={
#         "container": {"padding": "0!important", "background-color": "#fafafa"},
#         "icon": {"color": "orange", "font-size": "25px"},
#         "nav-link": {
#             "font-size": "25px",
#             "text-align": "left",
#             "margin": "0px",
#             "--hover-color": "#eee",
#         },
#         "nav-link-selected": {"background-color": "green"},
#     },
# )



# if selected == 'Table':
st.header("Test Sales Data")

_funct = st.sidebar.radio(label = 'Functions',options=['Display','Highlight'])
if _funct == 'Highlight':
    gd = GridOptionsBuilder.from_dataframe(df)
    gd.autoSizeColumns(True)    
    gd.configure_pagination(enabled=True)
    gd.configure_default_column(editable=True,groupable=True)
    sel_mode = st.radio('Selection Type', options=['Single','multiple'])

    gd.configure_selection(selection_mode=sel_mode, use_checkbox=True)
    gridoptions = gd.build()
    gridoptions.auto_size_columns = True
    grid_table = AgGrid(df,gridOptions=gridoptions, update_mode=GridUpdateMode.SELECTION_CHANGED, height=500,allow_unsafe_jscode=True,Theme = 'fresh')

    sel_row = grid_table["selected_rows"]
    st.write(sel_row)
    