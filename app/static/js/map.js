((g) => {
  var h,
    a,
    k,
    p = "The Google Maps JavaScript API",
    c = "google",
    l = "importLibrary",
    q = "__ib__",
    m = document,
    b = window;
  b = b[c] || (b[c] = {});
  var d = b.maps || (b.maps = {}),
    r = new Set(),
    e = new URLSearchParams(),
    u = () =>
      h ||
      (h = new Promise(async (f, n) => {
        await (a = m.createElement("script"));
        e.set("libraries", [...r] + "");
        for (k in g)
          e.set(
            k.replace(/[A-Z]/g, (t) => "_" + t[0].toLowerCase()),
            g[k]
          );
        e.set("callback", c + ".maps." + q);
        a.src = `https://maps.${c}apis.com/maps/api/js?` + e;
        d[q] = f;
        a.onerror = () => (h = n(Error(p + " could not load.")));
        a.nonce = m.querySelector("script[nonce]")?.nonce || "";
        m.head.append(a);
      }));
  d[l]
    ? console.warn(p + " only loads once. Ignoring:", g)
    : (d[l] = (f, ...n) => r.add(f) && u().then(() => d[l](f, ...n)));
})({
  key: API_KEY,
  v: "weekly",
});

let map;
let markers = [];

/**
 * @typedef {Object} Place
 * @property {string} name
 * @property {string} latitude
 * @property {string} longitude
 */

function drawMarkerForPlace(place) {
  markers.push(
    new google.maps.Marker({
      title: place.name,
      position: {
        lat: Number.parseFloat(place.latitude),
        lng: Number.parseFloat(place.longitude),
      },
      map: map,
    })
  );
}

function renderPlaceInfo(place) {
  const placeInfo = document.createElement("div");
  placeInfo.classList.add("place-info-container");
  placeInfo.style.height = "20vh";
  placeInfo.innerHTML = `
      <div class="place-image-container">
        <img src="${place.image}" alt="${place.name}" />
      </div>
      <div class="place-info">
        <h3>${place.name}</h3>
        <p>${place.description}</p>
      </div>
  `;

  document.getElementById("sidebar").appendChild(placeInfo);
}

/**
 * @param {LatLngBounds} bounds
 */
async function showPlacesForCurrentCoords(bounds) {
  markers.forEach((marker) => marker.setMap(null));
  document.getElementById("sidebar").innerHTML = "";

  const northEast = bounds.getNorthEast();
  const southWest = bounds.getSouthWest();
  response = await fetch(
    "/api/places/" +
      northEast.lng() +
      "/" +
      northEast.lat() +
      "/" +
      southWest.lng() +
      "/" +
      southWest.lat()
  );
  places_data = await response.json();
  places_data.data.forEach((place_data) => {
    drawMarkerForPlace(place_data);
    renderPlaceInfo(place_data);
  });
}

/**
 * @param {GeolocationCoordinates} coords
 */
async function renderMapWithInCoords(coords) {
  const { Map } = await google.maps.importLibrary("maps");
  let searchPlacesTimeout;

  document.getElementById("map").style.height = window.innerHeight + "px";
  document.getElementById("map").style.width = window.innerWidth * 0.75 + "px";

  map = new Map(document.getElementById("map"), {
    center: { lat: coords.latitude, lng: coords.longitude },
    zoom: 15,
    streetViewControl: false,
    fullscreenControl: false,
  });
  map.addListener("bounds_changed", async () => {
    clearTimeout(searchPlacesTimeout);
    searchPlacesTimeout = setTimeout(async () => {
      await showPlacesForCurrentCoords(map.getBounds());
    }, 5);
  });

  try {
    await showPlacesForCurrentCoords(map.getBounds());
  } catch (error) {
    console.error(error);
  }
}

function renderMap() {
  if (navigator.geolocation) {
    return navigator.geolocation.getCurrentPosition((position) => {
      renderMapWithInCoords(position.coords);
    });
  }

  renderMapWithInCoords({
    latitude: -34.397,
    longitude: 150.644,
  });
}

try {
  renderMap();
} catch (error) {
  console.error(error);
}
