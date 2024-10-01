from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from gcsa.recurrence import SU, MO, TU, WE, TH, FR, SA
from personal_info import USERNAME_SECRET, PASSWORD_SECRET
from datetime import datetime, timedelta
import random
import traceback

'''MODIFY INFORMATION BELOW'''
USERNAME = USERNAME_SECRET
PASSWORD = PASSWORD_SECRET

LOGIN_PAGE = "https://cas.ucdavis.edu/cas/login?service=https%3A%2F%2Fmy%2Eucdavis%2Eedu%2Flogin%2Findex%2Ecfm%3Fredirect%3DaHR0cHM6Ly9teS51Y2RhdmlzLmVkdS9pbmRleC5jZm0%3D"
SCHEDULE_URL = "https://my.ucdavis.edu/schedulebuilder/index.cfm?termCode=202403&helpTour="


'''DO NOT MODIFY BELOW'''
QUARTER_ID_XPATH = '//*[@id="pass_time_appointments"]/div[2]/div[1]'
CLASS_NAME_CLASS = 'className'
DAYS_CLASS = 'days'
CHROME_DRIVER_PATH = "/Users/kylegabrielgalvez/SP/ScheduleToCalendar/chromedriver-mac-arm64/chromedriver"

class google_calendar_class_object:
    def __init__(self, is_quarter=True, class_name="", days=[], start_time=datetime.now(), end_time=datetime.now(), location="", color_id=1):
        self.is_quarter = is_quarter
        self.class_name = class_name
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.location = location
        self.color_id = color_id

class google_calendar_final_object:
    def __init__(self, class_name="", start_time=datetime.now(), end_time=datetime.now(), color_id=1):
        self.class_name = class_name + " - Final"
        self.start_time = start_time
        self.end_time = end_time
        self.color_id = color_id


def get_is_quarter(driver):
    # Locate session label text
    is_quarter_elements = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, QUARTER_ID_XPATH)))
    
    # Determine if quarter or summer session
    is_quarter = True
    if "Summer Session" in is_quarter_elements.text:
        is_quarter = False
    
    return is_quarter


def get_class_names(driver):
    # Locate class name text
    class_elements = driver.find_elements(By.CLASS_NAME, CLASS_NAME_CLASS)
    class_names = [element.text for element in class_elements]

    # debug
    # print("CLASS NAME: ", class_names)
    return class_names[0]


def get_class_days(driver):
    # Locate class days text
    days_elements = driver.find_elements(By.CLASS_NAME, 'days')
    # days_text = [element.text for element in days_elements]
    

    # Determine what days the class takes place
    element = days_elements[0]
    print("DAYS: ", element.text)
    days = []
    if 'M' in element.text:
        days.append(MO)
    if 'T' in element.text:
        days.append(TU)
    if 'W' in element.text:
        days.append(WE)
    if 'R' in element.text:
        days.append(TH)
    if 'F' in element.text:
        days.append(FR)

    # debug
    # print("days debug: ", days)
    return days

def get_class_times(driver):
    # Locate class times text
    class_time_elements = driver.find_elements(By.CLASS_NAME, "class-time")

    element = class_time_elements[0]
    start_time_str, end_time_str = element.text.split('-')

    # check if AM or PM
    if 'AM' in end_time_str or 'PM' in end_time_str:
        meridiem = end_time_str[-2:]
    else:
        raise ValueError("AM or PM not specified!")
    if 'AM' not in start_time_str and 'PM' not in start_time_str:
        start_time_str += f' {meridiem}'
    
    # Time Processing
    start_time_str = start_time_str.strip()
    end_time_str = end_time_str.strip()
    datetime_format = '%I:%M %p'
    start_time = datetime.strptime(start_time_str, datetime_format).time()
    end_time = datetime.strptime(end_time_str, datetime_format).time()

    # debug
    # print("CLASS TIMES:", [start_time, end_time])
    return [start_time, end_time]


def get_class_locations(driver):
    # Locate class location text
    bldg_elements = driver.find_elements(By.CLASS_NAME, "bldg")
    bldg_names = [element.text for element in bldg_elements]

    room_elements = driver.find_elements(By.CLASS_NAME, "room")
    room_names = [element.text for element in room_elements]

    # debug
    # print("LOCATION: ", bldg_names[0] + ' ' + room_names[0])

    # Process building room location
    return bldg_names[0] + ' ' + room_names[0]

def get_final_times(driver):
    # Locate final times text
    final_elements = driver.find_elements(By.CLASS_NAME, 'final-time')
    final_times_texts = [element.text for element in final_elements]
    final_time = final_times_texts[0]

    # process final times
    final_time_text = final_time.replace('Final Exam:', '').strip()

    # check if final time for class is stated
    if final_time_text == '' or final_time_text == 'at':
        print("There is no final times stated")
        return None

    # strip out start time
    date_format = "%a. %b.%d at %I:%M%p"
    start_time = datetime.strptime(final_time_text, date_format)

    # add two hours to start time to create end time
    final_duration = timedelta(hours=2)
    end_time = start_time + final_duration

    # debug
    # print("FINAL TIMES: ", [start_time, end_time])
    return [start_time, end_time]

def get_weekly_schedule(username, password):
    try:
        # Chrome Driver Setup
        options = Options()
        options.add_argument("--headless=new")
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(options=options)

        # Begin Gathering Schedule
        driver.get(LOGIN_PAGE)
        driver.maximize_window()

        # input login info and login
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password + Keys.ENTER)

        # Click this is my device
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "trust-browser-button")))
        driver.find_element(By.ID, "trust-browser-button").click()
        print("LOGIN SUCCESSFUL")

        # get class block elements
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "class_container.content-block")))
        class_block = driver.find_elements(By.CLASS_NAME, "class_container.content-block")

        calendar_class_objects = []
        calendar_final_objects = []
        # process each class
        for each_class in class_block:
            is_quarter = get_is_quarter(each_class)
            class_names = get_class_names(each_class)
            final_time = get_final_times(each_class)

            # class color
            random_color_id = random.randint(1,11)


            event_elements = each_class.find_elements(By.CSS_SELECTOR, ".row-fluid > .row-fluid:not(.final-time)")
            for event in event_elements:
                # get each class info
                class_days = get_class_days(event)
                class_times = get_class_times(event)
                class_locations = get_class_locations(event)
            
                # create calendar class objects
                new_class = google_calendar_class_object(is_quarter, class_names, class_days, class_times[0], 
                                                        class_times[1], class_locations, random_color_id)
                calendar_class_objects.append(new_class)

            # create calendar final objects
            if final_time != None:
                new_final = google_calendar_final_object(class_names, 
                                                    final_time[0], final_time[1], random_color_id)
                calendar_final_objects.append(new_final)
        
        print("CLASS ACQUISITION SUCCESSFUL")

        # debug
        # print(calendar_class_objects)
        # print(calendar_final_objects)

        # Clean
        driver.close()
        driver.quit()
              
        return calendar_class_objects, calendar_final_objects

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
        traceback.print_exc()  # Prints the full traceback to the console
    except TimeoutException as e:
        print(f"Timeout occured: {e}")
        print("Possible Incorrect Login")
        traceback.print_exc()  # Prints the full traceback to the console
        return -1,-1
    except WebDriverException as e:
        print(f"WebDriver exception occured: {e}")
        traceback.print_exc()  # Prints the full traceback to the console
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        traceback.print_exc()  # Prints the full traceback to the console
