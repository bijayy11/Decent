from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os
import RSA
import AES

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


@app.route('/generate_keypair', methods=['GET']) # generates keypair (public and private key) 
def generate_keypair():
    keypairs = RSA.generate_keypair()
    return jsonify(keypairs)

@app.route('/generate_AESkey', methods=['GET']) #generates AES key
def generate_AESkey():
   encrypted_AES_key= AES.generate_random_key()
   return encrypted_AES_key

"""route to encrypt the message before sending"""
@app.route('/encrypt', methods=['GET']) 
def encrypt_message():
    message = request.form['message']
    private_key= request.form['private key']
    AES_key=request.form['AES_key']
    AES_key = RSA.decrypt(private_key,AES_key) # decrypts the encrypted AES key
    encrypted_message = AES.encrypt(AES_key,message) # decrypted AES key in previous line is used to encrypt the actual message
    return jsonify({'encrypted_message': encrypted_message})

"""route to decrypt the message after being received"""
@app.route('/decrypt', methods=['GET'])
def decrypt_message():
    encrypted_message = request.form['encrypted_message']
    message = request.form['message']
    private_key= request.form['private key']
    AES_key=request.form['AES_key']
    AES_key = RSA.decrypt(private_key,AES_key) # decrypts the encrypted AES key
    decrypted_message = AES.encrypt(AES_key,message) #decrypts the actual message using decrypted AES key
    return jsonify({'decrypted_message': decrypted_message})

"""route to retrieve privatekey"""
@app.route('/privatekey', methods=['GET'])
def getprivatekey():

    filename = ".private_key.pem"

    with open(filename, 'rb') as f:
        private_key_data = f.read()
        return private_key_data


"""route to extract the AES key"""
@app.route('/getAESkey', methods=['GET'])
def getAESkey():
    filename = ".AES_key.pem"
    with open(filename, 'rb') as f:
        AES_key_data = f.read()
        return AES_key_data

"""Route to username, keys and imagepath"""
@app.route('/store', methods=['POST'])
def store_data():
    if 'image_path' not in request.files:
        return jsonify({'error': 'No file part'})

    image_path = request.files['image_path']
    username = request.form['username']
    public_key = request.form['public_key']
    AES_key = request.form['AES_key']
    private_key = request.form['private_key']

    """writing private key in a hidden file with .pem extension"""
    filename = ".private_key.pem"  # Prefix filename with a dot
    with open(filename, 'wb') as f:
        f.write(private_key)

    """writing private key in a hidden file with .pem extension"""
    filename = ".AES_key.pem"  # Prefix filename with a dot
    with open(filename, 'wb') as f:
        f.write(AES_key)

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


"""route to retrieve the database"""
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