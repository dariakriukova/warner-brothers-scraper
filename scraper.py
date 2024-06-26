import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Telegram bot token and chat ID from environment variables
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Function to send message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, data=payload)

# Set up the WebDriver (Assuming you have the appropriate driver for your browser)
driver = webdriver.Chrome()  # or webdriver.Firefox() or another browser's driver

# URL to the ticket purchasing page
ticket_url = "https://tickets.wbstudiotour.co.uk/webstore/shop/viewitems.aspx?cg=hptst2&c=tix2"

# Open the ticket purchasing page
driver.get(ticket_url)
print("Please select the number of tickets manually and press Enter to continue...")
input()  # Wait for user input after they have selected the number of tickets manually

# Find and click the button to select date and time
select_date_button = driver.find_element(By.CSS_SELECTOR, "button.shared-calendar-button")
select_date_button.click()
time.sleep(5)  # Wait for the calendar to load completely

def check_for_july_availability():
    # Check if the first month in the calendar is July
    month_dropdown = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder$SalesChannelDetailControl$EventsDateTimeSelectorModal$EventsDateTimeSelector$CalendarSelector$MonthDropDownList")
    selected_month = month_dropdown.find_element(By.CSS_SELECTOR, "option[selected]").text
    available_dates = []
    if selected_month == "July":
        days = driver.find_elements(By.CSS_SELECTOR, ".calendar-body .day.available")
        for day in days:
            aria_label = day.get_attribute("aria-label")
            if aria_label and "07/2024" in aria_label:
                available_dates.append(aria_label.strip())
    return available_dates

def filter_dates(dates, start_date, end_date):
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    filtered_dates = []
    for date in dates:
        try:
            date_obj = datetime.strptime(date, "%d/%m/%Y")
            if start <= date_obj <= end:
                filtered_dates.append(date)
        except ValueError as e:
            print(f"Error parsing date {date}: {e}")
    return filtered_dates

def switch_month(month):
    # Switch to the specified month if not already selected
    month_dropdown = driver.find_element(By.NAME, "ctl00$ContentPlaceHolder$SalesChannelDetailControl$EventsDateTimeSelectorModal$EventsDateTimeSelector$CalendarSelector$MonthDropDownList")
    selected_option = month_dropdown.find_element(By.CSS_SELECTOR, "option[selected]").text
    if selected_option != month:
        month_options = month_dropdown.find_elements(By.TAG_NAME, "option")
        for option in month_options:
            if option.text == month:
                option.click()
                print(f"Switched to {month}")
                time.sleep(5)  # Wait for the calendar to update
                break

# Function to simulate user activity
def simulate_user_activity():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")
    print("Simulated user activity to keep the session alive.")

# Function to extend session if the button appears
def extend_session():
    try:
        extend_button = driver.find_element(By.CSS_SELECTOR, "button.ui-control.button.extendSession")
        extend_button.click()
        print("Extended session by clicking the button.")
        time.sleep(2)  # Wait a moment after clicking the button
    except NoSuchElementException:
        print("Extend session button not found, continuing monitoring.")

# Set to store already notified dates
notified_dates = set()

# Date range for notifications
start_date = "19/07/2024"
end_date = "22/07/2024"

try:
    while True:
        extend_session()  # Check and click the extend session button if it appears
        
        switch_month("July")
        available_dates = check_for_july_availability()
        filtered_dates = filter_dates(available_dates, start_date, end_date)
        new_dates = [date for date in filtered_dates if date not in notified_dates]
        if new_dates:
            message = f"Available spots in July for Warner Brothers Studio Tour on: {', '.join(new_dates)}"
            print(message)
            send_telegram_message(message)
            notified_dates.update(new_dates)  # Add new dates to the notified set
        else:
            print("No new available dates in the specified range for July.")

        switch_month("August")
        print("Switched to August to maintain activity.")

        simulate_user_activity()  # Simulate user activity to keep the session alive
        time.sleep(3)

except KeyboardInterrupt:
    print("Monitoring stopped.")
    send_telegram_message("Monitoring stopped.")

# Close the browser
driver.quit()
