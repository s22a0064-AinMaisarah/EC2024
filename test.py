import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Define CSV URL and encoding
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/EC2024/refs/heads/main/cleaned_student_survey.csv'
ENCODING_TYPE = 'cp1252'

# Streamlit app title
st.title('Gender Distribution of 4th Year Students 🧑‍🤝‍🧑')
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

# Load the dataset
df = load_data(CSV_URL, ENCODING_TYPE)

if df is not None:
    # Clean missing data
    missing_percentage = df.isnull().sum() / len(df) * 100
    cols_to_drop = missing_percentage[missing_percentage > 50].index
    df_cleaned = df.drop(columns=cols_to_drop)

    # Fill missing values with mode
    for col in df_cleaned.columns:
        if df_cleaned[col].isnull().sum() > 0:
            mode_value = df_cleaned[col].mode()[0]
            df_cleaned[col].fillna(mode_value, inplace=True)

    # Filter for 4th-year students
    if 'Bachelor  Academic Year in EU' in df_cleaned.columns:
        fourth_year_students = df_cleaned[df_cleaned['Bachelor  Academic Year in EU'] == '4th Year']

        if not fourth_year_students.empty:
            # Count gender distribution for 4th year
            gender_counts_4th_year = fourth_year_students['Gender'].value_counts()

            # Create Matplotlib pie chart
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.pie(
                gender_counts_4th_year,
                labels=gender_counts_4th_year.index,
                autopct='%1.1f%%',
                startangle=90
            )
            ax.set_title('Gender Distribution of 4th Year Students (Pie Chart)')
            ax.axis('equal')

            # Add legend
            ax.legend(gender_counts_4th_year.index, title="Gender", loc="best")

            # Display chart in Streamlit
            st.pyplot(fig)
        else:
            st.warning("No data found for 4th Year students.")
    else:
        st.error("Column 'Bachelor  Academic Year in EU' not found in dataset.")
else:
    st.error("Failed to load dataset from GitHub.")
