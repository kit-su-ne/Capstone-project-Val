import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="CPF Investment Simplified"
)
# endregion <--------- Streamlit App Configuration --------->

def method():
    st.title("Methodology")
    st.write("""
        This is a comprehensive explanation of the data flows and implementation details,/
        with a flowchart illustrating the process flow for each of the use cases in the application.
    """)

    st.header(":green[Password Protection Implementation]")
    st.write("""
        The `check_password()` function is implemented to secure access to the application.
        A text input field for password entry is displayed to the user, where the password input is configured to hide characters for security.
        
        The app uses Streamlit's session state to keep track of whether the correct password has been entered.
        If the password is correct, password_correct is set to True in the session state.
        The entered password is immediately deleted from the session state after verification for security.
        If the password check fails, the rest of the app content is not displayed.
    """)

    st.title(":one: :orange[CPF Investment Simplified Chatbot]")

    st.image("images/Chatbot Process Flowchart Diagram.png", caption="Process Flowchart Diagram")

    st.header(":orange[Data Collection and Processing]",divider="orange")
    st.write("""
        The application uses web scraping techniques to gather information from two primary sources: 1) CPF website, 2) Singapore Statutes Online (SSO)
        
        Web scraping is implemented using Selenium WebDriver in headless mode, as the sites uses javascript, combined with BeautifulSoup for HTML parsing.
        The scraping process targets specific CSS classes to extract relevant content from each webpage.
        Scraped data is then stored in JSON format for easy retrieval and processing.
        
        Additional static data about instruments that can be invested under CPFIS (saved as WhatCan_data) is manually curated
         and stored in a dictionary, as the format online is difficult to parse from its original PDF format.
        Additional information on links to check out were manually added so that users can visit the sites on their own.
    """)

    st.header(":orange[Implementation]", divider="orange")
    st.write("""
        Scraped data is saved in JSON files: 1) 'CPF_scraped_data.json' for CPF website data, 2)'SSO_scraped_data.json' for Singapore Statutes Online data
             
        The load_data() function retrieves the stored JSON data and the static WhatCan_data each time a user query is processed,
         ensuring the most up-to-date information is used.
    """)

    st.subheader(":orange[Query Processing Pipeline]")
    st.write("""
        When a user submits a query, the `process_user_message()` function is called. This function loads the latest data 
        and passes it to `generate_response_for_user()`. The response generation process includes:
        - **System Message**: Defines the AI assistant's role and behavior.
        - **User's Query**: The specific input provided by the user.
        - **Structured Instructions**: Ensures responses follow a step-by-step approach to reduce hallucinations and ensure clarity.
    """)

    st.subheader(":orange[Language Model Integration]")
    st.write("""
        The app uses OpenAI's "gpt-4o-mini" model. The `get_completion_by_messages()` function makes the API call to generate responses.
    """)

    st.subheader(":orange[Response Generation Process]")
    st.write("""
        The chatbot generates responses with the following approach:
        -  **Information Retrieval**:
        1. Searches for relevant data in the CPF dataset.
        2. If necessary, supplements with information from the SSO dataset.
        -  **Answer Formulation**:
        3. Constructs an answer based on retrieved data.
        4. Formats the response for clarity, factual accuracy, and helpful tone.
        - **Citation and Disclaimer**: Cites information sources and includes a disclaimer about the educational nature of the information.
    """)


    st.title(":two: :blue[CPFIS-Approved Investment (UTs and ILPs)]")
    st.write("""
        The app visualizes CPF Investment Scheme (CPFIS) options by processing official PDF data for Unit Trusts (UTs) and 
        Investment-Linked Products (ILPs). Filters allow users to check for the appropriate funds based on their risk appetite.
    """)

    st.image("images/Filter Process Flowchart Diagram.png", caption="Process Flowchart Diagram")

    st.header(":blue[Data Collection and Processing]",divider="blue")
    st.write("""
        The application downloads PDF documents containing CPFIS data, using `pdfplumber`, the `extract_and_segregate_tables()` function:
        - Extracts text and tables from each PDF page.
        - Identify different sections within the PDF based on predefined section titles, as one of the files had more than one instrument within.
        - Segregate table data into appropriate sections.
    """)

    st.subheader(":blue[Data Cleaning and Structuring]")
    st.write("""
        The `clean_table_data()` function performs several cleaning operations:
        - Strips whitespace from columns.
        - Removes rows with non-numeric serial numbers.
        - Standardizes column names and converts numeric values.
        - Parses complex fields like 'Risk Class' into individual columns.
        - Extracts CPFIS OA/SA eligibility into separate columns.
        
        Cleaned data is saved in JSON format, organized by UTs and ILPs sections.
    """)

    st.header(":blue[Implementation]", divider="blue")
    st.write("""
        Scraped data is saved in JSON files: 1) 'CPF_ILPs_List_A_Funds_-Investment_Linked_Products.json' for ILPs,
        2) 'CPF_UTs_List_A_Funds_-_only_for_Investment_-Linked_Insurance_Policies_to_feed_into.json' and 'CPF_UTs_List_A_Funds_-Unit_Trusts.json' for UTs
             
        The `load_data1()` function retrieves the stored JSON datasets. Filtered data is displayed using Streamlit's dataframe() function.
    """)

    st.subheader(":blue[Streamlit Application Interface]")
    st.write("""
        The main Streamlit app processes both UTs and ILPs data for interactive visualization. Each section has dropdown filters 
        for:
        - **Risk Level**
        - **Focus/Scope**
        - **Geographical Area**
        - **Sector Focus**
        
        A simple explanation is provided for the filters. Users can then refine the data displayed by adjusting filters, which dynamically updates the table without reprocessing PDFs.
    """)


if __name__ == "__main__":
    method()