import streamlit as st 
from utils.random_data_generator import generate_random_production_dataframe
from utils.schedule_generator import schedule_generator
import pandas as pd
import requests
from pathlib import Path

def read_file(file_path):
    if file_path.startswith("http://") or file_path.startswith("https://"):
        try:
            response = requests.get(file_path)
            response.raise_for_status()
            return response.text 
        except requests.exceptions.ReadTimeoutException as e:
             return f"Error fetching the file: {e}"
    else:
        path = Path(file_path)
        if path.is_file():
            if path.is_file():
                return path.read_text(encoding='utf-8')
            else:
                return f"File not found: {file_path}"
            
def main():
    st.title("Production Schedule Generator")
    st.write("This app generates a production schedule for a given production dataframe.")
    st.write("The production dataframe should have the following columns:")
    st.markdown("__DATE__ : as index")
    st.markdown("__FOPR__: Oil production")
    st.markdown("__FGPR__: Gas production")
    st.markdown("__FWPR__: Water production")
    st.markdown("__FIELD__: could be group, or wells")
    st.markdown("__MOTHER_FIELD__: which groups belong to the field")

    choice= st.radio("Data from excel sheet", key='excel', options=['excel', 'csv','random'])

    if choice == 'excel':
        st.write("Please upload the excel file")
        df = st.file_uploader("Upload excel file", type=['xlsx'])
        if df is not None:
            df = pd.read_excel(df, index_col='DATE', parse_dates=True)
            st.dataframe(df)
    
    elif choice =='csv':
        st.write("Please upload the csv file")
        df = st.file_uploader("Upload csv file", type=['csv'])
        if df is not None:
            df = pd.read_csv(df, index_col='DATE', parse_dates=True)
            st.dataframe(df)
    else:
        st.write("Generating random production dataframe")
        df = generate_random_production_dataframe()
        st.dataframe(df)
    save_folder =st.text_input("Enter the folder to save the schedule", ".")
    generate_schedule = st.button("Generate Schedule")
    if generate_schedule:
        schedule = schedule_generator(df,export_file=save_folder) 
        st.success("Schedule generated")
        #choice =st.checkbox("show the schedule")
        st.write(schedule)
        file_url = read_file(schedule)
        if file_url:
            #st.write(file_url)
            st.text_area("Schedule Content", file_url, height=1000) 
        
          

if __name__ == "__main__":
    main()