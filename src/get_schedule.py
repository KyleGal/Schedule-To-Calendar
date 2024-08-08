from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from gcsa.recurrence import SU, MO, TU, WE, TH, FR, SA

'''MODIFY INFORMATION BELOW'''
USERNAME = 'kgalvez'
PASSWORD = 'BlazingWater12345'

LOGIN_PAGE = "https://cas.ucdavis.edu/cas/login?service=https%3A%2F%2Fmy%2Eucdavis%2Eedu%2Flogin%2Findex%2Ecfm%3Fredirect%3DaHR0cHM6Ly9teS51Y2RhdmlzLmVkdS9pbmRleC5jZm0%3D"
SCHEDULE_URL = "https://my.ucdavis.edu/schedulebuilder/index.cfm?termCode=202403&helpTour="

NUMBER_OF_CLASSES_IN_SCHEDULE = 6


'''DO NOT MODIFY BELOW'''
google_calendar_objects = []
class google_calendar_object:
    def __init__(self, is_quarter=True, class_name="", days=[], time="", location=""):
        self.is_quarter = is_quarter
        self.class_name = class_name
        self.days = days
        self.time = time
        self.location = location

# Chrome Driver Setup
CHROME_DRIVER_PATH = "/Users/kylegabrielgalvez/Desktop/SP/calendar/chromedriver"

service = Service(executable_path=CHROME_DRIVER_PATH)
options = Options()
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
is_quarter_elements = WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="pass_time_appointments"]/div[2]/div[1]')))

is_quarter = True
if "Summer Session" in is_quarter_elements.text:
    is_quarter = False
print(is_quarter)


class_elements = driver.find_elements(By.CLASS_NAME, "className")

class_names = [element.text for element in class_elements]
print(class_names)


days_elements = driver.find_elements(By.CLASS_NAME, "days")
days = []
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


for i in range(len(class_names)):
    new_class = google_calendar_object(is_quarter, class_names[i], days[i], )

driver.quit()




# valid_days = ['M', 'T', 'W', 'TR', 'F']
# for i,class_name in enumerate(class_names):
#     # find days the class is
#     days = []
#     j = 0
#     while sched_data[i][j] in valid_days:
#         days.append(sched_data[i][j])
#         j += 1


