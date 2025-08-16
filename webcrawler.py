import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_amazon_links(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        # Send a GET request to the URL
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP request errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor tags
        links = set()
        for a_tag in soup.find_all('a', href=True):
            # Resolve relative URLs to absolute URLs
            full_url = urljoin(url, a_tag['href'])
            links.add(full_url)

        return links

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return set()

# Example usage
amazon_url = "https://www.amazon.in/"
hyperlinks = get_amazon_links(amazon_url)

# Print the extracted links
for link in hyperlinks:
    print("\""+link+"\""+",")
