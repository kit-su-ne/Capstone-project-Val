import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="CPF Investment Simplified"
)
# endregion <--------- Streamlit App Configuration --------->

def about():
    st.title("About This Project")
    
    with st.expander("Source Code"):
        st.write("""
        [GitHub](https://github.com/kit-su-ne/Capstone-project-Val)
        """)

    st.header(":large_orange_circle: :orange[Project Scope]")
    st.write("""
        This project aims to develop an application that provides information and interactive tools related to the CPF Investment Scheme (CPFIS). 
        The application consolidates information from official sources, offers simplified explanations of the scheme in a clear, user-friendly manner.
        
        This application serves also to make CPFIS investment options (unit trusts (UTs) and investment-linked insurance products (ILPs) at the moment)
        interactive by allowing users to filter by criteria, whereas the original documents are in PDF format.
    """)
    
    st.header(":large_yellow_circle: :orange[Objectives]")
    st.write("""
    - **Consolidate and simplify** information about the CPFIS from multiple official sources.
    - **Provide an interactive RAG chatbot** to answer user queries about the CPFIS.
    - **Visualize available CPFIS-approved investment options** to help users make informed decisions.
    - **Enhance user understanding** of CPFIS regulations and investment options through interactive features.
    """)
    
    st.header(":large_green_circle: :orange[Data Sources]")
    st.write("""
    - [CPF website](https://www.cpf.gov.sg)
        - [CPFIS Information Pages](https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/investing-your-cpf-savings)
        - [CPFIS Scheme Options](https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/investing-your-cpf-savings/cpf-investment-scheme-options)
        - [CPFIS Self-Awareness Questionnaire](https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/investing-your-cpf-savings/cpf-investment-scheme-self-awareness-questionnaire)
        - [Earning Attractive Interest](https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/earning-attractive-interest)
        - [What You Need to Know About CPFIS](https://www.cpf.gov.sg/member/infohub/educational-resources/cpf-investment-scheme-what-you-need-to-know-about-cpfis)
    - [Singapore Statutes Online - CPFIS Regulations](https://sso.agc.gov.sg/SL/CPFA1953-RG9?DocDate=20161220&ProvIds=P1II-)
    - CPFIS-approved UTs and ILPs lists
        - [Approved Investment Products](https://www.cpf.gov.sg/content/dam/web/member/growing-your-savings/documents/CPFISInvestmentProducts.pdf)
        - [Approved ILPs](https://www.cpf.gov.sg/content/dam/web/member/business-partners/documents/RCSILP_ListA.pdf)
        - [Approved UTs](https://www.cpf.gov.sg/content/dam/web/member/business-partners/documents/RCSUT_ListA.pdf)
    """)
    
    st.header(":large_purple_circle: :orange[Features]")
    st.write("""
    - **Request for OpenAI API Key:** Users will need to input their OpenAI API Key before asking questions.
    - **RAG Chatbot for CPFIS Information:**
        - An interactive chatbot trained on CPFIS information and regulations
        - Answers user queries about the scheme, eligibility, and investment options
        - Provides simplified, easy-to-understand explanations
    - **CPFIS Investment Options Visualization:**
        - Interactive tables and charts displaying CPFIS-approved UTs and ILPs
        - Filtering options based on risk levels, focus/scope, geographical area, and sector focus
        - Visual representation of key fund information, including performance and risk levels
    """)

if __name__ == "__main__":
    about()