import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Referer': 'https://www.flipkart.com'
}


def get_flipkart_price(product_name):
    try:
        # Construct the search URL with product name
        search_url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
        response = requests.get(search_url, headers=headers)
        
        # If the request fails
        if response.status_code != 200:
            return "Failed to fetch data", search_url
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Search for price in the div with the class 'Nx9bqj _4b5DiR'
        product_price_tag = soup.find('div', class_='Nx9bqj _4b5DiR')  # This is the class for price
        if product_price_tag:
            product_price = product_price_tag.get_text(strip=True)
        else:
            return "Price not found", search_url
        
        # Fetch the product name from search results
        product_name_tag = soup.find('a', {'class': 'IRpwTa'})
        if product_name_tag:
            product_name = product_name_tag.get_text(strip=True)
        else:
            product_name = "Not found"

        return product_price, search_url

    except Exception as e:
        print(f"Error fetching Flipkart price: {e}")
        return "Error", "Error"


# Function to scrape Amazon (unchanged)
def get_amazon_price(product_name):
    try:
        search_url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Parse Amazon product name and price
        if soup.select('.a-price-whole') and soup.select('.a-color-base.a-text-normal'):
            product_name = soup.select('.a-color-base.a-text-normal')[0].getText().strip()
            product_price = soup.select('.a-price-whole')[0].getText().strip()
            return f"₹{product_price}", search_url
        else:
            return "Not found", search_url
    except Exception as e:
        print(f"Error fetching Amazon price: {e}")
        return "Not found", search_url
