import requests
from bs4 import BeautifulSoup

def scrape_news_article(article_url):
    """
    Fetch and extract the title, author, date, and content from a news article.

    Parameters:
        article_url (str): The URL of the news article to scrape.

    Returns:
        dict: A dictionary containing the extracted data.
    """
    try:
        # Send an HTTP GET request to fetch the webpage content
        http_response = requests.get(article_url)
        http_response.raise_for_status()  # Raise an error for HTTP request failures (e.g., 404, 500)

        # Parse the HTML content using BeautifulSoup
        soup_object = BeautifulSoup(http_response.text, 'html.parser')

        # Extract the article title (if found)
        article_title = soup_object.find('h1')
        extracted_title = article_title.get_text().strip() if article_title else "Title not found"

        # Extract the author's name (many sites use <meta> tags for this)
        author_meta = soup_object.find("meta", attrs={"name": "author"})
        extracted_author = author_meta["content"] if author_meta else "Author not found"

        # Extract the publication date (often in <time> or <meta> tags)
        date_meta = soup_object.find("meta", attrs={"property": "article:published_time"})
        extracted_date = date_meta["content"] if date_meta else "Date not found"

        # Extract the article content (all paragraphs within <p> tags)
        paragraph_elements = soup_object.find_all('p')
        extracted_content = "\n".join(paragraph.get_text().strip() for paragraph in paragraph_elements)

        # Return extracted data in a structured format
        return {
            "title": extracted_title,
            "author": extracted_author,
            "publication_date": extracted_date,
            "content": extracted_content
        }

    except requests.exceptions.RequestException as request_error:
        return {"error": f"Failed to fetch article: {request_error}"}

if __name__ == "__main__":
    # Ask the user for a news article URL
    user_input_url = input("Enter the news article URL: ")
    
    # Scrape the article and display results
    scraped_data = scrape_news_article(user_input_url)

    print("\n--- Article Details ---")
    print(f"Title: {scraped_data.get('title', 'N/A')}")
    print(f"Author: {scraped_data.get('author', 'N/A')}")
    print(f"Publication Date: {scraped_data.get('publication_date', 'N/A')}")
    print("\n--- Content ---")
    print(scraped_data.get('content', 'N/A'))
