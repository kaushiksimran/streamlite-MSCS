import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import json
from PIL import Image

image = Image.open('MSCS_LOGO.png')

st.image(image, width = 300)

# Simple Text
st.header('Ministry of Coorperation - CRCS Portal')
st.write('Welcome to our portal! Here you will get information regarding Societies.')

# navigation bar
st.sidebar.title('Navigation')
options = st.sidebar.radio('Select options below to know more:', ['Home','State Filteration','Sector Filteration'])

df = pd.read_csv('Final_CRCD_Govt.csv')
 ##################  ALL THESE ARE UNDER HOME ####################

 # giving whole data on the screen
@st.cache_data(experimental_allow_widgets=True)
def stats():
    
    st.write(df)
    def convert_df(df):
        # IMPORTANT: Cache the conversion to prevent computation on every rerun
        return df.to_csv().encode('utf-8')

    csv = convert_df(df)

    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='data.csv',
        mime='text/csv',
    )

    st.write(' ')
    #plot 1
    st.header('Different Types of Sectors')
    sector_counts = df['Sector Type'].value_counts()
    fig4 = go.Figure(go.Treemap(labels=sector_counts.index, parents=['']*13, values=sector_counts.values))
    fig4.update_layout(
        font = dict(size = 18)        
    )
    st.write(fig4)


    st.divider() 

    #plot2

    st.header('Total no. of Different Types of Sectors available')
    
    fig = px.histogram(df, x="Sector Type", histfunc="count", text_auto=True, width=1000, height=800)
    fig.update_layout(
        font = dict(size = 18)   
    )
    
    st.write(fig)

    st.header('Percentage of Societies per Sector')
    sect_type = df['Sector Type'].value_counts()
    fig2 = px.pie(labels=sect_type.index, values=sect_type.values, names=sect_type.index, color_discrete_sequence=px.colors.sequential.RdBu)
    fig2.update_traces(textposition='inside', textfont_size=15, textinfo='percent')
    st.write(fig2)

    st.markdown('There are about **:blue[52.5%]** of societies available for **:blue[Agro]**  Sector accross India and for sectors such as Dairy, Construction and Tourism have almost neglegible number of societies.')
    st.markdown('Other avaiable sectors are approx. **:blue[18%]** less then the most available sector Agro.')

    st.divider() 

    #plot3
    st.header('No. of Societies per State')
    fig3 = px.histogram(df, x="State", histfunc="count", text_auto=True, width=1000, height=800)
    st.write(fig3)

    m = df['State'].value_counts()
    st.markdown(f'Out of **:blue[{df.State.nunique()}]** States across India,  **:blue[{m.index[0]}]** has highest no. of societies. ')

    st.divider() 


    # plot 4
    m = df['State'].value_counts()

    ll = []
    n = m.index
    for i in n:
        if i == 'NEW DELHI':
            ll.append('NCT of Delhi')
        elif i == 'JAMMU AND KASHMIR':
            ll.append('Jammu & Kashmir')
        else:
            ll.append(i.title())

    d = pd.DataFrame(ll, columns=['States'])

    v = d.assign(Count=m.values)

    india_states = json.load(open("states_india.geojson", "r"))

    state_id_map = {}

    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]

    v["id"] = v["States"].apply(lambda x: state_id_map[x])

    st.header('Coverage of Different Indian States')
        
    fig5 = px.choropleth(
        v,
        locations="id",
        geojson=india_states,
        color="Count",
        hover_name="States",
        hover_data=["Count"],
        color_continuous_scale=px.colors.diverging.BrBG,
        color_continuous_midpoint=5,
    )
    fig5.update_geos(fitbounds="locations", visible=False)
    st.write(fig5)

    st.markdown('Note: Only the states which are present in the dataset are included in the map.')
    

###################### ALL THESE ARE UNDER FILTERS ##########################
####################################################################### Filter 1 #############################################################

def state_filt():
    st.write(" ")
    st.subheader('Apply State Filters here for enchancing your search')
    ############### dropdown 1 #################
    m = df['State'].value_counts()
    n = m.index
    ll = []
    for i in n:
        ll.append(i)

    option = st.selectbox(
    'Choose your STATE',
    (ll))

    st.write(f'You selected: **:blue[{option}]**')
    
    ch_state = option
    n = df[df['State'] == ch_state]
    st.write(n)

    g = df[df['State'] == ch_state]['Sector Type'].unique()
    len_g = len(g)
    st.write(" ")
    st.header('Different Sectors available in your State')
    sector_counts = df[df['State'] == ch_state]['Sector Type'].value_counts()
    fig8 = go.Figure(go.Treemap(labels=sector_counts.index, parents=['']*len_g, values=sector_counts.values))
    fig8.update_layout(
        font = dict(size = 18)        
    )
    st.write(fig8)


    agree = st.checkbox( f'Want to see the distribution of societies in **:blue[{option}]** ?')
    if agree:
        st.write(' ')
        st.subheader('No. of Sectors available in Different Districts')
        count_df = df.groupby([n['District'], n['Sector Type']]).size().reset_index(name='Count')

        fig6 = go.Figure(data=[go.Bar(x=count_df['District'], y=count_df['Count'], text=count_df['Sector Type'], textposition='auto')])
        fig6.update_layout(xaxis_title=ch_state,
                        yaxis_title='COUNT',width=1000, height=800)
        
        fig6.update_layout(
            font = dict(size = 18)        
        )

        st.write(fig6)

###############################################


############### dropdown 2 #################
    st.write(' ')
    st.write(' ')
    state_list = []
    s = df[df['State'] == ch_state]['District'].unique()

    for item in s:
        if str(item) != 'nan':
            state_list.append(item)
        
    option2 = st.selectbox(
    'Choose your DISTRICT',
    (state_list))
    st.write(f'You selected: **:blue[{option2}]**')
    
    ch_dictt = option2
    st.subheader(f'Based on District for {ch_state}')
    m = df[(df['State'] == ch_state) & (df['District'] == ch_dictt)]
    st.write(m)
#########################################################

########################### dropdown 3 ###############################
    sectors = df[df['State'] == ch_state]['Sector Type'].unique()
    sec_list = sectors.tolist()
    
    option3 = st.selectbox(
    'Choose your Sector',
    (sec_list))
    st.write(f'You selected: **:blue[{option3}]**')
    st.subheader(f'Based on Sector for {ch_state}')
    ch_sector = option3
    df[(df['State'] == ch_state) & (df['Sector Type'] == ch_sector)]

########################################################################
######################################################################### Filter 2 ####################################################################
def sec_filt():
    st.write(" ")
    st.subheader('Apply Sector Filters here for enchancing your search')
    st.write(" ")
    st.write(" ")
    st.subheader('Distribution of Different Sectors')
    fig9 = px.histogram(df, x="Sector Type", histfunc="count", text_auto=True, width=1000, height=800)
    fig9.update_layout(
            font = dict(size = 18)        
        )
    st.write(fig9)

    st.markdown('The **:blue[Agro]**  Sector is the most emerging sector across India.')

    st.write(" ")
    u_sec = df['Sector Type'].unique()
    uni_sec = u_sec.tolist()
    option6 = st.selectbox(
    'Choose your Sector',
    (uni_sec))
    st.write(f'You selected: **:blue[{option6}]**')
    c = df[df['Sector Type'] == option6]
    agree = st.checkbox(f'Want to see the distribution of **:blue[{option6}]** ?')
    if agree:
        st.write(' ')
        st.subheader(f'Distribution of {option6}')
        fig7 = px.histogram(c, x="State", histfunc="count", text_auto=True, width=1000, height=800)
        fig7.update_layout(
            font = dict(size = 18)        
        )
        st.write(fig7)

    st.write(' ')
    st.write(c)


########################## Navigation Options ##############################


if options == 'Home':
    stats()

elif options == 'State Filteration':
    state_filt()

elif options == 'Sector Filteration':
    sec_filt()
