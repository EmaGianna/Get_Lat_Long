import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from io import StringIO
import streamlit as st
from geopy.geocoders import Nominatim
import base64
from loguru import logger

@st.cache
def get_data_latlon(country_list, prefix):

    lat = []
    lon = []
    place = []

    for country in country_list:
        try: 
            geolocator = Nominatim(user_agent='Cities_AR')
            location = geolocator.geocode(country)
            lat.append(location.latitude)
            lon.append(location.longitude)
            place.append(country)
        except:
            pass

    df_coord = pd.DataFrame({'COUNTRY_' + prefix : place, 'LAT_' + prefix : lat, 'LON_' + prefix : lon})

    return df_coord 
    
def get_show_map(df_data): 

    df_data.columns = ['Place','lat','lon']
    st.map(df_data)

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False, sep=';')
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'
    return href


if __name__ == '__main__':

    st.sidebar.title('Instructions\n')
    st.sidebar.text('1. Please select a csv file that\n contain country list.\n2. Wait few time.\n3. Verify on the map.\n4. Download the file.')

    st.title('Get Latitude and Longitude of Places List\n')

    st.header('Upload a File\n')
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:

        st.header('List Places\n')
        dataframe = pd.read_csv(uploaded_file)
        st.write(dataframe)

        column = dataframe.columns.tolist()                  
        list_place = dataframe[column[0]].unique().tolist()    #List of Values
        st.header('Latitude and Longitude of Places\n')
        st.write(get_data_latlon(list_place,'DATA'))
        df = get_data_latlon(list_place,'DATA')
        st.header('Map Places(Please verify)\n')
        get_show_map(df)
        st.header('Download File with the points\n')
        st.markdown(get_table_download_link(df), unsafe_allow_html=True)
