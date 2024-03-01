import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Function to handle API rate limit error


def handle_rate_limit_error():
    st.error("API rate limit exceeded. Please try again later.")


# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = "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"

# Initialize the OpenAI class
llm = OpenAI(temperature=0.6)

# Title and Dropdown for Food Genres
st.title("TastyByte")
food_genre = st.selectbox("Select a food genre", [
                          "Indian", "Mexican", "Italian", "Arabic", "American"])

# Generate Recommendation or Show Source Code based on user selection
if st.button("Generate Recommendation"):
    if food_genre:
        try:
            # Prompt Templates
            prompt_template_name = PromptTemplate(
                input_variables=['cuisine'],
                template='I want to open a restaurant for {cuisine} food. Suggest a fancy name for this.'
            )
            prompt_template_items = PromptTemplate(
                input_variables=['restaurant_name'],
                template='Suggest some menu items for {restaurant_name}. Return it as a comma separate list.'
            )

            # Initialize language model chains
            name_chain = LLMChain(
                llm=llm, prompt=prompt_template_name, output_key="restaurant_name")
            food_items_chain = LLMChain(
                llm=llm, prompt=prompt_template_items, output_key="menu_items")

            # Define a sequential chain
            chain = SequentialChain(chains=[name_chain, food_items_chain],
                                    input_variables=["cuisine"],
                                    output_variables=['restaurant_name', 'menu_items'])

            # Run the chain with input cuisine
            response = chain({'cuisine': food_genre})

            # Display recommendation
            st.header(
                f"Recommended Restaurant Name: {response['restaurant_name'].strip()}")
            st.subheader("Menu Items:")
            menu_items = response['menu_items'].strip().split(",")
            for item in menu_items:
                st.write("-", item)

        except Exception as e:
            # Handle API rate limit error
            if "RateLimitError" in str(e):
                handle_rate_limit_error()
            else:
                st.error(f"An error occurred: {e}")

# Display Source Code
if st.button("Show Source Code"):
    st.text("Source Code:")
    st.code("""
import os
import streamlit as st
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain

# Function to handle API rate limit error
def handle_rate_limit_error():
    st.error("API rate limit exceeded. Please try again later.")

# Set the OpenAI API key as an environment variable
os.environ["OPENAI_API_KEY"] = "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"

# Initialize the OpenAI class
llm = OpenAI(temperature=0.6)

# Title and Dropdown for Food Genres
st.title("TastyByte")
food_genre = st.selectbox("Select a food genre", ["Indian", "Mexican", "Italian", "Arabic", "American"])

# Generate Recommendation or Show Source Code based on user selection
if st.button("Generate Recommendation"):
    if food_genre:
        try:
            # Prompt Templates
            prompt_template_name = PromptTemplate(
                input_variables=['cuisine'],
                template='I want to open a restaurant for {cuisine} food. Suggest a fancy name for this.'
            )
            prompt_template_items = PromptTemplate(
                input_variables=['restaurant_name'],
                template='Suggest some menu items for {restaurant_name}. Return it as a comma separate list.'
            )

            # Initialize language model chains
            name_chain = LLMChain(llm=llm, prompt=prompt_template_name, output_key="restaurant_name")
            food_items_chain = LLMChain(llm=llm, prompt=prompt_template_items, output_key="menu_items")

            # Define a sequential chain
            chain = SequentialChain(chains=[name_chain, food_items_chain],
                                     input_variables=["cuisine"],
                                     output_variables=['restaurant_name', 'menu_items'])

            # Run the chain with input cuisine
            response = chain({'cuisine': food_genre})

            # Display recommendation
            st.header(f"Recommended Restaurant Name: {response['restaurant_name'].strip()}")
            st.subheader("Menu Items:")
            menu_items = response['menu_items'].strip().split(",")
            for item in menu_items:
                st.write("-", item)

        except Exception as e:
            # Handle API rate limit error
            if "RateLimitError" in str(e):
                handle_rate_limit_error()
            else:
                st.error(f"An error occurred: {e}")
    """)
