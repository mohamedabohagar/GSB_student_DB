import streamlit as st
import requests
import pandas as pd
import pdfkit
import calendar
from datetime import datetime


# Define a function to fetch and process data, and use @st.cache to cache its results
@st.cache_resource
def fetch_and_process_data(locations, selected_semester, quarter, study_type, weeks, fastapi_post):
    try:
        # Construct the query parameters
        query_params = {
            'location': locations,
            'semester': selected_semester,
            'quarter': quarter,
            'study_type': study_type,
            'week': str(weeks)
        }
        response = requests.get(url=fastapi_post, params=query_params)
        response.raise_for_status()  # Check for HTTP errors
        data_all = response.json()
        if data_all:
            rooms = [] 
            for index, row_data in enumerate(data_all):
                room = ""
                rooms.append(room)
            df = pd.DataFrame(data_all)
            df['Room']  = rooms
            df.columns = ['TimeTableID', 'Moodle_Course', 'Day', 'StartDate', 'FinalExamDate', 'Room']
            df = df.astype(str)
            return df
        else:
            return None

    except requests.exceptions.RequestException as e:
        st.error(f" An error occurred while fetching the timetable: {e}")
        return None

st.set_page_config(layout="wide")
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
fastapi_get = 'http://localhost:8000/alllocation'
fastapi_post = 'http://localhost:8000/tables'
st.title('TimeTable Programming For GSB Alexander')
Year = [datetime.today().year, datetime.today().year+1]
with st.form("Login" ,clear_on_submit=True):
    try:
        # Send an HTTP GET request to the FastAPI endpoint
        response = requests.get(url=fastapi_get)
        response.raise_for_status()  # Check for HTTP errors

        # Parse the JSON response
        data = response.json()

        # Display the fetched data
        if data:
            col0, col00 = st.columns(2)
            with col0:
                locations = st.selectbox('Select Location', data, 0)  # Assuming the first option is selected by default
        else:
            st.info('No data available.')

    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching locations: {e}")

    col1, col2, col3 = st.columns(3)

    with col1:
        semester = st.selectbox('Select Semester', ['Spring ', 'Fall '], index=0)

    with col2:
        years = st.selectbox('The Year: ', Year , index=0)

    with col3:
        quarter = st.selectbox('Select Quarter', ['Q1', 'Q2'], index=0)

    col4, col5, col6 = st.columns(3)

    with col4:
        study_type = st.selectbox('Select Study Type', ['Online', 'Smart', 'Attend', 'Hybrid'], index=0)

    with col5:
        weeks = st.selectbox('Select Week', ['1', '2', '3'], index=0)

    selected_semester = str(semester) + str(years)

    df = []
    if st.form_submit_button('Fetch Timetable', type="primary"):
        df = fetch_and_process_data(locations, selected_semester, quarter, study_type, weeks, fastapi_post)
        if df is not None:
            st.subheader('TimeTable:')
            #st.dataframe(df, use_container_width=True)
            edited_df = st.data_editor(df)
            #favorite_command = edited_df.loc[edited_df["Room"].idxmax()]["TimeTableID"]           
            html_file = 'dataframe.html'
            edited_df.to_html(html_file, index=False)
            pdf_file = 'dataframe.pdf'
            config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe" )
            options = {
                'page-size': 'Letter',
                'margin-top': '0.75in',
                'margin-right': '0.75in',
                'margin-bottom': '0.75in',
                'margin-left': '0.75in',
                'encoding': "UTF-8",
                'custom-header': [
                    ('Accept-Encoding', 'gzip')
                ]}
            pdfkit.from_file(html_file, pdf_file, configuration=config, options=options)
            st.success(f'PDF file "{pdf_file}" generated successfully with Arabic text.')
        else:
            st.info('No data available.')