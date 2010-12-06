var geocoder;
var map;

function initialize() {
  geocoder = new google.maps.Geocoder();
  var latlng = new google.maps.LatLng(-34.397, 150.644);
  var myOptions = {
    zoom: 8,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  }
  map = new google.maps.Map(document.getElementById("hack-deploymentmap"), myOptions);
  onLocationInput();
}

function codeAddress(loc, description) {
  geocoder.geocode( { 'address': loc }, function(results, status) {
    if (status == google.maps.GeocoderStatus.OK) {
      map.setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: map, 
          position: results[0].geometry.location,
          title: description
      });
      var rect = new google.maps.Rectangle({ 'bounds': results[0].geometry.bounds });
      rect.setMap(map);
    } else {
      alert("Geocode was not successful for the following reason: " + status);
    }
  });
}

function onLocationInput() {
    var title = $("#id_title").val();
    var loc = $("#id_location").val();
    
    if (loc != null && loc != "")
        codeAddress(loc, title);
}

if (typeof window.onload != 'function') {
  window.onload=initialize;
} else {
  var old_onload = window.onload;
  window.onload = function () {
    if (old_onload) {
      window.onload();
    }
    initialize();
  }
}

$("#id_location").change(onLocationInput);
