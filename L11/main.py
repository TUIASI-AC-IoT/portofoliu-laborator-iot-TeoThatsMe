from flask import Flask, request, jsonify
import os
import uuid

app = Flask(__name__)


FILES_DIR = 'files'


# listarea continutului directorului
@app.route('/files', methods=['GET'])
def list_files():
    return jsonify(os.listdir(FILES_DIR))

# listare continut fisier
@app.route('/files/<filename>', methods=['GET'])
def read_file(filename):
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'Fisierul nu exista'}), 404
    with open(path, 'r') as f:
        return jsonify({'content': f.read()})

# creare fisier specificat prin nume si continut
@app.route('/files', methods=['POST'])
def create_file_with_name():
    data = request.get_json()
    filename = data.get('filename')
    content = data.get('content', '')
    path = os.path.join(FILES_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    return jsonify({'message': f'{filename} creat'}), 201

# creare fisier specificat prin continut
@app.route('/files/auto', methods=['POST'])
def create_file_content():
    data = request.get_json()
    content = data.get('content', '')
    filename = f'{uuid.uuid4().hex}.txt'
    path = os.path.join(FILES_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    return jsonify({'message': 'Fisier creat'}), 201

# stergerea unui fisier specificat
@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'Fisier inexistent found'}), 404
    os.remove(path)
    return jsonify({'message': f'Fisier sters'}), 200

# modificare fisier
@app.route('/files/<filename>', methods=['PUT'])
def update_file(filename):
    data = request.get_json()
    content = data.get('content', '')
    path = os.path.join(FILES_DIR, filename)
    if not os.path.exists(path):
        return jsonify({'error': 'Fisierul nu exista'}), 404
    with open(path, 'w') as f:
        f.write(content)
    return jsonify({'message': f'Fisier updatat'}), 200

if __name__ == '__main__':
    app.run(debug=True)
