"""byte_data = b'\x9b\xban\xa5h;\xf4\x8c\xd3Ui\xcb\x91\x87P\x15\xc2\xaf\x0b\xe2\tv\xfe\xc5r\xf03U9\x9d\x02\x04'

char_array = [chr(byte) for byte in byte_data]

print(char_array)


byte_data = bytes(ord(char) for char in char_array)

print(byte_data)"""

from flask import Flask 

app = Flask(__name__) 

# Pass the required route to the decorator. 
@app.route("/hello") 
def hello(): 
	return "testfile"
	
@app.route("/") 
def index(): 
	return "hello"

if __name__ == "__main__": 
	app.run(debug=True) 
