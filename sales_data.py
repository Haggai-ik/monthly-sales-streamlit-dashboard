import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objs 
import pickle
from pathlib import Path
import streamlit_authenticator as str
import yaml
from yaml.loader import SafeLoader

st.set_page_config(page_title='MONTHLY SALES DASHBOARD',
                   layout="wide")



with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = str.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)


name,authentication_status,username=authenticator.login("Login","main")
 
if authentication_status==False:
    st.error("incorrect username and password")

if authentication_status==None:
    st.warning("please enter your username")

if authentication_status==True:
        df=pd.read_csv('sales_january_2019.csv')
        #st.dataframe(df)
        authenticator.logout("Logout","sidebar")
        dff=df['Quantity Ordered'].str.contains('Quantity Ordered')==False
        df=df.loc[dff]
        df['Quantity Ordered']=df['Quantity Ordered'].astype(int)
        df['Price Each']=df['Price Each'].astype(float)
        df['total amount']=df['Quantity Ordered']*df['Price Each']
        df['Order Date']=pd.to_datetime(df['Order Date'])
        month=df['Order Date'].dt.month
        year=df['Order Date'].dt.year
        day=df['Order Date'].dt.day
        day_name=df['Order Date'].dt.day_name
        hour=df['Order Date'].dt.hour
        df['month']=month
        df['year']=year
        df['day']=day
        df['day_name']=day_name()
        df['hour']=hour
        def long(hour):
           if hour ==0:
               x='Midnight'
           elif hour>0 and hour<12:
               x='Morning'
           elif hour==12:
               x='Noon'
           elif hour>12 and hour<16:
               x='Afternoon'
           elif hour>=16 and hour<21:
               x='Evening'
           elif hour>=21 and hour<24:
               x='Night'
           return x
        df['Hour']=df['hour'].apply(lambda x:long(x))
        df['trial']=df['Purchase Address'].str.extract(r'(,\s[a-zA-Z]+.+,)')
        df['City']=df['trial'].str.extract(r'([a-zA-Z]+.[a-zA-Z]+)')
        df.drop(columns=['Order Date','Purchase Address','trial'],inplace=True)
        df.rename(columns={'Quantity Ordered':'Quantity_Ordered','Price Each':'Price_Each','total amount':'total_amount'},
            inplace=True)
      ##st.dataframe(df)
    
        #authenticator.logout("logout","main")
        st.sidebar.title(f" Welcome {username}")
        st.sidebar.header('Please select field : ')

        products=st.sidebar.multiselect('Select Products :',options=df['Product'].unique(), default=df['Product'].unique())

        hour=st.sidebar.multiselect('Select time of day :',options=df['Hour'].unique(), default=df['Hour'].unique())

        city=st.sidebar.multiselect('Select the city :',options=df['City'].unique(), default=df['City'].unique())

        day_name=st.sidebar.multiselect('Select day of week :',options=df['day_name'].unique(),default=df['day_name'].unique())

        day=st.sidebar.multiselect('Select day of week :',options=df['day'].unique(),default=df['day'].unique())


        df_selection=df.query("City==@city & Hour==@hour & day_name==@day_name & day==@day & Product==@products")

    #     ##st.dataframe(df_selection)

        st.title("MONTHLY SALES DASHBOARD")
        st.markdown("##")

        total_products=len(df_selection['Product'].unique())
        total_amount=round(df_selection['total_amount'].sum(),2)
        total_sales=round(df_selection['Quantity_Ordered'].sum(),2)
        avg_amount=round(df_selection['total_amount'].mean(),2)

        left_column,middle_column,s_midddle_col,right_column=st.columns(4)

        with left_column:
            st.subheader('Total number of products :')
            st.subheader(f"{total_products} products")
        with middle_column:
            st.subheader('Total sales amount :')
            st.subheader(f" US $ {total_amount}")
        with s_midddle_col:
            st.subheader('Total sales :')
            st.subheader(f"{total_sales}")
        with right_column:
            st.subheader('Average amount per order :')
            st.subheader(f" US $ {avg_amount}")


        st.markdown('---')
        product_by_amount=df_selection.groupby('Product').total_amount.sum().reset_index()
        hour_by_amount=df.groupby('Hour').total_amount.sum().reset_index()
        fig_product_sales=fig=px.bar(product_by_amount,x=product_by_amount.Product,y=product_by_amount.total_amount,
                                    title="<b>Total Sales by Products</b>",
                                    template="plotly_white",
                                    color_discrete_sequence=['#0083B8'] 
                                    )
        fig_hour_sales=fig=px.bar(hour_by_amount,x=hour_by_amount.Hour,y=hour_by_amount.total_amount,
                                    title="<b>Total sales by time of day</b>",
                                    template="plotly_white",
                                    color_discrete_sequence=['#0083B8'] 
                                    )

        fig_product_sales.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=False),
            xaxis=dict(tickmode="linear")
        )


        left_column,right_column=st.columns(2)

        left_column.plotly_chart(fig_hour_sales,use_container_width=True)
        right_column.plotly_chart(fig_product_sales,use_container_width=True)

        daily_sales=df_selection.groupby('day').total_amount.sum().reset_index().sort_values('day')
        daily_sales['day']=daily_sales['day'].astype(int)
        daily_sales=daily_sales.sort_values('day')
        city_sales=df_selection.groupby('City').total_amount.sum().reset_index()
        fig_line_sales=px.line(daily_sales,x=daily_sales.day,y=daily_sales.total_amount,
                                    title="<b>Total sales made per day</b>",
                                    template="plotly_white",
                                    color_discrete_sequence=['#0083B8'] 
                                    )

        fig_line_sales.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=False),
            xaxis=dict(tickmode="linear")
        )
        fig_city_sales=px.pie(city_sales,values=city_sales.total_amount,names=city_sales.City,
                                    title="<b>Total percentage of sales by City</b>",
                                    template="plotly_white",
                                    color_discrete_sequence=['#0083B8'] 
                                    )

        fig_product_sales.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=False),
            xaxis=dict(tickmode="linear")
        )

        left_column,right_column=st.columns(2)
        left_column.plotly_chart(fig_line_sales,use_container_width=True)
        right_column.plotly_chart(fig_city_sales,use_container_width=True)

        product_by_hour=df.groupby(['Product','Hour']).total_amount.sum().reset_index()
        product_by_day_of_week=df.groupby(['Product','day_name']).total_amount.sum().reset_index()

        fig_product_by_hour=px.bar(product_by_hour,x=product_by_hour.Product,y=product_by_hour.total_amount,
                                color=product_by_hour.Hour,barmode='group',
                                    title="<b>Total sales of products by time of day</b>",
                                    template="plotly_white"
                                    #color_discrete_sequence=['#0083B8'] 
                                    )
        fig_product_by_hour.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=False),
            xaxis=dict(tickmode="linear")
        )

        fig_product_by_day_of_week=px.bar(product_by_day_of_week,x=product_by_day_of_week.Product,y=product_by_day_of_week.total_amount,
                                color=product_by_day_of_week.day_name,barmode='group',
                                    title="<b>Total sales of products for each day of the weed.</b>",
                                    template="plotly_white"
                                    #color_discrete_sequence=['#0083B8'] 
                                    )
        fig_product_by_day_of_week.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            yaxis=dict(showgrid=False),
            xaxis=dict(tickmode="linear")
        )
        st.plotly_chart(fig_product_by_hour,use_container_width=True)
        st.plotly_chart(fig_product_by_day_of_week,use_container_width=True)

            #left_column,right_column=st.columns(2)
            #left_column.plotly_chart(fig_product_by_hour,use_container_width=True)
            #right_column.plotly_chart(fig_product_by_day_of_week,use_container_width=True)

