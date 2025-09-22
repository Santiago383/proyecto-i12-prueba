from . import auth_bp
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from models.user import User

# auth_bp = Blueprint("auth", __name__)

# -------- REGISTER --------
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Verificar que no exista
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Usuario o email ya existe", "danger")
            return redirect(url_for("auth.register"))

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.id
        flash("Usuario registrado con éxito", "success")
        return redirect(url_for("main.map_view"))

    return render_template("register.html")


# -------- LOGIN --------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login exitoso!", "success")
            return redirect(url_for("main.map_view"))
        elif user:
            flash("Contraseña incorrecta", "danger")
        else:
            flash("El usuario no existe", "warning")

    return render_template("login.html")


# -------- LOGOUT --------
@auth_bp.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Sesión cerrada", "info")
    return redirect(url_for("auth.login"))
