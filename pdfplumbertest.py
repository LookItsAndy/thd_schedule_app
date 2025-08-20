import os
import pdfplumber
import re


def main():
    if os.path.exists("pdfplumbertext.txt"):
        os.remove("pdfplumbertext.txt")

    with pdfplumber.open("multiplepages.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            text = clean_extracted_text(text)
            with open ("pdfplumbertext.txt", "a") as f:
                f.write(text + "\n\n")

            print(text, "\n\n\n")


def clean_extracted_text(text):
    month_day = r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}'
    text = text.strip()
    text = " ".join(text.split())
    text = re.sub(fr'Workforce Tools Schedule - Selected Date Range {month_day}, \d{{4}} - {month_day}, \d{{4}} ' , "", text)
    text = re.sub(r'Shared or printed versions of the schedule may not reflect the most current information. ' \
    'All associates are responsible for regularly checking the app for any schedule updates.','',text)
    return text


if __name__ == "__main__":
    main()