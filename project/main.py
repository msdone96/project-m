import os
import requests
from playwright.sync_api import sync_playwright
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram settings from environment variables
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN')

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")

# Scraping function using Playwright
def scrape_flipkart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            print("Starting Flipkart Scraper...")
            # Go to the Flipkart page (update the URL if necessary)
            page.goto('https://www.flipkart.com/footwear/pr?sid=osp&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove')
            page.wait_for_selector('._1AtVbE')  # Ensure the page is loaded and the product list is present

            # Get all product items on the page
            products = page.query_selector_all('._1AtVbE')

            found_deals = []

            for product in products:
                try:
                    # Extract product name, discount, and price
                    product_name = product.query_selector('._4rR01T').inner_text() if product.query_selector('._4rR01T') else 'No name found'
                    discount = product.query_selector('._3Ay6Sb').inner_text() if product.query_selector('._3Ay6Sb') else 'No discount found'
                    price = product.query_selector('._30jeq3').inner_text() if product.query_selector('._30jeq3') else 'No price found'

                    # Extract discount percentage (if available) and check if it's above 91%
                    if discount != 'No discount found':
                        discount_percentage = int(discount.replace('%', ''))
                        if discount_percentage > 91:
                            found_deals.append(f"{product_name} - {discount_percentage}% off - Price: {price}")
                    
                except AttributeError as e:
                    print(f"Error extracting product info: {e}")
            
            # Send message if deals are found above 91%
            if found_deals:
                deals_message = "\n".join(found_deals)
                send_telegram_message(f"Found deals above 91%:\n{deals_message}")
            else:
                send_telegram_message("No deals found above 91%.")

        except Exception as e:
            print(f"An error occurred: {e}")
            send_telegram_message(f"Error occurred during scraping: {e}")
        finally:
            browser.close()

# Run the scraper function
if __name__ == "__main__":
    scrape_flipkart()
