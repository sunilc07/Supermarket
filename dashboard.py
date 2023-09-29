import streamlit as st
import pandas as pd 
import numpy as np 
import plotly.express as px
import base64

#titles
st.title("Supermarket Grocery sales")
st.sidebar.title('Slicers')

#filelocation
DATA_URL= 'Supermart Grocery Sales - Retail Analytics Dataset.xlsx'

df = pd.read_excel(DATA_URL)

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover

    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('Background.jpg')

city = df['City'].unique()

selected_states = st.sidebar.selectbox('Select City',options = city,key =1)

city_df = df[(df['City'] == selected_states)]

#CategoryWiseSales
city_sales = (city_df.groupby(['Category'], group_keys=True, axis=0, as_index=True)['Sales']
    .sum()
    .reset_index()
    .rename(columns={"Category":"Category","Sales": "Sales"})
    )


city_df['year'] = pd.DatetimeIndex(city_df['Order Date']).year
city_df['month'] = pd.DatetimeIndex(city_df['Order Date']).month_name()


year_sales_df = (city_df.groupby(['year','month'], group_keys=True, axis=0, as_index=True)['Sales']
    .sum()
    .reset_index()
    .rename(columns={"year":"Year","month": "Month","Sales":"Sales"})
    )

#visualization
select= st.sidebar.selectbox('Sales by Category Visualization',['Bar Graph','Pi Chart'])


st.markdown('### Sales by Category')
if select=='Bar Graph':
	fig=px.bar(city_sales, x='Category',y='Sales',color='Sales',height=500)
	st.plotly_chart(fig)

else:
	fig=px.pie(city_sales, values='Sales', names='Category')
	st.plotly_chart(fig)

st.markdown('### Details')
st.dataframe(city_df)

st.markdown('### Monthly Sales at Every Month')
fig2 = px.area(year_sales_df, x='Month', y='Sales',color='Year', line_group='Year')
fig2.update_xaxes(categoryorder='array', categoryarray= ['January','February','March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
st.plotly_chart(fig2)

