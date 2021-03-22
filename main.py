import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import streamlit as st
from functions_utils import *

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(page_title='Analysis of univariate data - NHANES case study', page_icon="./f.png")
st.title('Analysis of univariate data - NHANES case study')
st.subheader('By [Francisco Tarantuviez](https://www.linkedin.com/in/francisco-tarantuviez-54a2881ab/) -- [Other Projects](https://franciscot.dev/portfolio)')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.write('---')
st.write("""
  The purpose of this app is analyse the data from [NHANES](https://www.cdc.gov/nchs/nhanes/index.htm) survey. It contains a lot of different health statistics such as blood pressure, BMI, etc. and demographic one like gender, education level and so on. 

  Also, this project is a univariate analysis of the data. In this other [TODO](https://google.com) there is a more extensive analysis of the same data, where I mixed and groupped different variables to understand deeply this dataset.
""")

def load_data():
  return pd.read_csv("https://raw.githubusercontent.com/ftarantuviez/Data/main/nhanes_2015_2016.csv")
df = load_data()

nhanes_univariate_analysis(df)

# This app repository

st.write("""
## App repository

[Github](https://github.com/ftarantuviez/)TODO
""")
# / This app repository