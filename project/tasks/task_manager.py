from playwright.sync_api import sync_playwright

# List of Flipkart categories and search URLs to scrape
categories = [
    "https://www.flipkart.com/footwear/pr?sid=osp&p%5B%5D=facets.discount_range_v1%255B%255D%3D70%2525%2Bor%2Bmore&p%5B%5D=facets.rating%255B%255D%3D4%25E2%2598%2585%2B%2526%2Babove",
    "https://www.flipkart.com/search?q=discount",  # Example search URL for discounted products
    # Add more category or search URLs as needed
]

# Function to crawl multiple pages and categories
def fetch_and_process_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Iterate over the categories and scrape pages dynamically
        for category_url in categories:
            print(f"Scraping: {category_url}")
            page.goto(category_url)

            # Handle dynamic content loading by scrolling or waiting for content to load
            while not is_content_loaded(page):
                page.evaluate("window.scrollBy(0, window.innerHeight)")

            # Fetch content after loading
            content = page.content()
            process_content(content)  # Process the content as needed

            # Check for pagination and click next if exists
            paginate_and_scrape(page)

        browser.close()

# Check if content is loaded
def is_content_loaded(page):
    # You can use more complex checks here based on the page's dynamic content
    return page.locator("text=Next").is_visible()

# Function to handle pagination and scrape multiple pages
def paginate_and_scrape(page):
    try:
        # Find the 'Next' button and click it to load the next page of results
        next_button = page.locator("text=Next")
        if next_button.is_visible():
            next_button.click()
            page.wait_for_load_state("networkidle")  # Wait until page finishes loading
            content = page.content()
            process_content(content)  # Process the new page content
            paginate_and_scrape(page)  # Recursively scrape the next page
    except Exception as e:
        print("No more pages or error during pagination:", e)

# Function to process the fetched content
def process_content(content):
    print("Processing content...")  # Perform your processing on the content
    # Example: Save the content to a file or perform any other task.
    save_content_to_file(content)

# Function to save content to a file
def save_content_to_file(content):
    with open("output.json", "a") as f:
        f.write(content + "\n")

