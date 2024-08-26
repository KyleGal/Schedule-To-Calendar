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
from datetime import datetime

'''MODIFY INFORMATION BELOW'''
USERNAME = USERNAME_SECRET
PASSWORD = PASSWORD_SECRET

LOGIN_PAGE = "https://cas.ucdavis.edu/cas/login?service=https%3A%2F%2Fmy%2Eucdavis%2Eedu%2Flogin%2Findex%2Ecfm%3Fredirect%3DaHR0cHM6Ly9teS51Y2RhdmlzLmVkdS9pbmRleC5jZm0%3D"
SCHEDULE_URL = "https://my.ucdavis.edu/schedulebuilder/index.cfm?termCode=202403&helpTour="


'''DO NOT MODIFY BELOW'''
QUARTER_ID_XPATH = '//*[@id="pass_time_appointments"]/div[2]/div[1]'
CLASS_NAME_CLASS = 'className'
DAYS_CLASS = 'days'
CHROME_DRIVER_PATH = "/Users/kylegabrielgalvez/SP/calendar/chromedriver"

class google_calendar_object:
    def __init__(self, is_quarter=True, class_name="", days=[], start_time=datetime.now(), end_time=datetime.now(), location=""):
        self.is_quarter = is_quarter
        self.class_name = class_name
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        self.location = location


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
    return class_names


def get_class_days(driver):
    # Locate class days text
    days_elements = driver.find_elements(By.CLASS_NAME, DAYS_CLASS)
    days = []

    # Determine what days the class takes place
    for element in days_elements:
        day = []
        if 'M' in element.text:
            day.append(MO)
        if 'T' in element.text:
            day.append(TU)
        if 'W' in element.text:
            day.append(WE)
        if 'Th' in element.text:
            day.append(TH)
        if 'F' in element.text:
            day.append(FR)
        days.append(day)

    return days

def get_class_times(driver):
    # Locate class times text
    class_time_elements = driver.find_elements(By.CLASS_NAME, "class-time")
    class_times = []
    for element in class_time_elements:
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

        class_times.append([start_time, end_time])
    
    return class_times


def get_class_locations(driver):
    # Locate class location text
    bldg_elements = driver.find_elements(By.CLASS_NAME, "bldg")
    bldg_names = [element.text for element in bldg_elements]

    room_elements = driver.find_elements(By.CLASS_NAME, "room")
    room_names = [element.text for element in room_elements]

    # Process building room location
    locations = []
    for i in range(len(bldg_names)):
        locations.append(bldg_names[i] + ' ' + room_names[i])
    
    return locations


def get_weekly_schedule(username, password):
    try:
        USERNAME = username
        PASSWORD = password

        # Chrome Driver Setup
        service = Service(executable_path=CHROME_DRIVER_PATH)
        options = Options()
        options.add_argument("--headless=new")
        options.add_experimental_option("detach", True)

        driver = webdriver.Chrome(service=service, options=options)

        # Begin Gathering Schedule
        driver.get(LOGIN_PAGE)
        driver.maximize_window()

        # input login info and login
        driver.find_element(By.ID, "username").send_keys(USERNAME)
        driver.find_element(By.ID, "password").send_keys(PASSWORD + Keys.ENTER)

        # Click this is my device
        WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "trust-browser-button")))
        driver.find_element(By.ID, "trust-browser-button").click()
        print("LOGIN SUCCESSFUL")

        # get Calendar Info
        is_quarter = get_is_quarter(driver)
        class_names = get_class_names(driver)
        class_days = get_class_days(driver)
        class_times = get_class_times(driver)
        class_locations = get_class_locations(driver)

        # create Calendar events
        google_calendar_objects = []
        for i in range(len(class_names)):
            new_class = google_calendar_object(is_quarter, class_names[i], class_days[i], 
                                                class_times[i][0], class_times[i][1], class_locations[i])
            google_calendar_objects.append(new_class)
        
        print("CLASS ACQUISITION SUCCESSFUL")
        return google_calendar_objects

    except NoSuchElementException as e:
        print(f"Element not found: {e}")
    except TimeoutException as e:
        print(f"Timeout occured: {e}")
        print("Possible Incorrect Login")
    except WebDriverException as e:
        print(f"WebDriver exception occured: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        # driver clean up
        try:
            driver.close()
            driver.quit()
        except WebDriverException:
            print("Error occured while closing the driver.")
        

