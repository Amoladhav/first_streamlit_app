from os import write
import streamlit
import requests
import pandas
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Diner')

streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocardo Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized

def get_fruit_load_list(snowflake_conn):
    With snowflake_conn.cursor() as my_cur:
        my_cur.execute("SELECT * FROM fruit_load_list")
        return my_cur.fetchall()


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt",)
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get infomation.")
    else:
        back_from_function = get_fruityvice_data(fruit_choice)
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()
        
streamlit.write('The user entered ', fruit_choice)


# don't run anythying
if streamlit.button('Get Fruit Load List'):
    snowflake_conn = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list(**snowflake_conn)
    streamlit.dataframe(my_data_rows)

# fruit2_choice = streamlit.text_input("What fruit would you like to add?", 'Kiwi')
# streamlit.write('Thanks for adding ', fruit2_choice)

# my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('from Streamlit');")