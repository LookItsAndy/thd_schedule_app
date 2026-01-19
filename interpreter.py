import re
import Shift

MONTH = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
DAY = r'(3[01]|2[0-9]|1[0-9]|[1-9])'
YEAR = r'(\d{4})'
HOURS = r'(\d{1,2}:\d{2})'
TIME = r'(\d{1,2}:\d{2}\s(?:PM|AM))'




'''
Normalizes the text by putting everything on single line. 
Removes unneeded text.
Splits shifts into new lines 
'''
def clean_extracted_text(text):
    
    text = text.strip()
    text = " ".join(text.split())
    
    match = re.search(fr'({MONTH})\s{DAY},\s{YEAR}\s-\s({MONTH})\s{DAY},\s{YEAR}\s', text)
    
    if not match:
        raise ValueError("Could not match headers in PDF file!")
    
    selected_range = match.groups()
    text = re.sub(fr'Workforce Tools Schedule - Selected Date Range {MONTH}\s{DAY},\s{YEAR}\s-\s{MONTH}\s{DAY},\s{YEAR}\s' , "", text)
    text = re.sub(r'Shared or printed versions of the schedule may not reflect the most current information. ' \
        'All associates are responsible for regularly checking the app for any schedule updates. ','',text)

    pattern = rf'(?<!-\s)({MONTH}\s{DAY})(?!\s*-\s*{MONTH}\s{DAY})'
    text = re.sub(pattern, r'\n\1', text)

    # Clean up leading/trailing whitespace
    text = text.lstrip("\n")
    lines = [line.rstrip() for line in text.splitlines()]
    text = "\n".join(lines)
    
    text_with_header = text
        
    return text_with_header, selected_range


'''
Needs clean text to be passed through
Processes the Week Header and removes. 
'''
def extract_information(clean_text):
# potential issue: when shift week goes from one month to another. Sep 21 - Oct 5
# potential way to detect, compare first start day to end day and if greater than
# i will figure out later
    
    WEEK_HEADER_PATTERN = (
        fr'({MONTH})\s'                             # Ex: Oct       '[Month] '
        fr'{DAY}\s-'                                # Ex: 27        '[Day] -'
        fr'(?:\s({MONTH}))?\s{DAY}\s'               # Ex: Nov 2     '[Maybe Month] [Day] '
        fr'{HOURS}'                                 # Ex: 19:30     '[Hours]'
    )
    SHIFT_PATTERN = (
        fr'({MONTH})\s'                             # Ex: Oct
        fr'{TIME}\s-\s{TIME}\s'                     # Ex: 2:30 PM - 10:00 PM
        fr'\[{HOURS}\]\s'                           # Ex: [7:00]
        fr'{DAY}\s'                                 # Ex: 27
        r'(\d{4})\s-\sStore\s(\d{2,3})\s-\s(.*)'    # Ex: 0105 - Store 094 - Order Fulfillment Associate
    )
    
    
    shift_objects = []
    week_header = re.finditer(WEEK_HEADER_PATTERN, clean_text)
    clean_text = re.sub(fr'{MONTH}\s{DAY}\s*-\s*{DAY}\s*{HOURS}\s*hours\s*', "", clean_text)
    
    # set to nothing in case no match found in week_header to avoid program crashing
    days_of_week = ""
    week_hours = ""
    
    for match in week_header:

        start_month = match.group(1)    
        start_day = match.group(2)
        
        end_month = match.group(3)
        end_day = match.group(4)
        
        week_hours = match.group(5)
    
        if end_month != None:
            days_of_week = f'{start_month} {start_day} - {end_month} {end_day}'
        else:
            days_of_week = f'{start_month} {start_day} - {end_day}'
            
        
    for line in clean_text.splitlines():
        match = re.match(SHIFT_PATTERN, line)
        
        if match:
            month = match.group(1)
            day = match.group(5)
            start_time = match.group(2)
            end_time = match.group(3)
            duration = "[" + match.group(4) + "]"
            store_number = match.group(6)
            department_number = match.group(7)
            job_description = match.group(len(match.groups())) # Always set description to last capturing match which is job description
            shift = Shift.Shift(month, day, start_time, end_time, duration, store_number, department_number, job_description, days_of_week, week_hours)
            shift_objects.append(shift)

        
           
        
    return clean_text, shift_objects

