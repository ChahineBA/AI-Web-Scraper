import selenium.webdriver as webdriver  # Importing selenium for web automation
from selenium.webdriver.chrome.service import Service  # Importing Service class for managing the ChromeDriver
from webdriver_manager.chrome import ChromeDriverManager  # Automatically manage ChromeDriver installation
import time  # Importing time for controlling sleep durations
from bs4 import BeautifulSoup  # Importing BeautifulSoup for HTML parsing

# Function to scrape the website and return its HTML content
def scrape_website(website):
    print("Launching chrome browser...")
    
    # For Linux:
    options = webdriver.ChromeOptions()  # Set Chrome options to run headlessly
    options.add_argument('--headless')  # Run browser in headless mode (without UI)
    options.add_argument('--no-sandbox')  # Disables sandboxing for better performance in headless mode
    options.add_argument('--disable-dev-shm-usage')  # Ensures the browser doesn't run into memory issues in containers
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)  # Initialize Chrome with the options
    
    try:
        driver.get(website)  # Open the specified website
        print("Page Loaded...")  # Indicate the page has loaded successfully
        html = driver.page_source  # Get the HTML source of the page
        time.sleep(10)  # Wait for 10 seconds to ensure that the page is fully loaded
        return html  # Return the HTML content of the page
    finally:
        driver.quit()  # Quit the browser after scraping

# Function to extract the body content from the HTML
def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")  # Parse the HTML content using BeautifulSoup
    body_content = soup.body  # Extract the <body> content from the parsed HTML
    if body_content:
        return str(body_content)  # Return the body content as a string if it exists
    return ""  # Return an empty string if no body content is found

# Function to clean the body content by removing unnecessary elements like scripts and styles
def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, 'html.parser')  # Parse the body content with BeautifulSoup
    for script_or_style in soup(["script", "style"]):  # Find and remove all <script> and <style> elements
        script_or_style.extract()  # Extract these elements from the content
    
    cleaned_content = soup.get_text(separator="\n")  # Extract only the text content, using newlines as separators
    cleaned_content = '\n'.join(  # Clean the text by stripping extra spaces from each line
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )
    return cleaned_content  # Return the cleaned body content

# Function to split the DOM content into smaller chunks, each of max length 'max_len'
def split_dom_content(dom_content, max_len=6000):
    return [
        dom_content[i:i+max_len] for i in range(0, len(dom_content), max_len)  # Split the content into chunks
    ]
