import pdfplumber
import interpreter
import iCalendarConvert


def parse_pdf(file_obj):
    shifts, selected_range = [], []

    with pdfplumber.open(file_obj) as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()
            text_with_header, selected_range = interpreter.clean_extracted_text(raw_text)
            
            cleaned_text, page_shifts = interpreter.extract_information(text_with_header)
            
            shifts.extend(page_shifts)
    return shifts, selected_range



def build_ics_bytes(shifts, selected_range, location="") -> bytes:
    cal, file_name = iCalendarConvert.generate_ICS_bytes(shifts, selected_range, location)

    return cal, file_name
            