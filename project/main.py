import time
from playwright.sync_api import sync_playwright
import requests
import os

# Telegram configuration
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"

# Send a message to Telegram
def send_telegram_message(message):
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
    }
    try:
        response = requests.post(TELEGRAM_API_URL, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

def scrape_flipkart():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Launch Chromium browser in headless mode
        page = browser.new_page()

        # Set user agent and navigate to Flipkart's footwear page
        page.set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        page.goto('https://www.flipkart.com/footwear/pr?sid=osp')

        # Retry mechanism and waiting for the selector
        max_retries = 3
        discount_threshold = 60  # Set discount threshold to 60%

        for attempt in range(max_retries):
            try:
                # Wait for the product selector to be visible (increased timeout)
                page.wait_for_selector('._1AtVbE', timeout=60000)  # 60 seconds timeout

                # Get product details
                product_elements = page.query_selector_all('._1AtVbE')
                deals_above_discount = []

                for product in product_elements:
                    try:
                        # Extract product info (example: title, price, discount)
                        title = product.inner_text('._2Kn22P')  # Assuming title is in this class
                        price = product.inner_text('._30jeq3')  # Assuming price is in this class
                        discount = product.inner_text('._3Ay6Sb')  # Assuming discount is in this class

                        # Clean discount and convert to integer
                        discount_percentage = int(discount.replace('%', '').strip())

                        if discount_percentage >= discount_threshold:
                            deals_above_discount.append({
                                "title": title,
                                "price": price,
                                "discount": discount_percentage,
                            })

                    except Exception as e:
                        print(f"Error extracting product info: {e}")
                        continue

                if deals_above_discount:
                    for deal in deals_above_discount:
                        message = f"Deal found: {deal['title']} for {deal['price']} with {deal['discount']}% off"
                        send_telegram_message(message)
                else:
                    send_telegram_message("No deals found above 60%.")

                break  # Exit loop if successful
            except Exception as e:
                if attempt == max_retries - 1:
                    print(f"Error occurred after {max_retries} attempts: {str(e)}")
                    send_telegram_message(f"Error occurred during scraping: {str(e)}")
                else:
                    print(f"Retrying... Attempt {attempt + 1}")
                    time.sleep(5)  # Wait 5 seconds before retrying

        browser.close()

if __name__ == "__main__":
    print("Starting Flipkart Scraper...")
    try:
        scrape_flipkart()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        send_telegram_message(f"An error occurred during scraping: {str(e)}")
