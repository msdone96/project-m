import requests
import time
from playwright.sync_api import sync_playwright

# Your Telegram Bot Token and Chat ID
chat_id = '6500267334'
token = '8070344172:AAHwWrbfbA3Ty8rICF9RS8pov1Sp9KG9BHE'

# Function to send a message to Telegram
def send_telegram_message(chat_id, token, message):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': message,
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")

# Function to scrape deals from Flipkart
def scrape_flipkart():
    deals = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Run in headless mode
        page = browser.new_page()

        # Start scraping a page with products, you can add more pages or categories as needed
        url = 'https://www.flipkart.com/footwear/pr?sid=osp&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove'
        page.goto(url)

        # Wait for the content to load
        page.wait_for_selector('.col-12-12')

        # Find the deals based on the discount info
        product_elements = page.query_selector_all('.col-12-12')

        for product in product_elements:
            try:
                name = product.query_selector('.IRpwTa').inner_text()
                discount = product.query_selector('.gUuXy-').inner_text().replace('%', '')
                
                # Filter deals above 91% discount
                if int(discount) >= 91:
                    deals.append({
                        'name': name,
                        'discount': int(discount)
                    })
            except Exception as e:
                print(f"Error extracting product info: {e}")

        browser.close()

    return deals

# Function to send deals above 91% to Telegram
def send_deals_to_telegram(deals):
    if deals:
        message = "Here are the deals above 91%:\n"
        for deal in deals:
            message += f"{deal['name']}: {deal['discount']}% off\n"
        send_telegram_message(chat_id, token, message)
    else:
        send_telegram_message(chat_id, token, "No deals found above 91%")

# Main function to run the scraper and send results
def main():
    print("Starting Flipkart Scraper...")
    try:
        deals = scrape_flipkart()
        if deals:
            send_deals_to_telegram(deals)
        else:
            print("No deals found above 91%.")
    except Exception as e:
        print(f"An error occurred: {e}")
        send_telegram_message(chat_id, token, f"An error occurred while scraping: {e}")

if __name__ == "__main__":
    main()
