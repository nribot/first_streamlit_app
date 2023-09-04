import streamlit
import pandas
import snowflake.connector
import requests # lets us display the fruityvice api response
from urllib.error import URLError # error message handling



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

# create function to get fruityvice data
def get_fruityvice_data(this_fruit_choice):
  # get the data
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  # normalize the json to a table / df (normalize)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized 

streamlit.header("Fruityvice Fruit Advice!")

try: 
  # get fruit choice
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # displays the table to the screen
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")

# snowflake-related functions
# function to query the table
def get_fruit_load_list():
  with my cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

# add a button that calls our function and loads the data onto the page.
if streamlit.button('Get Fruit Load List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)


# get second fruit choice
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
streamlit.write('Thanks for adding ', add_my_fruit)

my_cur.execute("insert into fruit_load_list values ('from streamlit')")
