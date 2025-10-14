import streamlit as st
import pandas as pd
import plotly.express as px

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






# NOTE: This assumes 'df' is the DataFrame loaded from the CSV file.
# You would need the data loading part from the previous example to run this fully.

def generate_gender_pie_chart(df):
    """
    Generates and displays an interactive Plotly Pie Chart for Gender Distribution.
    """
    st.header('Gender Distribution Analysis 🧑‍🤝‍🧑')

    # Check if the 'Gender' column exists
    if 'Gender' not in df.columns:
        st.error("DataFrame does not contain a 'Gender' column for plotting.")
        return

    # Plotly Express automatically handles counting the occurrences ('names')
    fig = px.pie(
        df,
        names='Gender',
        title='Overall Gender Distribution',
        # Customizations for a better visual:
        color_discrete_sequence=px.colors.qualitative.D3, # Choose a color palette
        hole=0.4 # Make it a donut chart
    )

    # Enhance the chart appearance
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1))
    )
    
    # Update layout for cleaner presentation
    fig.update_layout(
        showlegend=True,
        uniformtext_minsize=12,
        uniformtext_mode='hide'
    )

    # Display the interactive chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

# --- Example Usage (Assuming 'df' is available) ---
# NOTE: To run this, you must first load your data, e.g., using the function below:

# @st.cache_data
# def load_data(url, encoding):
#     # ... (previous data loading code)
#     return df

# df = load_data(CSV_URL, ENCODING_TYPE)
# if df is not None:
#     generate_gender_pie_chart(df)
