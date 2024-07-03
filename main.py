from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time

from scraper import driver, reject_cookies, check_for_availability, switch_month, select_first_available_time_for_date, increase_ticket_quantity, add_to_basket, handle_additional_items, click_continue_button
from utils import send_telegram_message, simulate_user_activity, extend_session, filter_dates
from config import BOT_TOKEN, CHAT_ID

reject_cookies()

# Find and click the button to select date and time
select_date_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.shared-calendar-button"))
)
select_date_button.click()

notified_dates = set()
start_date = "01/07/2024"
end_date = "31/07/2024"

try:
    extend_session(driver)
    
    while True:
        switch_month("July")
        available_dates = check_for_availability("July")
        filtered_dates = filter_dates(available_dates, start_date, end_date)
        new_dates = [date for date in filtered_dates if date not in notified_dates]
        if new_dates:
            for target_date in new_dates:
                message = f"Available spots in July for Warner Brothers Studio Tour on: {target_date}"
                print(message)
                send_telegram_message(message)
                notified_dates.add(target_date)
                
                select_first_available_time_for_date(target_date)
                increase_ticket_quantity()
                add_to_basket()
                
                handle_additional_items()
                handle_additional_items()
                
                click_continue_button()
                
                send_telegram_message("Ticket is in the basket.")
                print("Ticket added to basket. Please continue the purchase manually.")
        
        switch_month("August")
        available_dates = check_for_availability("August")
        filtered_dates = filter_dates(available_dates, start_date, end_date)
        new_dates = [date for date in filtered_dates if date not in notified_dates]
        if new_dates:
            for target_date in new_dates:
                message = f"Available spots in August for Warner Brothers Studio Tour on: {target_date}"
                print(message)
                send_telegram_message(message)
                notified_dates.add(target_date)
                
                select_first_available_time_for_date(target_date)
                increase_ticket_quantity()
                add_to_basket()
                
                handle_additional_items()
                handle_additional_items()
                
                click_continue_button()
                
                send_telegram_message("Ticket is in the basket.")
                print("Ticket added to basket. Please continue the purchase manually.")
        
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        simulate_user_activity(driver)
        extend_session(driver)
except KeyboardInterrupt:
    print("Monitoring stopped.")
    send_telegram_message("Monitoring stopped.")

print("Script has completed. Browser will remain open for manual continuation.")
while True:
    time.sleep(10)
    simulate_user_activity(driver)
    extend_session(driver)
