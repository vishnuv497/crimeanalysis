import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title='Crime Rate Analysis', layout='wide')

# Title
st.title('Crime Rate Analysis Dashboard')

# File uploader
uploaded_file = st.file_uploader("Upload Crime Data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Load data
    df = pd.read_csv(uploaded_file)
    st.write("### Raw Data Preview")
    st.dataframe(df.head())
    
    # Select relevant columns
    numerical_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Sidebar filters
    st.sidebar.header("Filter Data")
    selected_category = st.sidebar.selectbox("Select Category", categorical_cols)
    selected_value = st.sidebar.selectbox("Select Value", df[selected_category].unique())
    filtered_df = df[df[selected_category] == selected_value]
    
    st.write(f"### Filtered Data by {selected_category} = {selected_value}")
    st.dataframe(filtered_df.head())
    
    # Visualization
    st.write("### Crime Rate Trends")
    if 'Year' in df.columns and 'Crime Rate' in df.columns:
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x='Year', y='Crime Rate', hue=selected_category)
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.warning("Ensure your dataset has 'Year' and 'Crime Rate' columns for trend analysis.")
    
    # Heatmap for correlation
    st.write("### Correlation Heatmap")
    if numerical_cols:
        plt.figure(figsize=(10, 5))
        sns.heatmap(df[numerical_cols].corr(), annot=True, cmap='coolwarm', fmt='.2f')
        st.pyplot(plt)
    else:
        st.warning("No numerical columns found for correlation analysis.")
