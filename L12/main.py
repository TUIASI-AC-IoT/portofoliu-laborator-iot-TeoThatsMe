from flask import *
import os
import random

app = Flask(__name__)
CONFIG_DIR = 'sensor_configs'
os.makedirs(CONFIG_DIR, exist_ok=True)


# sim senzori
def simulate_sensor_value(sensor_id):
    return round(random.uniform(20.0, 30.0), 2)  # temperatura random


# get senzor
@app.route('/sensor/<sensor_id>', methods=['GET'])
def get_sensor_value(sensor_id):
    value = simulate_sensor_value(sensor_id)
    return jsonify({'sensor_id': sensor_id, 'value': value})


# creare fisier de conf
@app.route('/sensor/<sensor_id>', methods=['POST'])
def create_sensor_config(sensor_id):
    filename = os.path.join(CONFIG_DIR, f'{sensor_id}.cfg')
    if os.path.exists(filename):
        return jsonify({'error': 'Fisierul deja exista'}), 409
    config = request.get_json()
    with open(filename, 'w') as f:
        f.write(str(config))
    return jsonify({'message': f'Fisier de configurare pentru {sensor_id} creat'}), 201


# PUT: actualizare fisier de conf
@app.route('/sensor/<sensor_id>/<filename>', methods=['PUT'])
def update_sensor_config(sensor_id, filename):
    full_path = os.path.join(CONFIG_DIR, filename)
    if not os.path.exists(full_path):
        return jsonify({'error': 'Fisierul de configurare nu exista'}), 404
    new_config = request.get_json()
    with open(full_path, 'w') as f:
        f.write(str(new_config))
    return jsonify({'message': f'Update reusit'}), 200

if __name__ == '__main__':
    app.run(debug=True)

# curl -X POST http://localhost:5000/sensor/sensor1 \
# -H "Content-Type: application/json" \
# -d '{"scale": "Celsius"}'
