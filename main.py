import json

import streamlit as st
import pandas as pd
import numpy as np
import requests
import streamlit.components.v1 as components

st.set_page_config(
    page_title="All-In-One Food",
    menu_items={"About": "Developed by Kaden Furigay"},
    layout="wide",
    initial_sidebar_state="collapsed"
)

api_key = "8fb0081bddf149a2b32bb6de769d19ae"

def get_nutrition_table(item_id):
    url = (f"https://api.spoonacular.com/recipes/{item_id}/nutritionWidget.json?apiKey={api_key}")
    nutrition_data = requests.get(url).json()
    nutrition_df = pd.DataFrame(nutrition_data["nutrients"])
    st.dataframe(nutrition_df)


def get_nutrition_chart(item_id):
    url = (f"https://api.spoonacular.com/recipes/{item_id}/nutritionWidget.json?apiKey={api_key}")
    nutrition_data = requests.get(url).json()
    nutrition_df = pd.DataFrame(nutrition_data["nutrients"])
    st.bar_chart(nutrition_df.set_index("name")["percentOfDailyNeeds"])

def get_nutrition_lineChart(item_id):
    url = (f"https://api.spoonacular.com/recipes/{item_id}/nutritionWidget.json?apiKey={api_key}")
    nutrition_data = requests.get(url).json()
    nutrition_df = pd.DataFrame(nutrition_data["nutrients"])
    st.line_chart(nutrition_df.set_index("name")["percentOfDailyNeeds"])

page = st.sidebar.selectbox("Select an option", ["📋 Homepage","🥗 Search for recipe", "🥘 Generate meal plan",
                                                 "🥡 Search for restaurant"])

if page:
    st.sidebar.success('You have selected "' + page + '"')
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("Are you satisfied with our services?")
    yes_opt = st.sidebar.checkbox("Yes")
    no_opt = st.sidebar.checkbox("No")
    if yes_opt:
        st.sidebar.info("We're glad to hear that. We hope you continue to have fun using All-In-One Food Stop!")
    elif no_opt:
        st.sidebar.text_input("Please let us know what we can do to improve our webpage!")

# --- Homepage starts ---
if page == "📋 Homepage":
    with st.container():
        left_column, right_column = st.columns(2)
        with left_column:
            st.title("All-In-One Food Stop!")
            st.write("We understand the pain of finding the next meal to eat. "
                     "Using our website you'll be able to customize a meal plan, find a specific recipe, or "
                     "if you're feeling lazy, you can find yourself a restaurant!")
            st.write("")
            st.write("")
            st.write("")
            st.write("On your right hand side, please complete a tiny questionnaire to see which option that we offer"
                     " fits your needs the best!")
            st.write("Just pick yes or no for the questions and do not think too hard about it! ")
            st.write("")
            st.subheader("Here are some reviews:")
            st.info("This webpage is a life-saver when it comes to last minute meals!"
                    "\n   - Andrea Scholz ⭐⭐⭐⭐⭐" )
            st.info("I love that we are able to customize meal plans and restaurants to our needs!"
                    "\n   - Rachel Mendez ⭐⭐⭐⭐⭐")


        with right_column:
            st.image("images/stock food.jpg", width= 310)
            st.write("")
            restrictions = st.radio("Do you have any dietary restrictions?", ["Yes", "No"], index= None, horizontal=1)
            eat_out = st.radio("Do you like to eat out a lot?", ["Yes", "No"], index= None, horizontal=1)
            time = st.radio("Do you have time to cook your meals?", ["Yes", "No"], index=None, horizontal=1)
            planning = st.radio("Do you like to plan ahead?", ["Yes", "No"], index=None, horizontal=1)
            urgent = st.radio("Do you need a meal recipe now?", ["Yes", "No"], index=None, horizontal=1)
            if restrictions and eat_out and time and planning and urgent:
                if restrictions == "Yes" and eat_out == "No":
                    st.success('Open the sidebar on the left-hand side of your screen, '
                               'select "🥗 Search for recipe" or "🥘 Generate meal plan"')
                elif urgent == "Yes" and planning == "Yes":
                    st.success('Using the sidebar on the left-hand side of your screen, '
                               'select "🥗 Search for recipe" or "🥘 Generate meal plan"')
                elif eat_out == "Yes" or time == "No":
                    st.success('Using the sidebar on the left-hand side of your screen, '
                               'select "Search for restaurant"')


    st.write("")
    st.write("")

    st.subheader("Examples of recipes offered:")
    tab1, tab2, tab3 = st.tabs(["Sweet & Salty Granola Bars", "Panera Spicy Thai Salad", "Beef Tataki"])

    with tab1:
        st.write(
            f'<iframe src="https://spoonacular.com/sweet-salty-granola-bars-662416" width = 950 height = 900 ></iframe>',
            unsafe_allow_html=True,
        )

    with tab2:
        st.write(
            f'<iframe src="https://spoonacular.com/panera-spicy-thai-salad-1697535" width = 950 height = 900 ></iframe>',
            unsafe_allow_html=True,
        )

    with tab3:
        st.write(
            f'<iframe src="https://spoonacular.com/beef-tataki-634698" width = 950 height = 900 ></iframe>',
            unsafe_allow_html=True,
        )
# --- Homepage ends ---


# --- Search for recipe page starts ---
elif page == "🥗 Search for recipe":
    st.title("Search for your next meal!")
    st.subheader("Use any of the following filters to find the right meal for you")
    cuisine = st.selectbox("Select a cuisine",
                           ["","African", "Asian", "American", "British", "Cajun", "Caribbean", "Chinese",
                            "Eastern European", "European", "French", "German", "Greek", "Indian", "Irish", "Italian",
                            "Japanese", "Jewish",
                            "Korean", "Latin American", "Mediterranean", "Mexican", "Middle Eastern",
                            "Nordic", "Southern", "Spanish", "Thai", "Vietnamese"])
    cuisine.lower()

    diet = st.selectbox("Do you have a diet preference?",
                        ["", "Gluten Free", "Ketogenic", "Vegetarian", "Lacto-Vegetarian",
                         "Ovo-Vegetarian", "Vegan", "Pescetarian", "Paleo", "Primal",
                         "Low FODMAP", "Whole30"])

    intolerances = st.selectbox("Do you have any intolerances?",[" ","Dairy", "Egg", "Gluten","Grain", "Peanut", "Seafood",
                                                                 "Sesame", "Shellfish", "Soy", "Sulfite", "Tree Nut", "Wheat"])
    calorie_min = st.slider("Calorie Amount (minimum)", min_value=20, max_value=1500)
    calorie_max = st.slider("Calorie Amount (maximum)", min_value=20, max_value=1500)

    url = (f"https://api.spoonacular.com/recipes/complexSearch?apiKey={api_key}&cuisine={cuisine}&diet={diet}&"
           f"intolerances={intolerances}&minCalories={calorie_min}&maxCalories={calorie_max}&number=20")
    recipe_list = requests.get(url).json()


    def find_recipe_list(start, end):
        counter = start
        for recipe in recipe_list["results"]:
            st.write("---")
            with st.container():
                left_column, right_column = st.columns(2)
                with left_column:
                    recipe_name = recipe_list["results"][counter]["title"]
                    recipe_image = recipe_list["results"][counter]["image"]
                    recipe_id = recipe_list["results"][counter]["id"]
                    recipe_url = (f" https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={api_key}")
                    get_recipe = requests.get(recipe_url).json()
                    recipe_url = get_recipe["spoonacularSourceUrl"]
                    st.subheader(recipe_name)
                    st.image(recipe_image, width=300)
                    st.link_button("Go to recipe!", recipe_url)
                with right_column:
                    get_nutrition_table(recipe_id)
            if counter == end:
                break
            counter += 1

    if recipe_list["totalResults"] == 0:
        st.warning("Please select different parameters.")
    elif recipe_list["totalResults"] >= 10:
        st.info("Results:")
        tab1, tab2 = st.tabs(["1-10", "11-20"])

        with tab1:

            find_recipe_list(0, 9)

        with tab2:

            find_recipe_list( 10,19)
    else:
        find_recipe_list(0,9)

# --- Search for recipe page ends ---


# --- Generate meal plan page starts ---
elif page == "🥘 Generate meal plan":
    st.title("Personalize your food!")
    duration = st.radio("How long is this meal plan?", ["One day", "One week"],
                        captions=["sometimes we need to take it day by day!", "planning ahead is a great idea!"])
    target_calories = st.slider("Target Calories (for one day)", min_value= 1200, max_value=3000)
    diet = st.selectbox("Do you have a diet preference?", ["","Gluten Free", "Ketogenic", "Vegetarian", "Lacto-Vegetarian",
                                                           "Ovo-Vegetarian", "Vegan", "Pescetarian", "Paleo", "Primal",
                                                           "Low FODMAP", "Whole30"])
    diet_restrictions = st.text_input("Do you have any dietary restrictions? (separate using comma)",
                                      "Ex: shellfish, olives")
    st.success('Your meal plan has been successfully generated')


    # if option "One day" is chosen
    if duration == "One day":
        # receive results from API
        duration = "day"
        url = (f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key}&timeFrame={duration}"
               f"&targetCalories={target_calories}&diet={diet}&exclude={diet_restrictions}")
        meal_list = requests.get(url).json()
        
        # create columns for meal_list results
        counter = 0
        for recipe in meal_list["meals"]:
            with st.container():
                left_column, right_column = st.columns(2)

                with left_column:
                    st.write("---")
                    recipe_name = meal_list["meals"][counter]["title"]
                    recipe_ID = meal_list["meals"][counter]["id"]
                    st.subheader(recipe_name)
                    st.image(f"https://spoonacular.com/recipeImages/{recipe_ID}-556x370.jpg", width=200, )

                    meal_URL = meal_list["meals"][counter]["sourceUrl"]
                    st.link_button("Go to recipe!", meal_URL)

            with right_column:
                st.write("")
                st.write(" ")
                tab1, tab2 =st.tabs(["Nutrient Facts", "Percentage of Nutrients"])
                with tab1:
                    st.info("These are the following nutrient facts:")
                    get_nutrition_table(recipe_ID)
                with tab2:
                    st.info("Percentage of nutrient that we need daily:")
                    get_nutrition_chart(recipe_ID)


            counter += 1


    # if option "One week" is chosen
    elif duration == "One week":
        duration = "week"
        url = (f"https://api.spoonacular.com/mealplanner/generate?apiKey={api_key}&timeFrame={duration}"
               f"&targetCalories={target_calories}&diet={diet}&exclude={diet_restrictions}")
        meal_list = requests.get(url).json()
        
        with st.container():
            left_column, right_column = st.columns(2)
            counter = 0
        for day in meal_list["week"]:
            with left_column:
                st.header(day.capitalize())
                for meal in meal_list["week"][day]["meals"]:
                    recipe_name = meal_list["week"][day]["meals"][counter]["title"]
                    recipe_ID = meal_list["week"][day]["meals"][counter]["id"]
                    st.subheader(meal_list["week"][day]["meals"][counter]["title"])
                    st.image(f"https://spoonacular.com/recipeImages/{recipe_ID}-556x370.jpg", width=200, )
                    st.write(meal_list["week"][day]["meals"][counter]["sourceUrl"])

                    st.write("---")
                    if counter == 2:
                        counter = 0
                    counter += 1
            with right_column:
                get_nutrition_table(recipe_ID)
# --- Generate meal plan page ends ---



# --- Search for restaurant page starts ---
elif page == "🥡 Search for restaurant":

    st.title("Find a restaurant to eat at!")
    st.subheader("Enter your coordinates and cuisine preference for restaurants near you!")
    latitude = st.number_input("Insert your latitude", min_value=-90.01, max_value=90.01, step= 0.01, value=37.7749)
    longitude = st.number_input("Insert your longitude", min_value=-180.01, max_value=180.01, step= 0.01, value=-122.4194)
    cuisine = st.selectbox("Select a cuisine", ["African","Asian","American", "British", "Cajun", "Caribbean", "Chinese",
                                                "Eastern European", "European", "French", "German","Greek", "Indian",
                                                "Irish","Italian","Japanese", "Jewish","Korean", "Latin American",
                                                "Mediterranean", "Mexican", "Middle Eastern","Nordic", "Southern",
                                                "Spanish", "Thai", "Vietnamese"])

    distance = st.slider("Distance (miles)", 0 , 50, 5)
    rating = st.radio("Minimum rating (1-5 stars)", [0, 1, 2, 3, 4, 5], index= 3, horizontal=1 )
    sort = st.selectbox("Choose an option", ["relevance","cheapest", "fastest", "rating", "distance"])
    url = (f"https://api.spoonacular.com/food/restaurants/search?apiKey={api_key}&lat={latitude}&lng={longitude}"
           f"&cuisine={cuisine.lower()}&distance={distance}&min-rating={rating}&sort={sort}")
    restaurant_list = requests.get(url).json()

    counter = 0
    try:
        for restaurant in restaurant_list["restaurants"][counter]:
            restaurant_name = restaurant_list["restaurants"][counter]["name"]
            restaurant_address = (restaurant_list["restaurants"][counter]["address"]["street_addr"]
                                  + " " + restaurant_list["restaurants"][counter]["address"]["state"]+ ", "
                                  + restaurant_list["restaurants"][counter]["address"]["country"] + " "
                                  + restaurant_list["restaurants"][counter]["address"]["zipcode"])
            restaurant_lat = restaurant_list["restaurants"][counter]["address"]["lat"]
            restaurant_long = restaurant_list["restaurants"][counter]["address"]["longitude"]
            restaurant_foodIMG = restaurant_list["restaurants"][counter]["food_photos"][0]
            with st.container():
                st.write("---")
                left_column, right_column = st.columns(2)
                with left_column:
                    st.subheader(restaurant_name)
                    st.write(restaurant_address)
                    st.image(restaurant_foodIMG, width=350)

                with right_column:
                    df = pd.DataFrame({
                        "col1": restaurant_lat,
                        "col2": restaurant_long,
                        "col3": np.random.rand(1000, 4).tolist(),
                    })

                    st.map(df,
                           latitude='col1',
                           longitude='col2',
                           color='col3',
                           use_container_width = True)
            counter += 1
    except IndexError as e:
        st.info("You have reached the end of the results.")


                




# --- Search for restaurant page ends ---





