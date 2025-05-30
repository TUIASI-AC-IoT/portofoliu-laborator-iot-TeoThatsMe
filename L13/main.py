from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required,
    get_jwt_identity, get_jwt
)
from datetime import timedelta

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "cheie_jwt" 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

jwt = JWTManager(app)

users = {
    "user1": {"password": "parola1", "role": "admin"},
    "user2": {"password": "parola2", "role": "owner"},
    "user3": {"password": "parolaX", "role": "owner"},
}

active_tokens = set()

@app.route("/auth", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = users.get(username)
    if not user or user["password"] != password:
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"username": username, "role": user["role"]})
    jti = get_jwt()["jti"]
    active_tokens.add(jti)

    return jsonify(access_token=access_token), 200

@app.route("/auth/jwtStore", methods=["GET"])
@jwt_required()
def validate_token():
    jti = get_jwt()["jti"]
    if jti not in active_tokens:
        return jsonify({"msg": "Token not found"}), 404

    identity = get_jwt_identity()
    return jsonify({"role": identity["role"]}), 200

@app.route("/auth/jwtStore", methods=["DELETE"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    if jti not in active_tokens:
        return jsonify({"msg": "Token not found"}), 404

    active_tokens.remove(jti)
    return jsonify({"msg": "Token invalidated"}), 200

@app.route("/sensor/data", methods=["GET"])
@jwt_required()
def read_sensor():
    identity = get_jwt_identity()
    if identity["role"] in ["owner", "admin"]:
        return jsonify({"data": "valoare_senzor=123"}), 200
    return jsonify({"msg": "Access denied"}), 403

@app.route("/sensor/config", methods=["POST"])
@jwt_required()
def update_sensor():
    identity = get_jwt_identity()
    if identity["role"] == "admin":
        return jsonify({"msg": "Configurație actualizată"}), 200
    return jsonify({"msg": "Access denied"}), 403

if __name__ == "__main__":
    app.run(debug=True)
