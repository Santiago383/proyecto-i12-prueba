from flask import Flask
from extensions import db, migrate
from routes import main_bp, location_bp, auth_bp
import os

def create_app():
    app = Flask(__name__)

    # Configuración básica
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://i12user:i12pass@postgres:5432/i12db"

    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev_secret_key")

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)

    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(auth_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
