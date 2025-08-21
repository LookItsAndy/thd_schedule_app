import os
import pdfplumber
import interpreter


def main():
    if os.path.exists("pdfplumbertext.txt"):
        os.remove("pdfplumbertext.txt")

    with pdfplumber.open("multiplepages.pdf") as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            text = interpreter.clean_extracted_text(text)
            text = interpreter.extract_information(text)

            print(text + "\n\n")
            
            with open ("pdfplumbertext.txt", "a") as f:
                f.write(text + "\n\n")

            



if __name__ == "__main__":
    main()