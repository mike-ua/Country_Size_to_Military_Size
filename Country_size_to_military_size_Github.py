import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go  # Import graph objects (go) from plotly

st.subheader("Comparison of Country size (in sq. km) to Military size")

#Load data from the COMBINED .csv file
df = pd.read_csv('https://github.com/mike-ua/Streamlit-Data/blob/950c1c715785bd84c6bbcd9f9c98803bf9de4b2b/Country_Military_Size_August_2024.csv?raw=true')


#Clean column names to avoid issues with spaces or case sensitivity
df.columns = df.columns.str.strip()

#Define a mapping of countries to REGIONS
region_mapping = {
    'N. America': [
        'Antigua_and_Barbuda', 'Bahamas', 'Barbados', 'Belize', 'Canada',
        'Costa_Rica', 'Cuba', 'Dominican_Republic', 'El_Salvador', 'Guatemala',
        'Haiti', 'Honduras', 'Jamaica', 'Mexico', 'Nicaragua', 'Panama',
        'Trinidad_and_Tobago', 'UnitedStates_PuertoRico_Guam'
    ],
    'S. America': [
        'Argentina', 'Bolivia', 'Brazil', 'Chile', 'Colombia', 'Ecuador',
        'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela'
    ],
    'Europe': [
        'Albania', 'Austria', 'Belarus', 'Belgium', 'Bosnia_and_Herzegovina',
        'Bulgaria', 'Croatia', 'Czech_Republic', 'Denmark_Greenland_Faroe',
        'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
        'Ireland', 'Italy', 'Kosovo', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta',
        'Moldova', 'Montenegro', 'Netherlands', 'North_Macedonia', 'Norway',
        'Poland', 'Portugal', 'Romania', 'Russia', 'Serbia', 'Slovakia',
        'Slovenia', 'Spain', 'Sweden', 'Switzerland', 'Ukraine',
        'UnitedKingdom_Falkland_IsleofMan', 'Vatican_City'
    ],
    'Africa': [
        'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina_Faso', 'Burundi',
        'Cape_Verde', 'Central_African_Republic', 'Chad', 'Dem_Rep_of_Congo',
        'Djibouti', 'Egypt', 'Equatorial_Guinea', 'Eritrea', 'Ethiopia', 'Gabon',
        'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory_Coast', 'Kenya',
        'Lesotho', 'Liberia', 'Madagascar', 'Malawi', 'Mali', 'Mauritania',
        'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria',
        'Republic_of_the_Congo', 'Rwanda', 'Senegal', 'Seychelles', 'Sierra_Leone',
        'Somalia', 'South_Africa', 'South_Sudan', 'Sudan', 'Tanzania', 'Togo',
        'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
    ],
    'Middle East': [
        'Armenia', 'Azerbaijan', 'Bahrain', 'Cyprus', 'Georgia', 'Iran', 'Iraq',
        'Israel', 'Jordan', 'Kuwait', 'Lebanon', 'Oman', 'Qatar', 'Saudi_Arabia',
        'Syria', 'Turkey', 'United_Arab_Emirates', 'Yemen'
    ],
    'Asia': [
        'Afghanistan', 'Australia', 'Bangladesh', 'Bhutan', 'Brunei', 'Cambodia',
        'China', 'East_Timor', 'Fiji', 'India', 'Indonesia', 'Japan', 'Kazakhstan',
        'Kyrgyzstan', 'Laos', 'Malaysia', 'Maldives', 'Mongolia', 'Myanmar',
        'Nepal', 'New_Zealand', 'North_Korea', 'Pakistan', 'Papua_New_Guinea',
        'Philippines', 'Singapore', 'South_Korea', 'Sri_Lanka', 'Taiwan',
        'Tajikistan', 'Thailand', 'Turkmenistan', 'Uzbekistan', 'Vanuatu',
        'Vietnam'
    ]
}

#Sidebar - User input
region_list = list(region_mapping.keys())
region_list.insert(0, "None")  # Add a "None" option

selected_region = st.sidebar.selectbox(
    "Select Region (optional)", 
    region_list
)

country_list = df['Country'].unique().tolist()
country_list.insert(0, "All")

selected_countries = st.sidebar.multiselect(
    "Select Countries", 
    country_list
)

#Filter data based on region and country selection
if selected_region != "None":
    countries_in_region = region_mapping[selected_region]
    filtered_df = df[df['Country'].isin(countries_in_region)]
else:
    filtered_df = df[df['Country'].isin(selected_countries)]

#If "All" is selected, include all countries
if "All" in selected_countries:
    filtered_df = df

selected_category = st.sidebar.radio(
    "Select Military Category", 
    ['Active_Military', 'Reserve_Military', 'Paramilitary', 'Total']
)

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
    title=f'Size of Country vs {selected_category}'
)

#Add labels (or flags, maybe) for these special countries
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

#Display the Plotly figure in Streamlit
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
st.markdown('**Pandas:** data manipulation')
st.markdown('**Plotly:** create the main visualization')
st.markdown('**Streamlit:** Python framework to share the script, e.g. web app')
st.markdown('**Github:** developer platform for hosting the script and data file')

