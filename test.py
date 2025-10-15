import streamlit as st
import pandas as pd
import plotly.express as px

# Define CSV URL and encoding
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/EC2024/refs/heads/main/cleaned_student_survey.csv'
ENCODING_TYPE = 'cp1252'

# Streamlit app title
st.title('Gender Distribution Analysis 🧑‍🤝‍🧑')
st.markdown('---')

# Load and cache data
@st.cache_data
def load_data(url, encoding):
    try:
        df = pd.read_csv(url, encoding=encoding)
        return df
    except UnicodeDecodeError:
        st.error(f"Could not decode the file with {encoding}.")
        return None
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data(CSV_URL, ENCODING_TYPE)

# Generate pie chart if data loaded successfully
if df is not None and 'Gender' in df.columns:
    gender_counts = df['Gender'].value_counts().reset_index()
    gender_counts.columns = ['Gender', 'Count']

    fig = px.pie(
        gender_counts,
        names='Gender',
        values='Count',
        title='Overall Gender Distribution',
        color_discrete_sequence=px.colors.qualitative.D3,
        hole=0.4  # donut style
    )

    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        marker=dict(line=dict(color='#000000', width=1))
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("The dataset could not be loaded or does not contain a 'Gender' column.")
