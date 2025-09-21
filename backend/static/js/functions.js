// =======================
// Configuración del mapa
// =======================
const MapModule = (() => {
  let map;
  let markers = {}; // Guardar marcadores por ID

  function initMap(center = [-34.92145, -57.95453], zoom = 14) {
    map = L.map('map').setView(center, zoom);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);
    return map;
  }

  function addMarker(id, name, lat, lng, imageUrl = null) {
    if (!map) return;
    let popupContent = `<b>${name}</b>`;
    if (imageUrl) {
        popupContent += `<br><img src="${imageUrl}" alt="${name}" style="width:150px;height:auto;margin-top:5px;border-radius:6px;">`;
    }
    markers[id] = L.marker([lat, lng]).addTo(map).bindPopup(popupContent);
  }


  function setView(lat, lng, zoom = 16) {
    if (!map) return;
    map.setView([lat, lng], zoom);
  }

  return { initMap, addMarker, setView };
})();

// =======================
// Carga de ubicaciones
// =======================
const LocationsModule = (() => {
  async function loadLocations(userId = 1) {
    try {
      const res = await fetch(`/users/${userId}/locations`);
      const data = await res.json();
      data.forEach(loc => MapModule.addMarker(loc.id, loc.name, loc.lat, loc.lng, loc.image_url));
    } catch (err) {
      console.error("Error cargando ubicaciones:", err);
    }
  }

  async function updateLocation(locId, fields) {
    try {
      const res = await fetch(`/locations/${locId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(fields)
      });
      return await res.json();
    } catch (err) {
      console.error("Error actualizando ubicación:", err);
    }
  }

  return { loadLocations, updateLocation };
})();

// =======================
// Manejo de formulario
// =======================
const FormModule = (() => {

  async function geocodeIntersection(intersection) {
    const query = `${intersection}, La Plata, Buenos Aires, Argentina`;
    const url = `https://nominatim.openstreetmap.org/search?format=json&countrycodes=AR&q=${encodeURIComponent(query)}&bounded=1&viewbox=-58.0007,-34.8971,-57.9178,-34.9535`;
    const res = await fetch(url);
    const data = await res.json();
    if (data.length > 0) {
      return { lat: parseFloat(data[0].lat), lng: parseFloat(data[0].lon) };
    } else {
      throw new Error("No se encontró la intersección 😕");
    }
  }

  async function saveLocation(userId, name, intersection, lat, lng, imageFile) {
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("name", name);
    formData.append("intersection", intersection);
    formData.append("lat", lat);
    formData.append("lng", lng);
    if (imageFile) formData.append("image", imageFile);

    const res = await fetch("/locations", {
        method: "POST",
        body: formData
    });

    return await res.json();
  }


  function setupForm(userId = 1) {
    const form = document.getElementById("locationForm");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const intersection = document.getElementById("intersection").value;

      try {
        const imageFile = document.getElementById("foto").files[0];
        const coords = await geocodeIntersection(intersection);
        const result = await saveLocation(userId, name, intersection, coords.lat, coords.lng, imageFile);
        console.log("Guardado en DB:", result);
        
        MapModule.addMarker(result.id, name, coords.lat, coords.lng, result.image_url);
        MapModule.setView(coords.lat, coords.lng);

        form.reset();
      } catch (err) {
        alert(err.message);
      }
    });
  }

  return { setupForm };
})();

// =======================
// Inicialización al cargar
// =======================
window.onload = () => {
  MapModule.initMap();
  LocationsModule.loadLocations(1); // de momento cargamos user 1
  FormModule.setupForm(1);
};
