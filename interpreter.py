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

    # supports cross-month
    WEEK_HEADER_PATTERN = fr'({MONTH})\s{DAY}\s*-\s*(?:{MONTH}\s*)?{DAY}\s*{HOURS}'
    SHIFT_PATTERN = fr'({MONTH})\s{TIME}\s-\s{TIME}\s\[{HOURS}\]\s{DAY} (.*)'
    
    shift_objects = []
    week = re.finditer(WEEK_HEADER_PATTERN, clean_text)
    clean_text = re.sub(fr'{WEEK_HEADER_PATTERN}\s*hours\s*', "", clean_text)

    for match in week:
        days_of_week = match.group(1) + " " + match.group(2) + " - " + match.group(3)
        month = match.group(1)    
        start_day = match.group(2)
        end_day = match.group(3)
        week_hours = match.group(4)
        
    for line in clean_text.splitlines():
        #print(line)
        match = re.match(SHIFT_PATTERN, line)
        if match:
            #print("match groups" + str(match.groups()))
            month = match.group(1)
            day = match.group(5)
            start_time = match.group(2)
            end_time = match.group(3)
            duration = "[" + match.group(4) + "]"
            description = match.group(6)
            shift = Shift.Shift(month, day, start_time, end_time, duration, description, days_of_week, week_hours)
            shift_objects.append(shift)

        
           
        
    return clean_text, shift_objects

