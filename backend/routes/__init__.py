from flask import Blueprint

# Creamos blueprints
main_bp = Blueprint("main", __name__)
location_bp = Blueprint("location", __name__)
auth_bp = Blueprint("auth", __name__)

# Importamos rutas (esto se hace abajo para evitar imports circulares)
from . import main, location_routes, auth
