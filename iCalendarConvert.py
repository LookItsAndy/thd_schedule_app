import icalendar, time
from icalendar import Alarm
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

VERSION = '2.0'
PRODID = '//Andy//Orange Calendar//EN'
CALSCALE = 'GREGORIAN'

def generate_ICS_bytes(shifts, selected_range):
    file_name = "thd_schedule_" + selected_range[0] + "_" + selected_range[1] +  "_" + selected_range[2] + \
    "-" + selected_range[3] + "_" + selected_range[4] + "_" + selected_range[5]
    
    s_shift_year = selected_range[2]
    e_shift_year = selected_range[5]
    store_location = "[STORE_LOCATION_HERE]"
    
    if (s_shift_year == e_shift_year):
        
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
            
            start_dt = datetime.strptime(f'{shift.month} {shift.day} {s_shift_year} {shift.start_time}', "%b %d %Y %I:%M %p").replace(tzinfo=ZoneInfo("US/Pacific"))
            end_dt = datetime.strptime(f'{shift.month} {shift.day} {s_shift_year} {shift.end_time}', "%b %d %Y %I:%M %p").replace(tzinfo=ZoneInfo("US/Pacific"))
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