import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title='Analytics Portal',
    page_icon='📈'
)
st.title(':rainbow[Data Analytics Portal]')
st.subheader(':grey[Explore Data with ease.]',divider='rainbow')

file= st.file_uploader('Upload csv or xlsx file',type=['csv','xlsx'])
if (file!=None):
    if (file.name.endswith('csv')):
        data= pd.read_csv(file)
    else:
        data= pd.read_excel(file)
    st.dataframe(data)
    st.info('File Successfully Uploaded',icon='🔎')

    st.subheader(':rainbow[Basic Information of the Dataset]',divider='rainbow')
    tab1,tab2,tab3,tab4= st.tabs(['Summary','Top & Bottom Rows', 'Data Types','Columns Available'])

    with tab1:
        st.write(f'There are {data.shape[0]} rows & {data.shape[1]} columns in the dataset.')
        st.subheader(':grey[Statistical Summary of the Dataset]')
        st.dataframe(data.describe())
    with tab2:
        st.subheader(':grey[Top Rows]')
        toprows=st.slider('No. of Rows to Display:',1,data.shape[0],key='top slider')
        st.dataframe(data.head(toprows))
        st.subheader(':grey[Bottom Rows]')
        bottomrows=st.slider('No. of Rows to Display:',1,data.shape[0],key='bottom slider')
        st.dataframe(data.tail(bottomrows))
    with tab3:
        st.subheader(':grey[Column Data Types]')
        st.dataframe(data.dtypes)
    with tab4:
        st.subheader(':grey[Column Names in the Dataset]')
        st.write(list(data.columns))

    st.subheader(':rainbow[Column Values to Count]',divider='rainbow')
    with st.expander('Value Counts'):
        col1,col2=st.columns(2)
        with col1:
            column= st.selectbox('Choose Column Name',options=list(data.columns))
        with col2:
            toprows=st.number_input('Top Rows',min_value=1,step=1)
        
        count= st.button('Count')
        if (count==True):
            result= data[column].value_counts().reset_index().head(toprows)
            st.dataframe(result)
            st.subheader(':grey[Visualisation]',divider='grey')
            fig= px.bar(data_frame=result,x=column,y='count',color=column,text='count')
            st.plotly_chart(fig)
            fig= px.line(data_frame=result,x=column,y='count',markers='o',text='count')
            fig.update_traces(textposition='bottom left')
            st.plotly_chart(fig)
            fig= px.pie(data_frame=result,names=column,values='count')
            st.plotly_chart(fig)

    st.subheader(':rainbow[Groupby: Simplify Your Data Analysis]',divider='rainbow')
    st.write('''Groupby is a powerful method in data analysis, allowing you to group data based on one or more columns,
                apply aggregation, transformation, or filtering functions on grouped subsets.''')
    with st.expander('Group By Your Columns'):
        col1,col2,col3=st.columns(3)
        with col1:
            groupby_col=st.multiselect('Choose Your Columns to groupby',options=list(data.columns))
        with col2:
            operation_col= st.selectbox('Choose Column for Operation',options=list(data.columns))
        with col3:
            operation= st.selectbox('Choose Operation to perform',options=['sum','max','min','mean','median','count'])
        
        if(groupby_col):
            result= data.groupby(groupby_col).agg(
                new_col=(operation_col,operation)
            ).reset_index()
            st.dataframe(result)
        
            st.subheader(':grey[Data Visualisation]',divider='grey')
            graphs=st.selectbox('Choose your grapgh type',options=['line','pie','bar','scatter','sunburst'])
            if (graphs=='line'):
                x_axis=st.selectbox('Select x-axis',options=list(result.columns))
                y_axis=st.selectbox('Select y-axis',options=list(result.columns))
                color=st.selectbox('Color Information',options=[None]+list(result.columns))
                fig=px.line(data_frame=result,x=x_axis,y=y_axis,color=color)
                st.plotly_chart(fig)
            elif (graphs=='bar'):
                x_axis=st.selectbox('Select x-axis',options=list(result.columns))
                y_axis=st.selectbox('Select y-axis',options=list(result.columns))
                color=st.selectbox('Color Information',options=[None]+list(result.columns))
                facet_col=st.selectbox('Column Information',options=[None]+list(result.columns))
                fig=px.bar(data_frame=result,x=x_axis,y=y_axis,color=color,facet_col=facet_col,barmode='group')
                st.plotly_chart(fig)
            elif (graphs=='scatter'):
                x_axis=st.selectbox('Select x-axis',options=list(result.columns))
                y_axis=st.selectbox('Select y-axis',options=list(result.columns))
                color=st.selectbox('Color Information',options=[None]+list(result.columns))
                size=st.selectbox('Size Column',options=[None]+list(result.columns))
                fig=px.scatter(data_frame=result,x=x_axis,y=y_axis,color=color,size=size)
                st.plotly_chart(fig)
            elif (graphs=='pie'):
                names=st.selectbox('Select labels',options=list(result.columns))
                values=st.selectbox('Select Numerical Values',options=list(result.columns))
                fig=px.pie(data_frame=result,names=names,values=values)
                st.plotly_chart(fig)
            elif (graphs=='sunburst'):
                path=st.multiselect('Select your path',options=list(result.columns))
                fig=px.sunburst(data_frame=result,path=path,values='new_col')
                st.plotly_chart(fig)
