import os
import pdfplumber
import interpreter



def main():
    # make file is overriding previous
    if os.path.exists("pdfplumbertext.txt"):
        os.remove("pdfplumbertext.txt")

    with pdfplumber.open("Workforce_Tools_Schedule_10_2_2025.pdf") as pdf:
        for page in pdf.pages:
            raw_text = page.extract_text()
            text = interpreter.clean_extracted_text(raw_text)
            days_of_week, month, start_day, end_day, week_hours, text = interpreter.extract_information(text)
            # print("Days of Week: ", days_of_week)
            # print("Month: ", month)
            # print("Start Day: ", start_day)
            # print("End Day: ", end_day)
            # print("Week Hours: ", week_hours)

            # print(text, "\n\n")
            
            with open ("pdfplumbertext.txt", "a") as f:
                f.write(text + "\n\n")
                f.close
            
            with open ("raw_text.txt", "a") as f:
                f.write(raw_text + "\n\n")
                f.close     
            

            



if __name__ == "__main__":
    main()