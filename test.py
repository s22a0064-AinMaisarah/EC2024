import streamlit as st
import pandas as pd

# Define the URL and encoding
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/EC2024/refs/heads/main/cleaned_student_survey.csv'
ENCODING_TYPE = 'cp1252'

# Set the title for the application
st.title('Student Survey Data Viewer 📊')
st.markdown('---')

# Use st.cache_data to load and cache the data. This prevents re-downloading
# and re-reading the file every time the app interacts.
@st.cache_data
def load_data(url, encoding):
    """Reads the CSV file from a URL with specified encoding and handles errors."""
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(url, encoding=encoding)
        return df
    except UnicodeDecodeError:
        # Display the error in the Streamlit app
        st.error(f"Could not decode the file with **{encoding}** encoding.")
        st.info("Please check the file encoding in the GitHub repository.")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred while loading the data: {e}")
        return None

# Load the data
df = load_data(CSV_URL, ENCODING_TYPE)

# Display the data if loading was successful
if df is not None:
    st.subheader(f'Data Preview (Total Rows: {len(df)})')
    st.caption(f"Source: {CSV_URL}")
    
    # Display the DataFrame using Streamlit's function
    st.dataframe(df)

    # Optional: Show column information in an expander
    with st.expander("View Data Structure"):
        st.write("Column Names and Data Types:")
        # Use st.dataframe for displaying the info
        st.dataframe(df.dtypes.rename('Data Type'))
