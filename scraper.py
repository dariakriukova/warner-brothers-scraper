import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException, ElementClickInterceptedException
from utils import send_telegram_message, extend_session, filter_dates

driver = webdriver.Chrome()  # or webdriver.Firefox() or another browser's driver

ticket_url = "https://tickets.wbstudiotour.co.uk/webstore/shop/viewitems.aspx?cg=hptst2&c=tix2"
driver.get(ticket_url)

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
    except NoSuchElementException:
        print("Cookie buttons not found, continuing without rejecting cookies.")
    except Exception as e:
        print(f"An error occurred while rejecting cookies: {e}")

def check_for_availability(month):
    month_dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder$SalesChannelDetailControl$EventsDateTimeSelectorModal$EventsDateTimeSelector$CalendarSelector$MonthDropDownList"))
    )
    selected_month = month_dropdown.find_element(By.CSS_SELECTOR, "option[selected]").text
    available_dates = []
    if selected_month == month:
        days = driver.find_elements(By.CSS_SELECTOR, ".calendar-body .day.available")
        for day in days:
            aria_label = day.get_attribute("aria-label")
            if aria_label:
                available_dates.append(aria_label.strip())
    return available_dates

def switch_month(month, retries=3):
    for attempt in range(retries):
        try:
            month_dropdown = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.NAME, "ctl00$ContentPlaceHolder$SalesChannelDetailControl$EventsDateTimeSelectorModal$EventsDateTimeSelector$CalendarSelector$MonthDropDownList"))
            )
            selected_option = month_dropdown.find_element(By.CSS_SELECTOR, "option[selected]").text
            if selected_option != month:
                month_options = month_dropdown.find_elements(By.TAG_NAME, "option")
                for option in month_options:
                    if option.text == month:
                        option.click()
                        print(f"Switched to {month}")
                        WebDriverWait(driver, 20).until(
                            EC.text_to_be_present_in_element((By.CSS_SELECTOR, "option[selected]"), month)
                        )
                        return
            else:
                print(f"Already on {month}")
                return
        except TimeoutException as e:
            print(f"TimeoutException on attempt {attempt + 1} while switching to {month}: {e}")
        except Exception as e:
            print(f"Exception on attempt {attempt + 1} while switching to {month}: {e}")
        time.sleep(2)  # Wait before retrying
    print(f"Failed to switch to {month} after {retries} attempts")

def select_first_available_time_for_date(target_date):
    try:
        day_elements = driver.find_elements(By.CSS_SELECTOR, ".calendar-body .day.available")
        for day_element in day_elements:
            aria_label = day_element.get_attribute("aria-label")
            if aria_label and aria_label.strip() == target_date:
                day_element.click()
                break
        
        select_time_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui-control.button.select-time"))
        )
        select_time_button.click()
        print("Selected the first available time slot for the date:", target_date)
    except NoSuchElementException:
        print("Select time button not found, could not select time for the date:", target_date)

def increase_ticket_quantity():
    try:
        increase_quantity_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.plus.typcn.typcn-plus"))
        )
        increase_quantity_button.click()
        print("Increased ticket quantity by 1.")
    except NoSuchElementException:
        print("Increase quantity button not found, could not increase ticket quantity.")
    except StaleElementReferenceException:
        print("Stale element reference exception caught. Retrying to increase ticket quantity.")
        increase_ticket_quantity()

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
    except NoSuchElementException:
        print("Add to basket button not found, could not add tickets to basket.")
    except TimeoutException:
        print("Timed out waiting for basket confirmation, assuming add to basket was successful.")

def handle_additional_items():
    try:
        decline_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ui-control.button[ng-click='decline()']"))
        )
        decline_button.click()
        print("Declined additional items.")
    except NoSuchElementException:
        print("Decline button not found, attempting to click 'Continue' button instead.")
        click_continue_button()
    except ElementClickInterceptedException:
        print("Decline button not clickable, attempting to click 'Continue' button instead.")
        click_continue_button()
    except Exception as e:
        print(f"An error occurred: {e}")

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
    except NoSuchElementException:
        print("Continue button not found, could not proceed.")
    except Exception as e:
        print(f"An error occurred: {e}")
