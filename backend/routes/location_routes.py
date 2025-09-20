from . import location_bp
from flask import request, jsonify
from extensions import db
from models.ubicacion import Ubicacion
from models.user import User

# Crear ubicación asociada a un usuario
@location_bp.route("/locations", methods=["POST"])
def create_location():
    data = request.get_json()
    user_id = data.get("user_id")
    name = data.get("name")
    intersection = data.get("intersection")
    lat = data.get("lat")
    lng = data.get("lng")

    if not user_id or not name or lat is None or lng is None:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    ubicacion = Ubicacion(
        name=name,
        intersection=intersection,
        lat=lat,
        lng=lng,
        user=user
    )
    db.session.add(ubicacion)
    db.session.commit()

    return jsonify({
        "message": "Ubicación creada",
        "id": ubicacion.id
    }), 201


# Listar ubicaciones de un usuario
@location_bp.route("/users/<int:user_id>/locations", methods=["GET"])
def get_user_locations(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "intersection": u.intersection,
            "lat": u.lat,
            "lng": u.lng
        }
        for u in user.ubicaciones
    ])


# Actualizar ubicación
@location_bp.route("/locations/<int:loc_id>", methods=["PUT"])
def update_location(loc_id):
    ubicacion = Ubicacion.query.get(loc_id)
    if not ubicacion:
        return jsonify({"error": "Ubicación no encontrada"}), 404

    data = request.get_json()

    # Campos opcionales (solo actualiza los que vengan en el body)
    name = data.get("name")
    intersection = data.get("intersection")
    lat = data.get("lat")
    lng = data.get("lng")

    if name:
        ubicacion.name = name
    if intersection:
        ubicacion.intersection = intersection
    if lat is not None:
        ubicacion.lat = lat
    if lng is not None:
        ubicacion.lng = lng

    db.session.commit()

    return jsonify({
        "message": "Ubicación actualizada",
        "id": ubicacion.id,
        "name": ubicacion.name,
        "intersection": ubicacion.intersection,
        "lat": ubicacion.lat,
        "lng": ubicacion.lng
    })


# Eliminar ubicación
@location_bp.route("/locations/<int:loc_id>", methods=["DELETE"])
def delete_location(loc_id):
    ubicacion = Ubicacion.query.get(loc_id)
    if not ubicacion:
        return jsonify({"error": "Ubicación no encontrada"}), 404

    db.session.delete(ubicacion)
    db.session.commit()
    return jsonify({"message": "Ubicación eliminada"})
