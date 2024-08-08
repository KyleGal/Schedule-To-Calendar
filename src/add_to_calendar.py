from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.recurrence import Recurrence
from gcsa.recurrence import SU, MO, TU, WE, TH, FR, SA
from gcsa.recurrence import SECONDLY, MINUTELY, HOURLY, \
                            DAILY, WEEKLY, MONTHLY, YEARLY
import datetime
from datetime import datetime
import random

WEEKS_IN_SS = 6
WEEKS_IN_QUARTER = 10

ADD_TO_CALENDAR = 1

while ADD_TO_CALENDAR == 1:
    continu = input("Would you like to add an event to your calendar? (Y) or (N)")

    if continu == 'N':
        ADD_TO_CALENDAR = 0
        continue
    elif continu == 'Y':
        pass
    else:
        print("Not a valid input!")
        continue


    
    days_occuring = [MO, WE, FR]
    num_occurences = WEEKS_IN_QUARTER * len(days_occuring)

    # gather info from school website


    quarter = input("Is this for summer session or quarter? (SS) or (Q)")

    if quarter == "SS":
        num_occurences = WEEKS_IN_SS * len(days_occuring)

    
    start_date = input("When does your session start? (mm/dd/yy)")

    lecture_time_start = input("When does your lecture start? (hh:mm) 24hr clock")
    start_date_time = start_date + " " + lecture_time_start
    start_datetime_object = datetime.strptime(start_date_time, '%m/%d/%y %H:%M')
    
    lecture_time_end = input("When does your lecture end? (hh:mm) 24hr clock")
    end_date_time = start_date + " " + lecture_time_end
    end_datetime_object = datetime.strptime(end_date_time, '%m/%d/%y %H:%M')
    

    # add event to calendar
    gc = GoogleCalendar(credentials_path='/Users/kylegabrielgalvez/Desktop/SP/calendar/credentials.json')

    random_color_id = random.randint(1,11)
    
    event = Event('ECS 145 - Lecture', 
                  start=start_datetime_object, 
                  end=end_datetime_object, 
                  minutes_before_popup_reminder=30,
                  recurrence = [
                      Recurrence.rule(freq=WEEKLY,
                                      count=num_occurences,
                                      by_week_day=days_occuring)],
                  color_id = random_color_id)
    gc.add_event(event)

    # ask for final exam date

    # add event to calendar
    