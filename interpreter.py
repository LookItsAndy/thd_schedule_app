import re
import Shift

MONTH = r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
DAY = r'([1-9]|[12][0-9]|3[01])'
YEAR = r'(\d{4})'
HOURS = r'(\d{1,2}:\d{2})'
TIME = r'(\d{1,2}\sPM|AM)'


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
    #SHIFT_PATTERN = fr'{MONTH}\s{TIME}\s-\s{TIME}\s[{HOURS}]\s {DAY}'
    week = re.finditer(WEEK_HEADER_PATTERN, clean_text)
    clean_text = re.sub(fr'{MONTH}\s{DAY}\s*-\s*{DAY}\s*{HOURS}\s*hours\s*', "", clean_text)

    for match in week:
        print("Week:", match.group(1), match.group(2), "-", match.group(3))
        print("Month:", match.group(1))
        print("Start Day:", match.group(2))
        print("End Day:", match.group(3))
        print("Week Hours:", match.group(4))
        
        
    return clean_text

