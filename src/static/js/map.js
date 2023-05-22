function initAutocomplete() {
  var directionsRenderer = new google.maps.DirectionsRenderer();
  directionsService = new google.maps.DirectionsService;
  directionsDisplay = new google.maps.DirectionsRenderer({
    polylineOptions: {
      strokeColor: "red"
    }
  });
  markers = new Map();
  var bounds = new google.maps.LatLngBounds();

  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: 42.3732, lng: -72.5199 },
    zoom: 13,
    mapTypeId: "roadmap",
  });

  directionsDisplay.setMap(map);
  directionsDisplay.setPanel(document.getElementById('directionsPanel'));

  // Create the search box and link it to the UI element.
  var start = document.getElementById("start");
  var end = document.getElementById("end");
  //var submit = document.getElementById("submit").addEventListener("change", onChangeHandler);
  addMarkerOnMap(start, map, markers, bounds, 'start');
  addMarkerOnMap(end, map, markers, bounds, 'end');
}

function addMarkerOnMap(input, map, markers, bounds, key) {

var autocomplete = new google.maps.places.Autocomplete(input);
autocomplete.bindTo('bounds', map);

google.maps.event.addListener(autocomplete, 'place_changed', function () {
  var place = autocomplete.getPlace();

  const icon = {
    url: place.icon,
    size: new google.maps.Size(71, 71),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(17, 34),
    scaledSize: new google.maps.Size(25, 25),
  };

  var marker = new google.maps.Marker({
      map,
      icon,
      title: place.name,
      position: place.geometry.location,
    });

  var infowindow = new google.maps.InfoWindow();
  google.maps.event.addListener(marker, 'click', (function(marker) {
    return function() {
      infowindow.setContent(place.name);
      infowindow.open(map, marker);
    }
  })(marker));

  // Create a marker for each place.

  if(markers.has(key)) {
      markers.get(key).setMap(null);
      markers.delete(key);
  }
  markers.set(key, marker);
  bounds.extend(marker.position);
  map.fitBounds(bounds);
  var zoom = map.getZoom();
  map.setZoom(zoom > 13 ? 13 : zoom);
  });
}

function showPathOnMap(start, end, path, distance, elevation){
  waypts = []
  for (let i = 3; i < path.length-3; i++){
    waypts.push({
      location: new google.maps.LatLng(path[i][0], path[i][1]),
      stopover: false,
    });
  }

  directionsService.route({
    origin: new google.maps.LatLng(start[0], start[1]),
    destination: new google.maps.LatLng(end[0], end[1]),
    waypoints: waypts,
    // optimizeWaypoints: true,
    travelMode: 'WALKING'
  }, function(response, status) {
    if (status === 'OK') {
      directionsDisplay.setDirections(response);
      setRouteStatistics(distance, elevation);
    } else {
      window.alert('Directions request failed due to ' + status);
    }
  });

}

function removeMarker() {
  if(markers.has('start')) {
    markers.get('start').setMap(null);
  }
  if(markers.has('end')) {
    markers.get('end').setMap(null);
  }
  markers.clear();
  map.setCenter({lat:42.3732, lng:-72.5199});
  map.setZoom(13);
}

function removePathFromMap(){
  //directionsDisplay.setDirections({routes: []});
  directionsDisplay.setMap(null);
  directionsDisplay.setPanel(null);
  directionsService = new google.maps.DirectionsService;
  directionsDisplay = new google.maps.DirectionsRenderer({
    polylineOptions: {
      strokeColor: "red"
    }
  });
  directionsDisplay.setMap(map);
}

function formValidation(){
  var start = document.getElementById("start").value;
  var end = document.getElementById("end").value;

  if(start==""){
    window.alert("Start Location is required.");
    return false;
  }

  if(end==""){
    window.alert("End Location is required.");
    return false;
  }
  return true;
}

function setRouteStatistics(distance, elevation) {
  distance = distance/1609.344;
  distance = Math.round(distance * 100) / 100;
  elevation = Math.round(elevation * 100) / 100;
  var routeStats = `<b>Total Distance:</b> ${distance} miles`;
  routeStats += '<br>';
  routeStats += `<b>Elevation Gain:</b> ${elevation} metres`;
  document.getElementById("statistics").innerHTML = routeStats;
  directionsDisplay.setPanel(document.getElementById('directionsPanel'));
  $("#info").show();
}

function resetRouteStatistics() {
  document.getElementById("statistics").innerHTML = "";
}
