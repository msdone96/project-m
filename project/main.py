name: Scraper Workflow

on:
  schedule:
    # This will run the workflow every 5 minutes
    - cron: '*/5 * * * *'  # Runs every 5 minutes

jobs:
  scrape:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Install Playwright Browsers
        run: |
          python -m playwright install

      - name: Run Scraper
        run: |
          python project/main.py
        env:
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
          TELEGRAM_API_TOKEN: ${{ secrets.TELEGRAM_API_TOKEN }}
