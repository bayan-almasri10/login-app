from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app.extensions import db, bcrypt 

auth_bp = Blueprint("auth", __name__)

# ✅ Route لعرض صفحة تسجيل الدخول عند زيارة "/" أو "/login" مباشرة
@auth_bp.route("/", methods=["GET"])
@auth_bp.route("/login", methods=["GET"])
def show_login_page():
    return render_template("login.html")

# ✅ Route لتسجيل مستخدم جديد
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(username=data["username"])
    new_user.set_password(data["password"])  

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

# ✅ Route لتسجيل الدخول ويدعم `POST` باستخدام JSON أو بيانات نموذج (`form-data`)
@auth_bp.route("/login", methods=["POST"])
def login():
    if request.is_json:
        data = request.json  # استقبال البيانات بصيغة JSON
    else:
        data = request.form  # استقبال البيانات من النموذج (form-data)

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"message": "Login successful!", "access_token": access_token}), 200

# ✅ Route محمي يتطلب توثيق JWT
@auth_bp.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    user_id = get_jwt_identity()
    return jsonify({"message": f"Access granted for user {user_id}"}), 200
