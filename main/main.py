from pathlib import Path
import pdfplumber
import interpreter
import iCalendarConvert


def main():
    shifts = []
    selected_range = []
    
    # make file is overriding previous
    p = Path("/Users/chan/Documents/GitHub/thd_schedule_app/pdfplumbertext.txt")
    if p.exists:
        p.unlink(missing_ok=True)

    with pdfplumber.open("Workforce_Tools_Schedule_10_2_2025.pdf") as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()
            text, selected_range = interpreter.clean_extracted_text(raw_text)
            page_shifts, text = interpreter.extract_information(text, selected_range)
            
            shifts.extend(page_shifts)
            with open ("pdfplumbertext.txt", "a") as f:
                f.write(text + "\n\n")
                
            with open ("raw_text.txt", "a") as f:
                f.write(raw_text + "\n\n")
                
    iCalendarConvert.generate_ICS_file(shifts, selected_range)      
                
            

            



if __name__ == "__main__":
    main()