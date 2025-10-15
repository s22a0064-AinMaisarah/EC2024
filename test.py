import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIGURATION ---
CSV_URL = 'https://raw.githubusercontent.com/s22a0064-AinMaisarah/EC2024/refs/heads/main/cleaned_student_survey.csv'
ENCODING_TYPE = 'cp1252'

# --- STREAMLIT APP TITLE ---
st.title("🎓 Gender Distribution of 4th Year Students")
st.markdown("This dashboard shows the gender distribution among 4th-year students based on the provided dataset.")
st.markdown("---")

# --- DATA LOADING FUNCTION ---
@st.cache_data
def load_data(url, encoding):
    """Loads and caches data from GitHub with specified encoding."""
    try:
        df = pd.read_csv(url, encoding=encoding)
        return df
    except UnicodeDecodeError:
        st.error(f"Could not decode the file with encoding: {encoding}.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# --- LOAD THE DATA ---
df = load_data(CSV_URL, ENCODING_TYPE)

# --- DATA CLEANING ---
if not df.empty:
    st.subheader("📋 Raw Data Preview")
    st.dataframe(df.head())

    # Handle missing values
    missing_percentage = df.isnull().sum() / len(df) * 100
    cols_to_drop = missing_percentage[missing_percentage > 50].index
    df_cleaned = df.drop(columns=cols_to_drop)

    for col in df_cleaned.columns:
        if df_cleaned[col].isnull().sum() > 0:
            mode_value = df_cleaned[col].mode()[0]
            df_cleaned[col].fillna(mode_value, inplace=True)

    # --- FILTER FOR 4TH YEAR STUDENTS ---
    if 'Bachelor  Academic Year in EU' in df_cleaned.columns:
        fourth_year_students = df_cleaned[df_cleaned['Bachelor  Academic Year in EU'] == '4th Year']

        if not fourth_year_students.empty:
            # --- COUNT GENDER DISTRIBUTION ---
            gender_counts_df = fourth_year_students['Gender'].value_counts().reset_index()
            gender_counts_df.columns = ['Gender', 'Count']

            # --- PLOTLY PIE CHART ---
            fig = px.pie(
                gender_counts_df,
                values='Count',
                names='Gender',
                title='Gender Distribution of 4th Year Students',
                color_discrete_sequence=px.colors.qualitative.D3
            )

            fig.update_traces(
                textposition='inside',
                textinfo='percent+label',
                marker=dict(line=dict(color='#000000', width=1))
            )

            fig.update_layout(title_x=0.5)

            # --- DISPLAY CHART ---
            st.plotly_chart(fig, use_container_width=True)

            # --- SHOW DATA TABLE ---
            st.subheader("🔢 Gender Count Data")
            st.dataframe(gender_counts_df)
        else:
            st.warning("No data found for 4th Year students.")
    else:
        st.error("Column 'Bachelor  Academic Year in EU' not found in dataset.")
else:
    st.error("Failed to load dataset from GitHub.")
