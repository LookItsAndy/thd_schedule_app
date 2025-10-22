from flask import Flask, request, send_file, abort
import os
from io import BytesIO
from shift_parser import parse_pdf, build_ics_bytes


app = Flask("__name__")
app.config["MAXIMUM_CONTENT_LENGTH"] = 10 * 1024 * 1024 # 10 MB upload limit

@app.route("/")
def home():
    return '''
    <h2>Uplaod your Workforce Tools PDF at /upload</h2>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept=".pdf">
        <input type="submit" value="Upload">
    </form>
    '''
@app.route("/upload", methods=["POST"])
def upload():
    # Check if file exists in request
    if "file" not in request.files:
        abort(400, "File not found")
    f = request.files["file"]
    
    if not f or f.filename == "":
        abort(400, "No file selected")
    
    if "pdf" not in f.mimetype.lower():
        abort(400, "Please upload a PDF file")
        
        
    # Parse PDF and build ICS
    shifts, selected_range = parse_pdf(f.stream)



    if not shifts:
        abort(422, "No shifts found in the upload file")
        
        
    ics_bytes, file_name = build_ics_bytes(shifts, selected_range)
    
    return send_file(BytesIO(ics_bytes), mimetype="text/calendar", as_attachment=True,download_name=file_name + '.ics')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)), debug=True)