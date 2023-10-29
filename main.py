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

# Define keyword-to-specification mappings for different use cases
keyword_mappings = {
    "gaming": {
        'Display_Size': ('>', 5.9),
        'Battery': ('>', 5000),
        'Charging': ('>', 30),
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED'],
        'Refresh_Rate': ('>', 100),
        'Storage': ('>', 200),
        'Memory': ('>', 6)
    },
    "content": {
        'Display_Size': ('>', 5.9),
        'Compatible_Networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Sound': ['Spatial Audio', 'Stereo Speakers'],
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED'],
        'Refresh_Rate': ('>', 50),
        'Battery': ('>', 4400)
    },
    "photography": {
        'Display_Size': ('>', 5.9),
        'Compatible_Networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Refresh_Rate': ('>', 50),
        'Front_Camera': ('>', 10),
        'Rear_Camera': ('>', 40),
        'Storage': ('>', 500)
    },
    "communication": {
        'Display_Size': ('>', 5.0),
        'Compatible_Networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED','IPS LCD'],
        'Refresh_Rate': ('>', 50),
        'SIM': ['Dual SIM', 'eSIM']
    },
    "longevity": {
        'Display_Size': ('>', 5.0),
        'Compatible_Networks': '2G / 3G / 4G LTE / 5G',
        'Memory': ('>', 5),
        'Display_Type': ['AMOLED', 'SUPER AMOLED', 'OLED', 'Super Retina XDR OLED'],
        'Refresh_Rate': ('>', 50),
        'SIM': ['Dual SIM', 'eSIM'],
        'Water_resistance': ['IP68', 'IP67', 'IPX4', 'IPX8'],
    }
}

# Function to filter and recommend smartphones
def recommend_smartphones(user_needs, user_price):
    selected_category = None

    for keyword, _ in keyword_mappings.items():
        if keyword in user_needs:
            selected_category = keyword
            break

    if selected_category:
        query = "SELECT * FROM smartphone_data WHERE "
        criteria = keyword_mappings[selected_category]

        for feature, criterion in criteria.items():
            if isinstance(criterion, tuple):
                if criterion[0] == '>':
                    query += f"{feature} >= {float(criterion[1])} AND "
                elif criterion[0] == '>=':
                    query += f"{feature} >= {float(criterion[1])} AND "
            elif isinstance(criterion, list):
                values = ', '.join([f"'{val}'" for val in criterion])
                query += f"{feature} IN ({values}) AND "
            else:
                query += f"{feature} = '{criterion}' AND "

        query = query[:-4]  # Removing the trailing "AND"

        query += f"AND Price <= {user_price} ORDER BY ABS(Price - {user_price}) LIMIT 3"

        df = pd.read_sql(query, con=db_connection)

        return df[['Manufacturer', 'Name', 'Price']]
    else:
        return None

st.title("Smartphone Recommendation System :phone:")
st.write("Select your use case criteria and budget:")

user_needs = st.multiselect("Choose what you want to do", keyword_mappings.keys())
user_price = st.slider("Budget (in Rupees)", min_value=0, max_value=200000, step=1000)

if st.button("Recommend"):
    if not user_needs:
        st.error("Please select at least one criteria.")
    else:
        recommendations = recommend_smartphones(user_needs, user_price)
        if recommendations is not None:
            st.subheader("Recommended Smartphones")
            st.table(recommendations)
        else:
            st.write("No suitable recommendation based on the selected categories.")

db_connection.close()
