import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go  # Import graph objects (go) from plotly

st.subheader("Comparison of Country size (in sq. km) to Military size")



#Load data from the COMBINED .csv file
df = pd.read_csv('https://github.com/mike-ua/Streamlit-Data/blob/950c1c715785bd84c6bbcd9f9c98803bf9de4b2b/Country_Military_Size_August_2024.csv')


#Clean column names to avoid issues with spaces or case sensitivity
df.columns = df.columns.str.strip()

#Sidebar - User input

#Add an "All" option to the list of countries
country_list = df['Country'].unique().tolist()
country_list.insert(0, "All")

selected_countries = st.sidebar.multiselect(
    "Select Countries", 
    country_list
)

#If "All" is selected, include all countries
if "All" in selected_countries:
    selected_countries = df['Country'].unique()

selected_category = st.sidebar.radio(
    "Select Military Category", 
    ['Active_Military', 'Reserve_Military', 'Paramilitary', 'Total']
)

#Filter data based on selection
filtered_df = df[df['Country'].isin(selected_countries)]

#Calculate the 95th percentiles for sq_km and the selected military category
sq_km_threshold = filtered_df['sq_km'].quantile(0.95)
category_threshold = filtered_df[selected_category].quantile(0.95)

#Identify countries that are in the top 5% for either sq_km or the selected military category
special_countries = filtered_df[
    (filtered_df['sq_km'] > sq_km_threshold) | 
    (filtered_df[selected_category] > category_threshold)
]

#Create a basic scatter plot
fig = px.scatter(
    filtered_df, 
    x='sq_km', 
    y=selected_category, 
    hover_name='Country',
    labels={'sq_km': 'Country Size (sq km)', selected_category: f'{selected_category} Troops'},
    title=''
)

#Add labels (or flags) for these special countries
for i, row in special_countries.iterrows():
    fig.add_trace(
        go.Scatter(
            x=[row['sq_km']],
            y=[row[selected_category]],
            text=row['Country'],  # Label with the country name
            mode='markers+text',
            textposition='top center',
            marker=dict(size=12, color='red'),  # Customize marker appearance
            showlegend=False
        )
    )

#Display the Plotly chart in Streamlit
st.plotly_chart(fig)

st.text('Sources:')
st.text("1) Wikepedia, 'List of countries and dependencies by area',")
st.text("https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_area ")
st.text("2) Wikepedia, 'List of countries by number of military and paramilitary personnel',")
st.text("https://en.wikipedia.org/wiki/List_of_countries_by_number_of_military_and_paramilitary_personnel")


st.divider()

st.subheader('Data Analysis Tools Used')
st.markdown('**Dataset:** .csv file')
st.markdown('**Python:** create the basic script')
st.markdown('**Pandas: data manipulation')
st.markdown('**Plotly:** create the main visualization')
st.markdown('**Streamlit:** Python framework to share the script, e.g. web app')
st.markdown('**Github:** developer platform for hosting the script and data file')

