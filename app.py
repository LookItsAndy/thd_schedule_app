import os, secrets
from dotenv import load_dotenv
from flask import Flask, request, send_file, abort, flash, redirect, url_for, render_template, Response
from io import BytesIO
from shift_parser import parse_pdf, build_ics_bytes

ics_store = {}

load_dotenv()
app = Flask("__name__")
app.config["MAXIMUM_CONTENT_LENGTH"] = 10 * 1024 * 1024 # 10 MB upload limit
app.secret_key = os.environ.get("SECRET_KEY")

@app.route("/", methods=["GET"])
def home():
    return render_template('home.html')
   
@app.route("/upload", methods=["POST"])
def upload():
    # Check if file exists in request
    f = request.files["file"]
    
    if "file" not in request.files:
        #abort(400, "File not found")
        flash("File not found")
        return redirect(url_for("home"))
    
    if not f or f.filename == "":
        #abort(400, "No file selected")
        flash("No file selected")
        return redirect(url_for("home"))
    
    if "pdf" not in f.mimetype.lower():
        #abort(400, "Please upload a PDF file")
        return redirect(url_for("home"))
        
    # Parse PDF and build ICS
    try:
        shifts, selected_range = parse_pdf(f.stream)
    except ValueError as e:
        flash(str(e))
        return redirect(url_for("home"))
    except Exception:
        flash("Couldn't parse file, please try another")
        return redirect(url_for("home"))

    if not shifts:
        flash("No shifts found in the upload file")
        return redirect(url_for("home"))
        
        
    ics_bytes, file_name = build_ics_bytes(shifts, selected_range)
    ics_stream = BytesIO(ics_bytes)
    token = secrets.token_hex(8)
    ics_store[token] = (ics_bytes, file_name)
    
    #return send_file(BytesIO(ics_bytes), mimetype="text/calendar", as_attachment=True,download_name=file_name + '.ics')
    return redirect(url_for("download_ics", token=token))
    
    
@app.route("/download/<token>.ics", methods=["GET"])
def download_ics(token):
    entry = ics_store.get(token)
    if entry is None:
        return "File not found", 404
    
    ics_bytes, file_name = entry
    
    return Response(
        ics_bytes,
        mimetype="text/calendar",
        headers={
            "Content-Disposition": f'attachment; filename="{file_name}"'
        }
    )
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)), debug=True)
    