import streamlit as st
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime

Page_Default = 3

df = pd.read_csv("https://raw.githubusercontent.com/hoanghce/Contest/main/Test.csv")
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

today = datetime.today().date()
year = today.year
month = today.month
day = today.day


# Design cho page
st.set_page_config(
    page_title="Distribution Reporting Contest",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Tạo menu
selected = option_menu(
    menu_title=None,  # required
    options=["Dashboard","Details","Input",],  # required
    icons=["bar-chart-line",'table',"input-cursor-text"],  # optional
    menu_icon="cast",  # optional
    default_index=0,  # optional
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"},
        "nav-link": {
            "font-size": "25px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "green"},
    },
)
    




if selected == "Dashboard":
    # st.markdown(f"<h2 style='text-align: center; color: black;'>Cập nhật tình hình contest ngày {datetime.today().date()} </h2>", unsafe_allow_html=True)
    st.title(f'Contest {datetime.today().date()}')
    st.text(" ")
    with st.sidebar:
        Maker_Filter = st.multiselect(
            label = "Maker",
            options=  df['Maker'].unique(),
            default=df['Maker'].unique()
        )
        df_Maker_Filter = df.query('Maker == @Maker_Filter')
        
        Contest_Filter = st.multiselect(
            label = "Contest",
            options=  df_Maker_Filter['Contest'].unique(),
            default=df.query('Maker == @Maker_Filter')['Contest'].unique()
        )
    df1 = df.query('(Contest  == @Contest_Filter) & (Maker == @Maker_Filter)')
    

    col1, col2, col3 = st.columns(3)
    with col1:
        Finish = len(df1.query("Status == 'Complete'"))
        st.image('https://github.com/hoanghce/Contest/blob/main/Icon/Finish.png?raw=true',width=50)
        st.metric("Finish",Finish,1)

    with col2:
        UnComplete = len(df1.query("Status == 'Note Complete'"))
        st.image('https://github.com/hoanghce/Contest/blob/main/Icon/Warning.png?raw=true',width=50)
        st.metric("Unfinished",UnComplete,1)
    
    with col3:
        Running = len(df1.query("Status == 'Running'"))
        st.image('https://github.com/hoanghce/Contest/blob/main/Icon/Running.png?raw=true',width=50)
        st.metric("Running",Running,1)
        
    st.markdown("""
        <style>
            .stContainer {
                display: flex;
                justify-content: center;
            }
        </style>
        """, unsafe_allow_html=True)

    
if selected == "Details":
    st.title(f"Thông tin chi tiết về Contest")
    with st.sidebar:
        Maker_Filter = st.multiselect(
            label = "Maker",
            options=  df['Maker'].unique(),
            default=df['Maker'].unique()
        )
        df_Maker_Filter = df.query('Maker == @Maker_Filter')
        
        Contest_Filter = st.multiselect(
            label = "Contest",
            options=  df_Maker_Filter['Contest'].unique(),
            default=df.query('Maker == @Maker_Filter')['Contest'].unique()
        )
        
        
    df1 = df.query('(Contest  == @Contest_Filter) & (Maker == @Maker_Filter)')
    st.table(df1)
    st.download_button(label='📥 Download File CSV',
                                data=convert_df(df1) ,
                                file_name= f'Check_Contest_{year}_0{month}_{day}.csv')
    
if selected == "Input":
    st.title(f"You have selected {selected}")
# col3.metric("Humidity", "86%", "4%")
