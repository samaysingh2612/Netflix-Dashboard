import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="Netflix Data Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ---------------- CUSTOM CSS ---------------- #

st.markdown("""
<style>

.main {
    background-color: #141414;
    color: white;
}

h1,h2,h3,h4 {
    color: #E50914;
}

.stButton>button {
    background-color: #E50914;
    color: white;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ---------------- #

st.title("🎬 Netflix Data Analysis Dashboard")
st.write("Interactive dashboard using Pandas, NumPy, Matplotlib, Seaborn & Streamlit")

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    df = pd.read_csv("netflix.csv")
    return df

df = load_data()

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("Dashboard Menu")

option = st.sidebar.radio(
    "Select Section",
    [
        "Home",
        "Dataset Overview",
        "Missing Values",
        "Duplicate Records",
        "Movie Search",
        "Director Analysis",
        "Release Year Analysis",
        "Content Analysis",
        "Heatmap",
        "Visualizations",
        "About"
    ]
)

# ---------------- HOME ---------------- #

if option == "Home":

    st.image(
       "https://images.unsplash.com/photo-1574375927938-d5a98e8ffe85",
    width=1200
    )

    st.header("📊 Dashboard Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())
    col4.metric("Duplicate Rows", df.duplicated().sum())

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

# ---------------- DATASET OVERVIEW ---------------- #

elif option == "Dataset Overview":

    st.header("Dataset Information")

    st.subheader("Shape of Dataset")
    st.write(df.shape)

    st.subheader("Columns")
    st.write(df.columns)

    st.subheader("Data Types")
    st.write(df.dtypes)

    st.subheader("Statistical Summary")
    st.dataframe(df.describe(include='all'))

# ---------------- MISSING VALUES ---------------- #

elif option == "Missing Values":

    st.header(" Missing Values")

    missing = df.isnull().sum()

    st.dataframe(missing)

    fig, ax = plt.subplots(figsize=(10,5))

    missing.plot(kind='bar', ax=ax)

    st.pyplot(fig)

# ---------------- DUPLICATE RECORDS ---------------- #

elif option == "Duplicate Records":

    st.header(" Duplicate Records")

    duplicate = df[df.duplicated()]

    st.write("Total Duplicate Rows:", duplicate.shape[0])

    st.dataframe(duplicate)

# ---------------- MOVIE SEARCH ---------------- #

elif option == "Movie Search":

    st.header("🔍 Search Movie or Show")

    search = st.text_input("Enter Movie Name")

    if search:

        result = df[df.astype(str).apply(
            lambda row: row.str.contains(search, case=False).any(),
            axis=1
        )]

        st.dataframe(result)

# ---------------- DIRECTOR ANALYSIS ---------------- #

elif option == "Director Analysis":

    st.header(" Top Directors")

    if 'Director' in df.columns:

        directors = df['Director'].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(12,6))

        directors.plot(kind='bar', ax=ax)

        plt.xticks(rotation=45)

        st.pyplot(fig)

    else:
        st.warning("Director column not found.")

# ---------------- RELEASE YEAR ANALYSIS ---------------- #

elif option == "Release Year Analysis":

    st.header("📅 Release Year Analysis")
    df['DATE_N'] = pd.to_datetime(df['Release_Date'] , format ='mixed')
    df["YEARS"] = df['DATE_N'].dt.year
    possible_cols = ['YEARS', 'release_year']

    year_col = None

    for col in possible_cols:
        if col in df.columns:
            year_col = col

    if year_col:

        release = df[year_col].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(14,6))

        release.plot(ax=ax)

        st.pyplot(fig)

    else:
        st.warning("Release Year column not found.")

# ---------------- CONTENT ANALYSIS ---------------- #

elif option == "Content Analysis":

    st.header("📺 Content Type Analysis")

    possible_cols = ['Category', 'type']

    type_col = None

    for col in possible_cols:
        if col in df.columns:
            type_col = col

    if type_col:

        fig = px.pie(
            df,
            names=type_col,
            title="Movies vs TV Shows"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.warning("Content Type column not found.")

# ---------------- HEATMAP ---------------- #

elif option == "Heatmap":

    st.header(" Correlation Heatmap")

    numeric_df = df.isnull()

    fig, ax = plt.subplots(figsize=(12,8))

    sns.heatmap(
        numeric_df.corr(),
        annot=True,
        cmap='coolwarm',
        ax=ax
    )

    st.pyplot(fig)

# ---------------- VISUALIZATIONS ---------------- #

# ---------------- VISUALIZATIONS ---------------- #

elif option == "Visualizations":

    st.header("📈 Netflix Visualizations")

    chart = st.selectbox(
        "Select Visualization",
        [
            "Content Type Count",
            "Top 10 Countries",
            "Top 10 Directors",
            "Release Year Distribution",
            "Ratings Distribution"
        ]
    )

    # CONTENT TYPE
    if chart == "Content Type Count":

        if 'Type' in df.columns:

            fig, ax = plt.subplots(figsize=(8,5))

            sns.countplot(x='Type', data=df, ax=ax)

            st.pyplot(fig)

    # TOP COUNTRIES
    elif chart == "Top 10 Countries":

        if 'Country' in df.columns:

            top_country = df['Country'].value_counts().head(10)

            fig, ax = plt.subplots(figsize=(12,5))

            top_country.plot(kind='bar', ax=ax)

            plt.xticks(rotation=45)

            st.pyplot(fig)

    # TOP DIRECTORS
    elif chart == "Top 10 Directors":

        if 'Director' in df.columns:

            top_director = df['Director'].value_counts().head(10)

            fig, ax = plt.subplots(figsize=(12,5))

            top_director.plot(kind='bar', ax=ax)

            plt.xticks(rotation=45)

            st.pyplot(fig)

    # RELEASE YEAR
    elif chart == "Release Year Distribution":

        if 'YEARS' in df.columns:

            fig, ax = plt.subplots(figsize=(12,5))

            sns.histplot(df['YEARS'], bins=30, kde=True, ax=ax)

            st.pyplot(fig)

    # RATINGS
    elif chart == "Ratings Distribution":

        if 'Rating' in df.columns:

            fig, ax = plt.subplots(figsize=(12,5))

            sns.countplot(y='Rating', data=df, order=df['Rating'].value_counts().index, ax=ax)

            st.pyplot(fig)

# ---------------- ABOUT ---------------- #

elif option == "About":

    st.header("👨‍💻 About This Project")

    st.write("""
    This project demonstrates:

    1. NumPy Operations  
    2. Pandas Data Analysis  
    3. Data Cleaning  
    4. Missing Value Handling  
    5. Duplicate Handling  
    6. Matplotlib Visualizations  
    7. Seaborn Charts  
    8. Interactive Dashboard using Streamlit  

    """)

