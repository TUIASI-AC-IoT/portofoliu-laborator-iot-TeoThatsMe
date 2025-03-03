import io
from flask import Flask, send_file
import os.path
import sys

app = Flask(__name__)

@app.route('/firmware.bin')
def firm():
    with open(".pio\\build\\esp-wrover-kit\\firmware.bin", 'rb') as bites:
        print(bites)
        return send_file(
                     io.BytesIO(bites.read()),
                     mimetype='application/octet-stream'
               )

@app.route('/version')
def version():
    with open("versioning","rb") as version:
        line = version.readline()
        return line

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(host='192.168.89.37',ssl_context=('ca_cert.pem', 'ca_key.pem'),  debug=True)

#     app.run(host='192.168.89.37', ssl_context=('ca_cert.pem', 'ca_key.pem'), debug=True)