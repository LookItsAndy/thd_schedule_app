import icalendar, time
from icalendar import Alarm
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

VERSION = '2.0'
PRODID = '//Andy//Orange Calendar//EN'
CALSCALE = 'GREGORIAN'

def generate_ICS_bytes(shifts, selected_range, location=""):
    file_name = "thd_schedule_" + selected_range[0] + "_" + selected_range[1] +  "_" + selected_range[2] + \
    "-" + selected_range[3] + "_" + selected_range[4] + "_" + selected_range[5] + ".ics"

    s_shift_year = int(selected_range[2])
    e_shift_year = int(selected_range[5])
    store_location = location if location else ""   # if no location, leave blank

    cal = icalendar.Calendar()
    cal.add('version', VERSION)
    cal.add('prodid', PRODID)
    cal.add('calscale', CALSCALE)

    alarm_1hr_before = Alarm()
    alarm_1hr_before.add('action', 'DISPLAY')
    alarm_1hr_before.add('description', 'Reminder')
    alarm_1hr_before.add('trigger', timedelta(hours=-1))

    for shift in shifts:
        uid = shift.make_uid()
        now_utc = datetime.now(tz=ZoneInfo("UTC"))

        # Determine correct year for this shift based on month
        # If schedule spans years (e.g., Dec 2025 - Jan 2026), Jan shifts should use end year
        shift_year = s_shift_year
        if s_shift_year != e_shift_year and shift.month in ('Jan', 'Feb'):
            shift_year = e_shift_year

        start_dt = datetime.strptime(f'{shift.month} {shift.day} {shift_year} {shift.start_time}', "%b %d %Y %I:%M %p").replace(tzinfo=ZoneInfo("US/Pacific"))
        end_dt = datetime.strptime(f'{shift.month} {shift.day} {shift_year} {shift.end_time}', "%b %d %Y %I:%M %p").replace(tzinfo=ZoneInfo("US/Pacific"))

        # Handle overnight shifts (end time before start time means it ends the next day)
        if end_dt <= start_dt:
            end_dt += timedelta(days=1)

        event = icalendar.Event()
        event.add('summary', 'Home Depot Shift ' + shift.duration)
        event.add('dtstart' , start_dt)
        event.add('dtend', end_dt)

        event.add('uid', uid)
        event.add('dtstamp', now_utc)
        event.add('lastmodified', now_utc)
        event.add('sequence', int(time.time()))     # Epoch time ensures new file has higher sequence

        event.add('description', shift.description)
        event.add('location', store_location)
        event.add_component(alarm_1hr_before)
        cal.add_component(event)

    return cal.to_ical(), file_name 