# Warner Brothers Studio Tour Ticket Scraper

This project is a web scraper designed to automate the process of checking and booking tickets for the Warner Brothers Studio Tour. The scraper uses Selenium to interact with the website and automates tasks such as selecting dates, rejecting cookies, and adding tickets to the basket.


## Installation

### Prerequisites

- Python 3.8 or higher
- Pipenv
- Google Chrome or Firefox

### Steps

1. **Clone the repository**

    ```bash
    git clone https://https://github.com/dariakriukova/warner-brothers-scraper
    cd warner-brothers-scraper
    ```

2. **Set up the virtual environment**

    ```bash
    pipenv install
    ```

3. **Create a `.env` file**

    Create a `.env` file in the project root directory and add your Telegram bot token and chat ID. You can create a telegram bot using BotFather:

    ```
    TELEGRAM_BOT_TOKEN=your_bot_token
    TELEGRAM_CHAT_ID=your_chat_id
    ```

## Usage

1. **Run the scraper**

    ```bash
    pipenv run python main.py
    ```

2. The scraper will:
   - Open the Warner Brothers Studio Tour ticket purchasing page
   - Reject cookies
   - Select dates and check for ticket availability
   - Notify you via Telegram if tickets are available within the specified date range
   - Automate the process of selecting the first available time slot, increasing ticket quantity, and adding tickets to the basket

3. The script will keep the browser open for manual continuation after adding the ticket to the basket.

## Modules

### `config.py`

Handles loading environment variables from the `.env` file.

### `utils.py`

Contains utility functions such as:
- `send_telegram_message`: Sends a message to a Telegram chat
- `simulate_user_activity`: Simulates user activity to keep the session alive
- `extend_session`: Extends the session if the button appears
- `filter_dates`: Filters available dates within a specified range

### `scraper.py`

Contains the main scraping functions such as:
- `reject_cookies`: Rejects cookies on the website
- `check_for_availability`: Checks for available dates in a given month
- `switch_month`: Switches the calendar to a specified month
- `select_first_available_time_for_date`: Selects the first available time slot for a given date
- `increase_ticket_quantity`: Increases the quantity of tickets
- `add_to_basket`: Adds tickets to the basket
- `handle_additional_items`: Handles any additional items or steps in the checkout process
- `click_continue_button`: Clicks the continue button to proceed to the final checkout step

### `main.py`

The main script that orchestrates the scraping process, including:
- Setting up and starting the scraper
- Handling the main loop for checking ticket availability and sending notifications
- Managing session activity and extending sessions as needed

## Notes

- Ensure that you have the correct WebDriver version that matches your browser version.
- The script is designed to keep the browser open for manual intervention after adding tickets to the basket. This allows you to complete the purchase process manually.


