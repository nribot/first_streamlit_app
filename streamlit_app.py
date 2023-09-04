import streamlit
# display text
streamlit.title('My Parents New Healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


# DISPLAY FRUIT TABLE PICKER

# import fruit table data
import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# set index by fruit name
my_fruit_list = my_fruit_list.set_index('Fruit')

# display fruit pick list first so customers can pick the fruit they want to include (default fruits)
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])

# only show selected fruits
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display fruit table
streamlit.dataframe(fruits_to_show)


# DISPLAY FRUITYVICE API RESPONSE

# we import a python package that lets us display the fruityvice api response
import requests

streamlit.header("Fruityvice Fruit Advice!")

# get fruit choice
fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

# get the data
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# write text to the screen
#streamlit.text(fruityvice_response.json())

# normalize the json to a table / df (normalize)
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# displays the table to the screen
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

