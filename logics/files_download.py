import streamlit as st
import pandas as pd
import os
import json
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

# **********************USE CASE 1*************************

# 1) What can be invested, directly typed in
WhatCan_data = {
    "Investment products included under CPFIS": [
        "Unit Trusts (UTs)", "Investment-linked insurance products (ILPs)", "Annuities",
        "Endowment policies", "Singapore Government Bonds (SGBs)", "Treasury Bills (T-bills)",
        "Exchange Traded Funds (ETFs)", "Fund Management Accounts", "Fixed Deposits (FDs)",
        "Statutory Board Bonds", "Bonds Guaranteed by Singapore Government", "Shares",
        "Property Funds", "Corporate Bonds", "Gold ETFs",
        "Other Gold products (such as Gold certificates, Gold savings accounts, Physical Gold)"
    ],
    "You can invest using your CPF savings from OA": [
        "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "No products currently available",
        "No products currently available", "Yes", "Yes", "Yes", "Yes", "Yes"
    ],
    "Remarks under OA": [
        "", "", "", "", "", "", "", "", "", "",
        "", "", "", "", "", ""
    ],
    "You can invest using your CPF savings from SA": [
        "Yes", "Yes", "Yes", "Yes", "Yes", "Yes", "", "No", "Yes", "No products currently available",
        "No products currently available", "No", "No","No","No","No"
    ],
    "Remarks under SA": [
        "Higher risk UTs are not included", "Higher risk ILPs are not included", "", "", "", "", 
        "No products currently available; Higher risk ETFs are not included", "", "", "", 
        "", "", "", "", "", ""
    ],
    "Links": [
        "Visit https://fundsingapore.com/fund-library for more information", 
        "Visit https://fundsingapore.com/fund-library for more information",
        "Visit https://fundsingapore.com/fund-library for more information", 
        "Visit https://fundsingapore.com/fund-library for more information", 
        "Visit https://www.mas.gov.sg/bonds-and-bills/Singapore-Government-Bonds-Information-for-Individuals for more information", 
        "Visit https://www.mas.gov.sg/bonds-and-bills/Singapore-Government-T-bills-Information-for-Individuals for more information",
        "", "", "",  "", "", 
        "Visit https://www.sgx.com/securities/stocks-under-cpf-investment-scheme for more information", 
        "", "", "", ""
    ],
    "Additional information": [
        "", "", "", "", "", "", "", "", "", "", "", 
        "Up to 35% of investible savings can be invested", 
        "Up to 35% of investible savings can be invested", 
        "Up to 35% of investible savings can be invested", 
        "Up to 10% of investible savings can be invested", 
        "Up to 10% of investible savings can be invested"
    ],
    "Updated as of": [
        "Oct-22", "Oct-22", "Oct-22", "Oct-22", "Oct-22", "Oct-22", 
        "Oct-22", "Oct-22", "Oct-22", "Oct-22", "Oct-22", "Oct-22", 
        "Oct-22", "Oct-22", "Oct-22", "Oct-22"
    ]
}

# Define data file paths
OUTPUT_DIR = "data"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

CPF_FILE_PATH = os.path.join(OUTPUT_DIR, 'CPF_scraped_data.json')
SSO_FILE_PATH = os.path.join(OUTPUT_DIR, 'SSO_scraped_data.json')

# Retry delay and max attempts constants; added v01
RETRY_DELAY = 5  # seconds
MAX_RETRIES = 3

from webdriver_manager.chrome import ChromeDriverManager
# def scrape_page_content(url, category, target_classes):
#     # Set up Selenium WebDriver in headless mode with additional options
#     options = Options()
#     options.add_argument("--headless")
#     options.add_argument('--disable-gpu')
    
#     driver = None
#     try:
#         driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
#         # DEBUG log in Streamlit (remove or modify as needed)
#         st.write(f"DEBUG:DRIVER:{driver}")
        
#         # Scrape each URL with retry mechanism
#         scraped_data = []
#         for attempt in range(MAX_RETRIES):
#             try:
#                 driver.get(url)
#                 time.sleep(2)  # Wait for the page to load
                
#                 # Parse page source with BeautifulSoup
#                 soup = BeautifulSoup(driver.page_source, 'html.parser')
                
#                 for class_name in target_classes[category]:
#                     content_divs = soup.find_all('div', class_=class_name)
#                     text = ' '.join([div.get_text(separator=' ', strip=True) for div in content_divs]) if content_divs else 'Content not found'
                    
#                     page_data = {
#                         'url': url,
#                         'content': {class_name: text}
#                     }
#                     scraped_data.append(page_data)
                    
#                     # Debug print for scraping feedback
#                     print(f"Scraped content from {url} for class {class_name}:\n{text}\n{'='*80}")
#                 break  # Exit loop if successful

#             except Exception as e:
#                 print(f"Attempt {attempt + 1} failed for {url}: {e}")
#                 if attempt < MAX_RETRIES - 1:
#                     print(f"Retrying in {RETRY_DELAY} seconds...")
#                     time.sleep(RETRY_DELAY)
#                 else:
#                     st.write("Max retries reached. Moving to the next URL.")
#                     print("Max retries reached. Moving to the next URL.")

#     except Exception as e:
#         st.write(f"DEBUG:INIT_DRIVER:ERROR:{e}")
#     finally:
#         if driver is not None:
#             driver.quit()

#     return scraped_data

# Function to scrape all text content from a URL
def scrape_page_content(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    
    driver = None
    scraped_content = ""
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        for attempt in range(MAX_RETRIES):
            try:
                driver.get(url)
                time.sleep(2)  # Wait for the page to load
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Get all text from the page
                scraped_content = soup.get_text(separator=' ', strip=True)
                break  # Exit loop if successful

            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt < MAX_RETRIES - 1:
                    print(f"Retrying in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    print("Max retries reached. Moving to the next URL.")

    finally:
        if driver is not None:
            driver.quit()

    return scraped_content

# Function to save scraped data as JSON
def save_scraped_data(filepath, data):
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Scraped data saved in {filepath}")

def scrape_and_save_data():
        # URL lists
    urls = {
        "CPF": [
            "https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/investing-your-cpf-savings/cpf-investment-scheme-self-awareness-questionnaire",
            "https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/investing-your-cpf-savings/cpf-investment-scheme-options",
            "https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/investing-your-cpf-savings/cpf-investment-scheme-self-awareness-questionnaire",
            "https://www.cpf.gov.sg/member/infohub/educational-resources/cpf-investment-scheme-what-you-need-to-know-about-cpfis",
            "https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/investing-your-cpf-savings",
            "https://www.cpf.gov.sg/member/growing-your-savings/earning-higher-returns/earning-attractive-interest",
            # Add other CPF URLs here
        ],
        "SSO": [
            "https://sso.agc.gov.sg/SL/CPFA1953-RG9?DocDate=20240628&WholeDoc=1",
            # Add other SSO URLs here
        ]
    }

    # Target classes for CPF and SSO content
    target_classes = {
        "CPF": ['cmp-teaser__content', 'section-head section-title', 'container responsivegrid'],
        "SSO": ['row footer-title', 'status-value', 'legis']
    }

    # Initialize scraped data dictionary
    scraped_data = {
        "CPF": [],
        "SSO": []
    }

    for category, url_list in urls.items():
        for url in url_list:
            scraped_content = scrape_page_content(url)
            if scraped_content:  # Only add if scraping was successful
                scraped_data[category].append({
                    'url': url,
                    'content': scraped_content
                })

    # Save scraped data to JSON files
    save_scraped_data(CPF_FILE_PATH, scraped_data["CPF"])
    save_scraped_data(SSO_FILE_PATH, scraped_data["SSO"])

    return scraped_data["CPF"], scraped_data["SSO"], WhatCan_data

# Function to load data from JSON files and return as dictionaries
def load_data():
    try:
        with open(CPF_FILE_PATH, 'r') as file:
            CPF_scraped_data = json.load(file)
        with open(SSO_FILE_PATH, 'r') as file:
            SSO_scraped_data = json.load(file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return WhatCan_data, {}, {}  # Return empty data if file not found
    return WhatCan_data, CPF_scraped_data, SSO_scraped_data
# **********************USE CASE 1*************************

# **********************USE CASE 2*************************
# URLs for PDFs
CPF_UTs_pdf_url = "https://www.cpf.gov.sg/content/dam/web/member/business-partners/documents/RCSUT_ListA.pdf"
CPF_ILPs_pdf_url = "https://www.cpf.gov.sg/content/dam/web/member/business-partners/documents/RCSILP_ListA.pdf"
# Headers for PDF fetching
headers = {"User-Agent": "Mozilla/5.0"}

# Function to get the latest update date from the PDF
def get_update_date(pdf_content):
    try:
        with pdfplumber.open(BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                    
                # Use regex to find the update date
                date_match = re.search(r'Updated on (\d{1,2} \w+ \d{4})', text)
                if date_match:
                    return date_match.group(1)
        return None
    except Exception as e:
        print(f"Error reading PDF content: {e}")
        return None

# Function to clean table data and add necessary columns
def clean_table_data(df, update_date, investment_type):
    if df is None:
        raise ValueError("Input DataFrame is None")    
        
    # Strip whitespace from all string columns
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
    # Check and drop rows where 'SN' is not numeric
    df = df[pd.to_numeric(df['SN'], errors='coerce').notnull()]

    # Rename columns based on partial matches
    rename_map = {
        r"(1-Year Performance \(annualised\)).*": r"\1 (%)",
        r"(3-Year Performance \(annualised\)).*": r"\1 (%)",
        r"(Expense Ratio).*": r"\1 (%)",
        r"(Sharpe Ratio).*": r"\1",
    }
    df.columns = df.columns.to_series().replace(rename_map, regex=True)

    # Convert numeric columns to float (where applicable) after removing any percentage signs
    numeric_columns = df.columns[df.columns.str.contains("Expense Ratio|Sharpe Ratio|1-Year Performance|3-Year Performance", regex=True)]
    # Remove '%' sign if present and convert to numeric
    for col in numeric_columns:
        df[col] = df[col].str.replace('%', '', regex=False)  # Remove the '%' symbol
        df[col] = pd.to_numeric(df[col], errors="coerce")  # Convert to numeric, coercing errors to NaN

    # Parse 'Risk Class'
    if 'Risk Class' in df.columns:
        df[['Risk Level', 'Focus/Scope', 'Geographical Area', 'Sector Focus']] = (
            df['Risk Class'].str.split(' - ', expand=True).apply(lambda x: x.str.strip())
        )

    # Parse 'Included under CPFIS-OA/SA'
    if 'Included under CPFIS-OA/SA' in df.columns:
        df['CPFIS - OA'] = df['Included under CPFIS-OA/SA'].apply(lambda x: 'Yes' if 'OA' in str(x) else 'No')
        df['CPFIS - SA'] = df['Included under CPFIS-OA/SA'].apply(lambda x: 'Yes' if 'SA' in str(x) else 'No')

    # Rename the first column
    df.rename(columns={df.columns[1]: f"List updated as at {update_date}"}, inplace=True)

    #Drop columns
    df.drop(['SN','Risk Class','Included under CPFIS-OA/SA'], axis=1,inplace=True)

    print(df) #check
        
    return df

# Function to extract and segregate tables from PDF
def extract_and_segregate_tables(pdf_content, section_titles):
    data_by_section = {section: [] for section in section_titles}
    current_section = None
        
    try:
        with pdfplumber.open(BytesIO(pdf_content)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                table = page.extract_table()

                if table:
                    for row in table:
                        row_text = ' '.join([str(cell) for cell in row])

                        # Identify the section from the text
                        for section in section_titles:
                            if section in row_text:
                                current_section = section
                                break

                        # Add rows to the correct section
                        if current_section:
                            data_by_section[current_section].append(row)

        return data_by_section
    except Exception as e:
        print(f"Error extracting tables from PDF: {e}")
        return None
    
def process_pdf(pdf_url, section_titles, investment_type, output_file_prefix):

    # Fetch the PDF content
    response = requests.get(pdf_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to download PDF: {response.status_code}")
        return None  # Return None to indicate failure

    pdf_content = response.content
    update_date = get_update_date(pdf_content)
    print(f"Latest update date for {output_file_prefix}: {update_date}")

    data_by_section = extract_and_segregate_tables(pdf_content, section_titles)
    if data_by_section is None:
        print(f"No data extracted from PDF for {output_file_prefix}")
        return None  # Return None if extraction failed

    # Clean and save data for each section
    for section, data in data_by_section.items():
        if data:
            df = pd.DataFrame(data[1:], columns=data[0])
            cleaned_df = clean_table_data(df, update_date, investment_type[section])

            # Convert DataFrame to JSON format
            json_data = cleaned_df.to_json(orient='records', indent=4)

            # Save the JSON file
            output_file_path = os.path.join(OUTPUT_DIR, f"{output_file_prefix}_{section.replace(' ', '_')}.json")
            with open(output_file_path, 'w') as json_file:
                json_file.write(json_data)
                    
            print(f"Data for section '{section}' saved as JSON at: {output_file_path}")

    return data_by_section  # Ensure to return the processed data

# Define the section titles and corresponding investment types for Unit Trusts
sections_UTs = ["List A Funds - Unit Trusts", "List A Funds - only for Investment - Linked Insurance Policies to feed into"]
investment_types_UTs = {
    "List A Funds - Unit Trusts": "Unit Trusts (UTs)",
    "List A Funds - only for Investment - Linked Insurance Policies to feed into": "Unit Trusts (UTs) - only for Investment - Linked Insurance Policies to feed into"
}

# Process Unit Trusts PDF
cleaned_UTs_data = process_pdf(
    pdf_url=CPF_UTs_pdf_url,
    section_titles=sections_UTs,
    investment_type=investment_types_UTs,
    output_file_prefix="CPF_UTs"
)

# Define the section titles and corresponding investment types for ILPs
sections_ILPs = ["List A Funds - Investment Linked Products"]
investment_types_ILPs = {
    "List A Funds - Investment Linked Products": "Investment-linked insurance products (ILPs)"
}

# Process ILP-only PDF
cleaned_ILPs_data = process_pdf(
    pdf_url=CPF_ILPs_pdf_url,
    section_titles=sections_ILPs,
    investment_type=investment_types_ILPs,
    output_file_prefix="CPF_ILPs"
)

# Function to load JSON data for a specified file
def load_data1(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    return pd.read_json(filepath)