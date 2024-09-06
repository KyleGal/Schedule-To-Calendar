from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.recurrence import Recurrence
from gcsa.recurrence import WEEKLY
from datetime import datetime, date
from personal_info import USERNAME_SECRET, PASSWORD_SECRET
from enum import Enum
from get_schedule import get_weekly_schedule

CREDENTIALS_PATH = '/Users/kylegabrielgalvez/SP/calendar/credentials.json'
MINUTES_BEFORE_POPUP_REMINDER = 30
FREQUENCY_OF_EVENTS = WEEKLY

WEEKS_IN_SESSION = 10 # default is 10 for quarter

class LoginResult(Enum):
    INVALID_LOGIN = -1
    VALID_LOGIN = 0
    NO_CLASSES_FOUND = 1


def add_to_calendar(username, password, start_date_str):
    try:
        gc = GoogleCalendar(credentials_path=CREDENTIALS_PATH)

        # get calendar info to translate to google calendar events
        calendar_class_objects, calendar_final_objects = get_weekly_schedule(username, password)
        
        # debug
        # print(calendar_class_objects)
        # print(calendar_final_objects)

        # Invalid Login
        if calendar_class_objects == -1 or calendar_final_objects == -1:
            return LoginResult.INVALID_LOGIN

        if calendar_class_objects == None:
            return LoginResult.NO_CLASSES_FOUND
        else:
            
            # add classes to calendar
            for calendar_object in calendar_class_objects:
                # Check if quarter or summer session
                if calendar_object.is_quarter == False:
                    WEEKS_IN_SESSION = 6
                num_occurences = WEEKS_IN_SESSION * len(calendar_object.days)

                # Process datetimes
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
                start_time = datetime.combine(start_date, calendar_object.start_time)
                end_time = datetime.combine(start_date, calendar_object.end_time)
                
                # add events to calendar
                # TODO: Distinguish between lecture, discussion, and lab
                event = Event(calendar_object.class_name, 
                            start=start_time, 
                            end=end_time,
                            location=calendar_object.location,
                            minutes_before_popup_reminder=MINUTES_BEFORE_POPUP_REMINDER,
                            recurrence = [
                                Recurrence.rule(freq=FREQUENCY_OF_EVENTS,
                                                count=num_occurences,
                                                by_week_day=calendar_object.days)],
                            color_id = calendar_object.color_id)
                # print(event)
                gc.add_event(event)
        
        # add finals to calendar
        if calendar_final_objects == []:
            print("NO FINALS SHOWN")
        else:
            for final_object in calendar_final_objects:
                # add events to calendar
                event = Event(final_object.class_name, 
                            start=final_object.start_time, 
                            end=final_object.end_time,
                            minutes_before_popup_reminder=MINUTES_BEFORE_POPUP_REMINDER,
                            color_id = final_object.color_id)
                # print(event)
                gc.add_event(event)

        return LoginResult.VALID_LOGIN
    except TypeError as e:
        print(f"Type error exception occured: {e}")
        print("Invalid Data Obtained")