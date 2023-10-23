import streamlit as st
import pymysql
import pandas as pd

# Create a MySQL database connection
db_connection = pymysql.connect(
    host="localhost",
    user="root",
    password="kronos",
    database="project"
)

# Define keyword-to-specification mappings
keyword_mappings = {
    "gaming": {
        'Display_Size': ('>', 5.9),  # Display size greater than 5.9 inches
        'Battery': ('>', 5000),     # Battery capacity greater than 5000 mAh
        'Charging': ('>', 30),      # Fast charging support greater than 30W
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED'],
        'Refresh_Rate': ('>', 100),  # High refresh rate greater than 100 Hz
        'Storage': ('>', 200),      # Storage capacity greater than 200 GB
        'Memory': ('>', 6)         # RAM greater than 6 GB
    },
    "content": {
        'Display_Size': ('>', 5.9),
        'Compatible_networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Sound': ['Spatial Audio', 'Stereo Speakers'],
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED'],
        'Refresh_Rate': ('>', 50),
        'Battery': ('>', 5500)
    },
    "photography": {
        'Display_Size': ('>', 5.9),
        'Compatible_networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Refresh_Rate': ('>', 50),
        'Front_Camera': ('>', 10),  # Front camera resolution greater than 10 MP
        'Rear_Camera': ('>', 40),   # Rear camera resolution greater than 40 MP
        'Storage': ('>', 500)      # Storage capacity greater than 500 GB
    },
    "communication": {
        'Display_Size': ('>', 5.0),
        'Compatible_networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED'],
        'Refresh_Rate': ('>', 50),
        'Connectivity': 'Wi-Fi 6',  # Supports Wi-Fi 6
        'SIM': ['Dual SIM', 'eSIM']
    },
    "longevity": {
        'Display_Size': ('>', 5.0),
        'Compatible_networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED'],
        'Refresh_Rate': ('>', 50),
        'Connectivity': 'Wi-Fi 6',
        'SIM': ['Dual SIM', 'eSIM'],
        'Water_resistance': ['IP68', 'IP67', 'IPX4', 'IPX8'],
        'Release_Date': ['2023'],   # Released in 2023
        'OS': ['13', '17.2', '14']  # Supports specific OS versions
    }
}

# Function to filter and recommend smartphones
def recommend_smartphones(user_needs, user_price):
    # Process user input and extract relevant keywords
    user_keywords = []
    for keyword, criteria in keyword_mappings.items():
        if keyword in user_needs:
            user_keywords.append((keyword, criteria))

    # Fetch smartphone data from the MySQL database
    query = "SELECT * FROM smartphone_data"
    df = pd.read_sql(query, con=db_connection)

    # Filter the dataset based on extracted keywords, price constraint, and other criteria
    filtered_df = df.copy()
    for keyword, criteria in user_keywords:
        for feature, criterion in criteria.items():
            # Apply criteria based on the feature and criterion
            if feature == 'Display_Size':
                operator = criterion[0]
                threshold = float(criterion[1])
                if operator == '>':
                    filtered_df = filtered_df[filtered_df[feature] >= threshold]
                elif operator == '>=':
                    filtered_df = filtered_df[filtered_df[feature] >= threshold]
            # Add more criteria based on features as needed
            # ...

    # Apply the price constraint
    filtered_df = filtered_df[filtered_df['Price'] <= user_price]
    filtered_df['Price_Difference'] = abs(filtered_df['Price'] - user_price)
    filtered_df = filtered_df.sort_values(by='Price_Difference')

    # Recommend the top N smartphones based on the filtered dataset
    top_n = 3
    recommended_smartphones = filtered_df.head(top_n)
    recommended_smartphones = recommended_smartphones.reset_index(drop=True)
    return recommended_smartphones[['Manufacturer', 'Name', 'Price']]

st.title("Smartphone Recommendation System :phone:")
st.write("Select your use case criteria and budget:")

# Criteria selection
user_needs = st.multiselect("Choose what you want to do", keyword_mappings.keys())

# Budget input
user_price = st.slider("Budget (in Rupees)", min_value=0, max_value=200000, step=1000)

if st.button("Recommend"):
    if not user_needs:
        st.error("Please select at least one criteria.")
    else:
        recommendations = recommend_smartphones(user_needs, user_price)
        st.subheader("Recommended Smartphones")
        st.table(recommendations)
# Close the database connection
db_connection.close()