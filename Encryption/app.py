from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app = Flask(__name__)

# Function to establish connection to SQLite database
def get_db_connection():
    conn = sqlite3.connect('keyinfo.db')
    conn.row_factory = sqlite3.Row #allows selecting a row of tuples with column name
    return conn

# Function to initialize database schema
def init_db():
    with app.app_context():
        db = get_db_connection()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

# Route to store image file path and username in database
@app.route('/store', methods=['POST'])
def store_data():
    if 'image_path' not in request.files:
        return jsonify({'error': 'No file part'})

    image_path = request.files['image_path']
    username = request.form['username']
    public_key = request.form['public_key']
    private_key = request.form['private_key']

    # Write private key to a hidden file
    filename = ".private_key.pem"  # Prefix filename with a dot
    with open(filename, 'wb') as f:
        f.write(private_key)
        # Save image file
        filename = secure_filename(image_path.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_path.save(filepath)

    if image_path.filename == '':
        return jsonify({'error': 'No selected file'})

    if image_path and allowed_file(image_path.filename):
        filename = secure_filename(image_path.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_path.save(filepath)

        db = get_db_connection()
        db.execute('INSERT INTO keys (username, public_key, imagepath) VALUES (?, ?, ?)',
                   (username, public_key, filepath))
        db.commit()
        db.close()

        return jsonify({'message': 'Data uploaded successfully'}), 201

    return jsonify({'error': 'Invalid file type'})


# Route to retrieve stored image file paths and usernames
@app.route('/retrieve', methods=['GET'])
def get_images():
    db = get_db_connection()
    keys = db.execute('SELECT * FROM keys').fetchall()
    db.close()
    return jsonify([dict(key) for key in keys])


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    init_db()
    app.run(debug=True)
