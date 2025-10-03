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
    text = re.sub(fr'Workforce Tools Schedule - Selected Date Range {MONTH}\s{DAY},\s{YEAR}\s-\s{MONTH}\s{DAY},\s{YEAR}\s' , "", text)
    text = re.sub(r'Shared or printed versions of the schedule may not reflect the most current information. ' \
        'All associates are responsible for regularly checking the app for any schedule updates. ','',text)

    temptext = ""
    parts = re.split(fr'(?={MONTH})', text)
    for part in parts:
        temptext = temptext + "\n" + part

    #remove empty lines at beginning
    
    text = temptext.lstrip("\n")
    lines = text.splitlines()
    lines = [line.rstrip() for line in lines]
    text = "\n".join(lines)
    return text



'''
Needs clean text to be passed through
Processes the Week Header and removes. 
'''
def extract_information(clean_text):
# potential issue: when shift week goes from one month to another. Sep 21 - Oct 5
# potential way to detect, compare first start day to end day and if greater than
# i will figure out later
    WEEK_HEADER_PATTERN = fr'({MONTH})\s{DAY}\s*-\s*{DAY}\s*{HOURS}'
    SHIFT_PATTERN = fr'({MONTH})\s{TIME}\s-\s{TIME}\s\[{HOURS}\]\s{DAY} (.*)'
    
    shift_objects = []
    week = re.finditer(WEEK_HEADER_PATTERN, clean_text)
    clean_text = re.sub(fr'{MONTH}\s{DAY}\s*-\s*{DAY}\s*{HOURS}\s*hours\s*', "", clean_text)

    for match in week:
        f_days_of_week = match.group(1) + " " + match.group(2) + " - " + match.group(3)
        f_month = match.group(1)    
        f_start_day = match.group(2)
        f_end_day = match.group(3)
        f_week_hours = match.group(4)
        
        # print("Week:", match.group(1), match.group(2), "-", match.group(3))
        # print("Month:", match.group(1))
        # print("Start Day:", match.group(2))
        # print("End Day:", match.group(3))
        # print("Week Hours:", match.group(4))
    
    for line in clean_text.splitlines():
        print(line)
        match = re.match(SHIFT_PATTERN, line)
        if match:
            print("match groups" + str(match.groups()))
            month = match.group(1)
            day = match.group(5)
            start_time = match.group(2)
            end_time = match.group(3)
            duration = "[" + match.group(4) + "]"
            description = match.group(6) + " - Week Hours: [" + f_week_hours + "]"
            shift = Shift.Shift(month, day, start_time, end_time, duration, description)
            shift_objects.append(shift)
            print(shift.toString())
        
           
        
    return f_days_of_week, f_month, f_start_day, f_end_day, f_week_hours, clean_text

