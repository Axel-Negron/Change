# flask_app.py
from flask import Flask, send_file
import os

app = Flask(__name__)

# Define the path to the pre-made zip file
zip_file_path = "share.txt"

@app.route("/download")
def download():
    print("Entered download route")
    with open(zip_file_path, 'r') as f:
        file_path = f.read()
    # Check if the zip file exists
    if os.path.exists(file_path):
        # Provide the zip file for download
        return send_file(file_path, as_attachment=True)
    else:
        print(f"Zip file not found {file_path}")
        return "Zip file not found"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
