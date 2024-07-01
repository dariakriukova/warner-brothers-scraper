import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Telegram bot token and chat ID from environment variables
bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Function to send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    requests.post(url, data=payload)

# Set up the WebDriver (Assuming you have the appropriate driver for your browser)
driver = webdriver.Chrome()  # or webdriver.Firefox() or another browser's driver

# URL to the ticket purchasing page
ticket_url = "https://tickets.wbstudiotour.co.uk/webstore/shop/viewitems.aspx?cg=hptst2&c=tix2"

# Open the ticket purchasing page
driver.get(ticket_url)

# Function to reject cookies
def reject_cookies():
    try:
        manage_preferences_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "onetrust-pc-btn-handler"))
        )
        manage_preferences_button.click()
        print("Clicked 'Manage Preferences' button.")
        
        reject_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ot-pc-refuse-all-handler"))
        )
        reject_button.click()
        print("Clicked 'Reject' button.")
    except (NoSuchElementException, TimeoutException):
        print("Cookie buttons not found, continuing without rejecting cookies.")
    except Exception as e:
        print(f"An error occurred while rejecting cookies: {e}")

# Function to select the date and time
def select_date_and_time():
    try:
        select_date_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui-control.button.shared-calendar-button"))
        )
        select_date_button.click()
        print("Clicked 'Select date and time' button.")
    except (NoSuchElementException, TimeoutException):
        print("Select date and time button not found, could not proceed.")
    except Exception as e:
        print(f"An error occurred while selecting date and time: {e}")

# Function to simulate user activity
def simulate_user_activity():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")
    print("Simulated user activity to keep the session alive.")

# Function to extend the session if the button appears
def extend_session():
    try:
        extend_button = driver.find_element(By.CSS_SELECTOR, "button.ui-control.button.extendSession")
        extend_button.click()
        print("Extended session by clicking the button.")
    except NoSuchElementException:
        print("Extend session button not found, continuing monitoring.")

# Function to check for availability in July
def check_for_july_availability():
    available_dates = []
    try:
        month_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder$SalesChannelDetailControl$EventsDateTimeSelectorModal$EventsDateTimeSelector$CalendarSelector$MonthDropDownList"))
        )
        selected_month = month_dropdown.find_element(By.CSS_SELECTOR, "option[selected]").text
        if selected_month == "July":
            days = driver.find_elements(By.CSS_SELECTOR, ".calendar-body .day.available")
            for day in days:
                aria_label = day.get_attribute("aria-label")
                if aria_label and "07/2024" in aria_label:
                    available_dates.append(aria_label.strip())
    except NoSuchElementException:
        print("No available dates found.")
    return available_dates

# Function to filter dates within a specified range
def filter_dates(dates, start_date, end_date):
    start = datetime.strptime(start_date, "%d/%m/%Y")
    end = datetime.strptime(end_date, "%d/%m/%Y")
    return [date for date in dates if start <= datetime.strptime(date, "%d/%m/%Y") <= end]

# Function to switch to a specified month
def switch_month(month):
    try:
        month_dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder$SalesChannelDetailControl$EventsDateTimeSelectorModal$EventsDateTimeSelector$CalendarSelector$MonthDropDownList"))
        )
        selected_option = month_dropdown.find_element(By.CSS_SELECTOR, "option[selected]").text
        if selected_option != month:
            for option in month_dropdown.find_elements(By.TAG_NAME, "option"):
                if option.text == month:
                    option.click()
                    print(f"Switched to {month}")
                    WebDriverWait(driver, 10).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "option[selected]"), month)
                    )
                    break
    except NoSuchElementException:
        print(f"Month dropdown not found for {month}.")

# Function to select the first available time slot
def select_first_available_time():
    try:
        select_time_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui-control.button.select-time"))
        )
        select_time_button.click()
        print("Selected the first available time slot.")
    except NoSuchElementException:
        print("Select time button not found, could not select time.")

# Function to increase the quantity of tickets
def increase_ticket_quantity():
    try:
        increase_quantity_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.plus.typcn.typcn-plus"))
        )
        increase_quantity_button.click()
        print("Increased ticket quantity by 1.")
    except NoSuchElementException:
        print("Increase quantity button not found, could not increase ticket quantity.")

# Function to add tickets to the basket
def add_to_basket():
    try:
        add_to_basket_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui-control.button[name='ctl00$ContentPlaceHolder$SalesChannelDetailControl$SalesChannelDetailRepeater$ctl00$35479$AddToCartButton']"))
        )
        add_to_basket_button.click()
        print("Added tickets to the basket.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".shopping-basket"))
        )
    except (NoSuchElementException, TimeoutException):
        print("Add to basket button not found or timed out.")

# Function to handle additional items
def handle_additional_items():
    try:
        decline_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui-control.button[ng-click='decline()']"))
        )
        decline_button.click()
        print("Declined additional items.")
    except (NoSuchElementException, ElementClickInterceptedException):
        print("Decline button not found or not clickable, attempting to click 'Continue' button.")
        click_continue_button()

# Function to click the continue button within the specified element
def click_continue_button():
    try:
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div.checkout button.ui-control.button[type='submit'][value='Continue']"))
        )
        continue_button.click()
        print("Clicked the continue button.")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".final-checkout"))
        )
    except (NoSuchElementException, TimeoutException):
        print("Continue button not found or timed out.")

# Function to save the current page source to a file
def save_html_snapshot(filename="error_page.html"):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(driver.page_source)
    print(f"Saved HTML snapshot to {filename}")

# Main function to automate ticket purchase
def main():
    try:
        reject_cookies()
        select_date_and_time()
        
        notified_dates = set()
        start_date = "19/08/2024"
        end_date = "22/08/2024"

        while True:
            for month in ["July", "August"]:
                switch_month(month)
                available_dates = check_for_july_availability()
                filtered_dates = filter_dates(available_dates, start_date, end_date)
                new_dates = [date for date in filtered_dates if date not in notified_dates]
                if new_dates:
                    message = f"Available spots in {month} for Warner Brothers Studio Tour on: {', '.join(new_dates)}"
                    print(message)
                    send_telegram_message(message)
                    notified_dates.update(new_dates)  # Add new dates to the notified set

                    # Automate ticket selection and purchase
                    select_first_available_time()
                    increase_ticket_quantity()
                    add_to_basket()

                    # Handle additional items pages
                    handle_additional_items()
                    handle_additional_items()

                    # Click the final continue button
                    click_continue_button()

                    send_telegram_message("Ticket is in the basket.")
                    print("Ticket added to basket. Please continue the purchase manually.")
            
            # Wait for some time before checking again
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            simulate_user_activity()
            extend_session()
    except (NoSuchElementException, TimeoutException, StaleElementReferenceException) as e:
        print(f"An error occurred: {e}")
        save_html_snapshot()
    except KeyboardInterrupt:
        print("Monitoring stopped.")
        send_telegram_message("Monitoring stopped.")

    # Keep the browser open for manual continuation
    print("Script has completed. Browser will remain open for manual continuation.")
    while True:
        time.sleep(10)
        simulate_user_activity()
        extend_session()

if __name__ == "__main__":
    main()
