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

  // Incase the fields are already filled
  onLocationInput();
}

function onLocationInput() {
  var title = $("#id_title").val();
  var loc = $("#id_location").val();

  if (!loc || loc == "")
    return;

  geocoder.geocode( { 'address': loc }, function(results, status) {
    if (status != google.maps.GeocoderStatus.OK)
      return;

    // Center map and drop marker
    map.setCenter(results[0].geometry.location);
    var marker = new google.maps.Marker({
      map: map,
      position: results[0].geometry.location,
    });

    // Add rectangle on the region
    var bounds = results[0].geometry.bounds;
    var rect = new google.maps.Rectangle({ 'bounds': bounds });
    rect.setMap(map);

    // Save the geocode data
    $("#id_lat").val(results[0].geometry.location.lat());
    $("#id_lng").val(results[0].geometry.location.lng());
    $("#id_bbox").val(
      bounds.getSouthWest().lat() + ","
      + bounds.getSouthWest().lng() + ","
      + bounds.getNorthEast().lat() + ","
      + bounds.getNorthEast().lng());
  });
}
$("#id_location").change(onLocationInput);

$("#id_lat").hide();
$("#id_lng").hide();
$("#id_bbox").hide();
