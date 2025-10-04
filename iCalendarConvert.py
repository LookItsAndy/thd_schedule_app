import icalendar
from icalendar import Alarm
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

VERSION = '2.0'
PROID = '//AndyLy//THD Schedule App//EN'
CALSCALE = 'GREGORIAN'

def generate_ICS_file(shifts, selected_range):
    file_name = "thd_schedule_" + selected_range[0] + "_" + selected_range[1] +  "_" + selected_range[2] + \
    "-" + selected_range[3] + "_" + selected_range[4] + "_" + selected_range[5] + ".ics"
    
    s_shift_year = selected_range[2]
    e_shift_year = selected_range[5]
    store_location = "***REMOVED***"
    
    if (s_shift_year == e_shift_year):
        
        cal = icalendar.Calendar()
        cal.add('version', VERSION)
        cal.add('proid', PROID)
        cal.add('calscale', CALSCALE)
        print(file_name)
        
        alarm_1hr_before = Alarm()
        alarm_1hr_before.add('action', 'DISPLAY')
        alarm_1hr_before.add('description', 'Reminder')
        alarm_1hr_before.add('trigger', timedelta(hours=-1))

        for shift in shifts:
            start_dt = datetime.strptime(f'{shift.month} {shift.day} {s_shift_year} {shift.start_time}', "%b %d %Y %I:%M %p").replace(tzinfo=ZoneInfo("US/Pacific"))
            end_dt = datetime.strptime(f'{shift.month} {shift.day} {s_shift_year} {shift.end_time}', "%b %d %Y %I:%M %p").replace(tzinfo=ZoneInfo("US/Pacific"))
            event = icalendar.Event()
            event.add('summary', 'Home Depot Shift ' + shift.duration)
            event.add('dtstart' , start_dt)
            event.add('dtend', end_dt)
            event.add('dtstamp', datetime.now(tz=ZoneInfo("UTC")))
            event.add('description', shift.description)
            event.add('location', store_location)
            event.add_component(alarm_1hr_before)
            cal.add_component(event)
            
        p = Path('/Users/chan/Documents/GitHub/thd_schedule_app/thd_schedule_Oct_6_2025-Oct_26_2025.ics')
        p.unlink(missing_ok=True)
        with open(file_name, 'wb') as f:
            f.write(cal.to_ical())