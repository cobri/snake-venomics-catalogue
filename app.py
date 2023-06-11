#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image
from st_aggrid import GridOptionsBuilder, AgGrid, ColumnsAutoSizeMode

st.set_page_config(
      page_title="",
      page_icon=":snake:",
      layout="wide",
      initial_sidebar_state="expanded",
      # menu_items={
      #     'Get Help': '...',
      #     'Report a bug': "...",
      #     'About': "..."
      # }
 )

st.title(' Welcome to the Snake Venomics Online Catalogue :snake:')
st.subheader('To view venomics data please select a snake: 👇')
option = st.selectbox(
    '',
    ('Select from this list', 'Dendroaspis angusticeps', 'Dendroaspis polylepis'))

## INPUT OPTIONS ##

if option == 'Dendroaspis angusticeps':
    df1 = pd.read_csv('Data/Da/Da_Dataset_webplotdigi_5_5_annotated.csv') 
    df2 = pd.read_csv('Data/Da/Da_table_edited.csv') 
    Name = 'Dendroaspis angusticeps'
    image = Image.open('Data/Da/Da_chrom_cut.jpg')
    Source = 'https://www.sciencedirect.com/science/article/pii/S1874391916300264'
    
elif option == 'Dendroaspis polylepis':
    df1 = pd.read_csv('Data/Dp/Dp_Dataset_webplotdigi_2_2_annotated.csv') 
    df2 = pd.read_csv('Data/Dp/Dp_table_edited.csv') 
    Name = 'Dendroaspis polylepis'
    image = Image.open('Data/Dp/Dp_chrom_cut.jpg')
    Source = 'https://www.sciencedirect.com/science/article/pii/S1874391915000561'
    
else: 
    st.stop()  
     
## CHROMATOGRAM ##

fig1 = px.line(df1, x="Time", y="Absorbance", hover_name="Peak",
                hover_data={'Time':False,
                            'Absorbance':False,
                            'Protein':True},
                title= Name +' chromatogram')

fig1.update_xaxes(range=[0.5, 90])
fig1.update_layout(xaxis_title='Time (min)',
                  yaxis_title='Absorbance 215nm (Mu)')
st.plotly_chart(fig1, use_container_width=True)

st.markdown("**Original manuscript figure:**")
st.image(image, 
          #width=1200, 
          caption='Source: ' + Source)


## TABLE ##

st.markdown("**Original manuscript table:**")

gb = GridOptionsBuilder.from_dataframe(df2)
gb.configure_side_bar() #Add a sidebar
#gb.configure_first_column_as_index() # Pins peak to the left side
other_options = {'suppressColumnVirtualisation': True} #Load all columns not just the visible ones
gb.configure_grid_options(**other_options)
gb.configure_selection('multiple', use_checkbox=True, groupSelectsChildren="Group checkbox select children") #Enable multi-row selection
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc="sum", editable=True)
gridOptions = gb.build()


grid_response = AgGrid(
    df2,
    gridOptions=gridOptions,
    columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS, #Auto-size the widths of the columns
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    theme="streamlit", #Add theme color
    enable_enterprise_modules=True,
    height=550
    #width='100%',
    #reload_data=True
)
        
