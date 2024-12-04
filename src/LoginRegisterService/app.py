from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    return jsonify({"message": "User logged in successfully"}), 200

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    return jsonify({"message": "Password reset link sent"}), 200

@app.route('/remember-me', methods=['POST'])
def remember_me():
    data = request.get_json()
    return jsonify({"message": "Remember me enabled"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)