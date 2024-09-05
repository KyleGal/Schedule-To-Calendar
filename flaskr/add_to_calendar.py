from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.recurrence import Recurrence
from gcsa.recurrence import WEEKLY
from datetime import datetime, date
from personal_info import USERNAME_SECRET, PASSWORD_SECRET

from get_schedule import get_weekly_schedule

CREDENTIALS_PATH = '/Users/kylegabrielgalvez/SP/calendar/credentials.json'
MINUTES_BEFORE_POPUP_REMINDER = 30
FREQUENCY_OF_EVENTS = WEEKLY

WEEKS_IN_SESSION = 10 # default is 10 for quarter


def add_to_calendar(username, password, start_date_str):
    try:
        # gc = GoogleCalendar(credentials_path=CREDENTIALS_PATH)

        # get calendar info to translate to google calendar events
        calendar_class_objects, calendar_final_objects = get_weekly_schedule(username, password)
        if calendar_class_objects == None:
            print("NO CLASSES FOUND")
            return -1
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
                print(event)
                # gc.add_event(event)
        
        # add finals to calendar
        if calendar_final_objects == None:
            print("NO FINALS SHOWN")
        else:
            for final_object in calendar_final_objects:
                # add events to calendar
                event = Event(final_object.class_name, 
                            start=final_object.start_time, 
                            end=final_object.end_time,
                            minutes_before_popup_reminder=MINUTES_BEFORE_POPUP_REMINDER,
                            color_id = final_object.color_id)
                print(event)
                # gc.add_event(event)

        return 0
    except TypeError as e:
        print(f"Type error exception occured: {e}")
        print("Invalid Data Obtained")