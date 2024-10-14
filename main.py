import streamlit as st
import pandas as pd
import os
import json
import openai
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import hmac

import requests
import pdfplumber
import re
from io import BytesIO

from helper_functions.utility import check_password
from logics.files_download import scrape_and_save_data, load_data, load_data1

# Load environment variables (if any)
load_dotenv()

# Check password at the start
if not check_password():  
    st.stop()

# Streamlit App Configuration
st.set_page_config(
    layout="centered",
    page_title="CPF Investment Simplified",
    initial_sidebar_state="expanded"
)

st.title(":blue[CPF Investment Simplified]")
st.write('''
             CPF (Central Provident Fund) is Singapore's comprehensive social security system.
             It is a mandatory savings scheme where both employees and employers contribute a portion of the employee's monthly salary.
             These funds are allocated to different accounts for retirement, healthcare, and housing needs.
         
             CPFIS (CPF Investment Scheme) is an extension of CPF that allows members to invest their CPF savings in various financial products \
             like stocks, bonds, and unit trusts to potentially earn higher returns. However, this comes with investment risks.
             
            The application consolidates information from official sources, offers simplified explanations of the scheme, and presents investment options \
             (unit trusts (UTs) and investment-linked insurance products (ILPs) at the moment) in a clear, user-friendly manner.
             '''
)

#Mandatory disclaimer
with st.expander("Disclaimer"):
    st.write("""
        **IMPORTANT NOTICE**: This web application is a prototype developed for **educational purposes only**.
        The information provided here is **NOT intended for real-world usage** and should not be relied upon for making any decisions,
        especially those related to financial, legal, or healthcare matters.
             
        **Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.**
        
        Always consult with qualified professionals for accurate and personalized advice.
    """)

# Sidebar for API Key input
OPENAI_Key = st.sidebar.text_input("OpenAI API Key", type="password")

if not OPENAI_Key:
        st.info("Please add your OpenAI API key to continue.")

# Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_Key)

# Sidebar for selection between Chatbot and Investment Filtering
action = st.sidebar.selectbox("Choose your action", ["CPFIS Chatbot", "Investment Filtering (Unit Trusts & ILPs)"])

#******************Use Case 1***************************
# Load environment variables
load_dotenv()

def get_embedding(input, model='text-embedding-3-small'):
    response = client.embeddings.create(
        input=input,
        model=model
    )
    return [x.embedding for x in response.data]


# This is the "Updated" helper function for calling LLM
def get_completion(prompt, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1, json_output=False):
    if json_output == True:
      output_json_structure = {"type": "json_object"}
    else:
      output_json_structure = None

    messages = [{"role": "user", "content": prompt}]
    try:
        response = client.chat.completions.create( 
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            max_tokens=max_tokens,
            n=1,
            response_format=output_json_structure,
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None  # Return None in case of error
    
    return response.choices[0].message.content


# Note that this function directly take in "messages" as the parameter.
def get_completion_by_messages(messages, model="gpt-4o-mini", temperature=0, top_p=1.0, max_tokens=1024, n=1):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
        n=1
    )
    return response.choices[0].message.content

# Step 2: Generate Response Based on CPF Policy Details
def generate_response_for_user(user_input, WhatCan_data, CPF_scraped_data, SSO_scraped_data):
    delimiter = "####"
   
    # Define response system message
    system_message = f"""
        You are an AI assistant providing detailed responses to questions on the CPF Investment Scheme (CPFIS). 
        Respond exclusively using information from the CPF and Singapore Statutes Online (SSO) documents provided below. 
        Cite sources precisely without additional commentary, using this format: ({{'source': ..., 'URL': ...}}).
        Include specific portions of the documents relevant to each response. 

        When unsure of an answer, inform the user of the lack of available information rather than making assumptions.

        Follow these structured steps to answer user queries. Each query will be delimited by a pair of {delimiter} markers.

        Step 1:{delimiter} Locate relevant data from the CPF dataset for the user’s query:
        {WhatCan_data, CPF_scraped_data}

        Step 2:{delimiter} If relevant information isn't found in Step 1, retrieve supplementary information from the SSO dataset:
        {SSO_scraped_data}

        Step 3:{delimiter} Using the identified information, construct a response strictly based on the content found in these sources.
        Avoid making financial recommendations, and focus on providing clear and helpful explanations.

        Step 4:{delimiter} Present the answer to the user in an informative and supportive tone. Ensure all statements are accurate, fact-based, and easy to understand.

        - **End each response** with the source citations using the specified format, and add this standard disclaimer: 
        "This information is for educational purposes only. Please refer to official sources for the most current and accurate information."

        Use the following structured output format for clarity:

        - Step 1:{delimiter} <Step 1 retrieval>
        - Step 2:{delimiter} <Step 2 retrieval>
        - Step 3:{delimiter} <Step 3 reasoning and response development>
        - Step 4:{delimiter} <Final response to user>

        Ensure every step is separated by {delimiter} for clear readability.
    """

    messages =  [
        {'role':'system',
         'content': system_message},
        {'role':'user',
         'content': f"{delimiter}{user_input}{delimiter}"},
    ]

    response_to_customer = get_completion_by_messages(messages)
    response_to_customer = response_to_customer.split(delimiter)[-1]
    return response_to_customer

# Chatbot Functionality
def run_chatbot():
    st.title(":orange[CPF Investment Simplified Chatbot] :loudspeaker:")
    if st.button("Scrape Data"):
        scraped_data = scrape_and_save_data()
        st.success("Data scraped and saved successfully.")

    user_input = st.text_area("Type your question:")
    if st.button("Get Answer"):
        if user_input:
            WhatCan_data, CPF_scraped_data, SSO_scraped_data = load_data()
            
            # Generate response
            answer = generate_response_for_user(user_input, WhatCan_data, CPF_scraped_data, SSO_scraped_data)
            #answer = get_completion(user_input)
            st.write(answer)
        else:
            st.warning("Please enter a prompt.")
#******************Use Case 1***************************

#******************Use Case 2***************************
def run_investment_filtering():
    st.title(":orange[CPFIS-Approved Investment (UTs and ILPs)] :heavy_dollar_sign:")

    # Define the file paths and display titles for each data source
    data_sources = {
        "Unit Trusts": "CPF_UTs_List_A_Funds_-_Unit_Trusts.json",
        "Unit Trusts: Only for Investment-Linked Insurance Policies to feed into" : "CPF_UTs_List_A_Funds_-_only_for_Investment_-_Linked_Insurance_Policies_to_feed_into.json",
        "Investment-Linked Insurance Products (ILPs)": "CPF_ILPs_List_A_Funds_-_Investment_Linked_Products.json",
    }

    st.header(":gray[Filter Notes]", divider="gray")
    st.write("""
             :exclamation: **Risk Level** :exclamation: : Potential for loss or volatility in the investment's value.

             :eyeglasses: **Focus/Scope** :eyeglasses: : Indicates how diversified the investment is, whether narrow or broad.

             :world_map: **Geographical Area**:world_map: : Shows where the investment is primarily focused. 'NA' means it's not limited to any specific region.

             :factory: **Sector Focus** :factory: : Specifies if the investment targets a specific industry. 'NA' means it's diversified across multiple sectors.
    """)

    # Filter criteria
    filter_columns = ["Risk Level", "Focus/Scope", "Geographical Area", "Sector Focus"]

    # Loop through each data source and visualize it
    for title, filename in data_sources.items():
        st.header(f"{title}")
        
        # Load the data
        df = load_data1(filename)
        if df is not None:
            # Display filtering options for each column
            filters = {}
            cols = st.columns(4)
            for i, col in enumerate(filter_columns):
                unique_values = df[col].dropna().unique()
                filters[col] = cols[i].multiselect(
                    f"{col}:", options=unique_values, key=f"{col}_{title}"
                )

            # Apply filters
            filtered_df = df.copy()
            for col, values in filters.items():
                if values:
                    filtered_df = filtered_df[filtered_df[col].isin(values)]

            # Display the filtered data
            st.dataframe(filtered_df)

#******************Use Case 2***************************

# Call the function based on selected action
if __name__ == "__main__":
    if action == "CPFIS Chatbot":
        run_chatbot()
    else:
        run_investment_filtering()
