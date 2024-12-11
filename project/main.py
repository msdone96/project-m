import time
from tasks.task_manager import fetch_and_process_data

# Main function to run the scraper
def main():
    print("Starting Flipkart Scraper...")

    # Call the function to fetch and process data
    try:
        fetch_and_process_data()
    except Exception as e:
        print(f"An error occurred: {e}")
    
    print("Scraping completed.")

if __name__ == "__main__":
    main()
