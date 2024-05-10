from flask import Flask, request, send_file
import csv

app = Flask(__name__)

# Route to handle downloading the CSV file
@app.route('/download', methods=['GET'])
def download():
    # Path to the CSV file on the server
    csv_file_path = 'publicKeys.csv'
    return send_file(csv_file_path, as_attachment=True)

# Route to handle uploading and updating the CSV file
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        # Path to the CSV file on the server
        csv_file_path = 'publicKeys.csv'

        # Read the CSV file
        try:
            with open(csv_file_path, 'a') as f:
                # Append new entries to the CSV file
                f.write(file.stream.read().decode("utf-8"))
            return 'File uploaded and appended successfully'
        except Exception as e:
            return f'Error: {e}'

if __name__ == '__main__':
    app.run(debug=True)
