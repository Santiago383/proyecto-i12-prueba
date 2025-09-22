from . import location_bp
from flask import request, jsonify
from extensions import db
import uuid
import os
from models.ubicacion import Ubicacion
from models.user import User

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@location_bp.route("/locations", methods=["POST"])
def create_location():
    name = request.form.get("name")
    intersection = request.form.get("intersection")
    lat = request.form.get("lat", type=float)
    lng = request.form.get("lng", type=float)
    user_id = request.form.get("user_id", type=int)
    image_file = request.files.get("image")  # archivo opcional

    if not name or lat is None or lng is None or not user_id:
        return jsonify({"error": "Faltan datos obligatorios"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    filename = None
    if image_file:
        filename = image_file.filename
        upload_path = os.path.join(UPLOAD_FOLDER, filename)
        image_file.save(upload_path)

    ubicacion = Ubicacion(
        name=name,
        intersection=intersection,
        lat=lat,
        lng=lng,
        user=user,
        image=filename
    )
    db.session.add(ubicacion)
    db.session.commit()

    return jsonify({
        "message": "Ubicación creada",
        "id": ubicacion.id,
        "image_url": f"/static/uploads/{filename}" if filename else None
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
            "lng": u.lng,
            "image_url": f"/static/uploads/{u.image}" if u.image else None
        }
        for u in user.ubicaciones
    ])


# Actualizar ubicación
@location_bp.route("/locations/<int:loc_id>", methods=["PUT"])
def update_location(loc_id):
    ubicacion = Ubicacion.query.get(loc_id)
    if not ubicacion:
        return jsonify({"error": "Ubicación no encontrada"}), 404

    # Si viene JSON puro
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        intersection = data.get("intersection")
        lat = data.get("lat")
        lng = data.get("lng")
        image_file = None
    else:
        # Si viene multipart/form-data (para permitir imagen)
        name = request.form.get("name")
        intersection = request.form.get("intersection")
        lat = request.form.get("lat", type=float)
        lng = request.form.get("lng", type=float)
        image_file = request.files.get("image")

    # Actualizaciones
    if name:
        ubicacion.name = name
    if intersection:
        ubicacion.intersection = intersection
    if lat is not None:
        ubicacion.lat = lat
    if lng is not None:
        ubicacion.lng = lng

    if image_file:
        filename = f"{uuid.uuid4().hex}_{image_file.filename}"
        upload_path = os.path.join("static/uploads", filename)
        os.makedirs("static/uploads", exist_ok=True)
        image_file.save(upload_path)
        ubicacion.image = filename

    db.session.commit()

    return jsonify({
        "message": "Ubicación actualizada",
        "id": ubicacion.id,
        "name": ubicacion.name,
        "intersection": ubicacion.intersection,
        "lat": ubicacion.lat,
        "lng": ubicacion.lng,
        "image_url": f"/static/uploads/{ubicacion.image}" if ubicacion.image else None
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


# Listar todas las ubicaciones
@location_bp.route("/locations", methods=["GET"])
def get_all_locations():
    ubicaciones = Ubicacion.query.all()
    return jsonify([
        {
            "id": u.id,
            "name": u.name,
            "intersection": u.intersection,
            "lat": u.lat,
            "lng": u.lng,
            "image_url": f"/static/uploads/{u.image}" if u.image else None,
            "user_id": u.user_id
        }
        for u in ubicaciones
    ])

