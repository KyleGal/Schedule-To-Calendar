from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from gcsa.recurrence import Recurrence
from gcsa.recurrence import WEEKLY
from datetime import datetime, date
import random
from get_schedule import get_weekly_schedule

CREDENTIALS_PATH = '/Users/kylegabrielgalvez/SP/calendar/credentials.json'
MINUTES_BEFORE_POPUP_REMINDER = 30
FREQUENCY_OF_EVENTS = WEEKLY

WEEKS_IN_SESSION = 10 # default is 10 for quarter


def add_to_calendar(username, password, start_date_str):
    # get calendar info to translate to google calendar events
    google_calendar_objects = get_weekly_schedule(username, password)

    for calendar_object in google_calendar_objects:
        if calendar_object.is_quarter == False:
            WEEKS_IN_SESSION = 6
        num_occurences = WEEKS_IN_SESSION * len(calendar_object.days)

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        start_time = datetime.combine(start_date, calendar_object.start_time)
        end_time = datetime.combine(start_date, calendar_object.end_time)
        
        # add events to calendar
        # TODO: Distinguish between lecture, discussion, and lab
        gc = GoogleCalendar(credentials_path=CREDENTIALS_PATH)
        random_color_id = random.randint(1,11)
        
        event = Event(calendar_object.class_name, 
                    start=start_time, 
                    end=end_time,
                    location=calendar_object.location,
                    minutes_before_popup_reminder=MINUTES_BEFORE_POPUP_REMINDER,
                    recurrence = [
                        Recurrence.rule(freq=FREQUENCY_OF_EVENTS,
                                        count=num_occurences,
                                        by_week_day=calendar_object.days)],
                    color_id = random_color_id)
        gc.add_event(event)

        # TODO: Add final exam date
        