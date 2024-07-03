import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException, StaleElementReferenceException
from config import BOT_TOKEN, CHAT_ID

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(url, data=payload)

def simulate_user_activity(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(0.5)
    driver.execute_script("window.scrollTo(0, 0);")
    print("Simulated user activity to keep the session alive.")

def extend_session(driver):
    try:
        extend_button = driver.find_element(By.CSS_SELECTOR, "button.ui-control.button.extendSession")
        extend_button.click()
        print("Extended session by clicking the button.")
    except NoSuchElementException:
        print("Extend session button not found, continuing monitoring.")

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
