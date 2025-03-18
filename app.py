from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if username == "testuser" and password == "testuser":
            return jsonify({"message": "Login successful!"}), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401

    return render_template("login.html")  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=31685, debug=True)
