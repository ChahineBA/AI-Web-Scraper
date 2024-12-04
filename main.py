import streamlit as st  # Importing the Streamlit library for creating the web app interface
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content  # Importing functions for web scraping and content cleaning
from parse import parse_with_ollama  # Importing the function for parsing content with Ollama

# Set the title of the Streamlit web app
st.title("AI Web Scraper")

# Create a text input field for the user to enter the website URL
url = st.text_input("Enter a Website URL: ")

# Create a button for the user to trigger the website scraping process
if st.button("Scrape Website"):
    st.write("Scraping the website")  # Display a message indicating scraping is in progress

    # Scrape the website using the provided URL
    result = scrape_website(url)
    
    # Extract the body content from the scraped result
    body_content = extract_body_content(result)
    
    # Clean the extracted body content (removes unnecessary elements or formatting)
    cleaned_content = clean_body_content(body_content)

    # Store the cleaned content in Streamlit's session state for later use
    st.session_state.dom_content = cleaned_content

    # Expandable section to display the DOM content in a text area (with a height of 300px)
    with st.expander("View DOM Content"):
        st.text_area("DOM Content:", cleaned_content, height=300)

# Check if the DOM content is stored in the session state (from previous scraping)
if "dom_content" in st.session_state:
    # Create a text area for the user to describe what they want to parse from the content
    parse_description = st.text_area("Describe what you want to parse")

    # Create a button for the user to trigger the parsing process
    if st.button("Parse Content"):
        # Check if the user provided a description for what they want to parse
        if parse_description:
            st.write('Parsing the content')  # Display a message indicating parsing is in progress
            
            # Split the DOM content into chunks to facilitate easier parsing
            dom_chunks = split_dom_content(st.session_state.dom_content)
            
            # Call the Ollama parsing function with the DOM chunks and user description
            result = parse_with_ollama(dom_chunks, parse_description)
            
            # Display the parsed result
            st.write(result)
