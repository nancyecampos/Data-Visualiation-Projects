// Store our API endpoint inside queryUrl
var queryUrl = "https://raw.githubusercontent.com/nancyecampos/sandbox/master/2017.geojson";

// Perform a GET request to the query URL
d3.json(queryUrl, function (data) {
  createMap(data.features);
});
function createMap(corals) {
  // Define streetmap and darkmap layers
  var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    id: "mapbox.streets",
    accessToken: API_KEY
  });
  // Define a baseMaps object to hold our base layers
  var baseMaps = {
    "Street Map": streetmap
  };
  // Create our map, giving it the streetmap and earthquakes layers to display on load
  var myMap = L.map("map", {
    center: [
      37.09, -95.71
    ],
    zoom: 3,
    layers: [streetmap]
  });
  // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
  L.control.layers(baseMaps, null, {
    collapsed: false
  }).addTo(myMap);
  // use a "canvas" to render the layer
  // instead of a 'heavy' DOM element for the pushpins
  // the circles are rendered on their own layer at top GPU speeds
  var myRenderer = L.canvas({ padding: 0.5 }); // create the canvas 'renderer'
  console.log('starting to create corals')
  for (coral of corals) {
    let latlon = swap(coral.geometry.coordinates); // for some reason we had to swap the coords
    L.circleMarker(latlon, { // create the circle
      renderer: myRenderer, // tell it which renderer to use to draw the circle
      color: 'orange', 
      radius: 1.0
    }).addTo(myMap).bindPopup(`coral: ${coral.properties.commonname}, source: ${coral.properties.source}, number of records: ${coral.properties.ccount}`); // add the layer to your map
  }
  console.log('done creating corals')
}
function swap(a){
  return [a[1], a[0]]
}
