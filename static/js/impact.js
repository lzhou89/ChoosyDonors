$(document).ready(function () {
	var results = $("#query").html();
	var output = JSON.parse(results);
	console.log(output);

	var $map=$("#map");
	var map = new google.maps.Map($map[0], {
			zoom: 10,
			mapTypeId: google.maps.MapTypeId.ROADMAP,
		});
	var geocoder = new google.maps.Geocoder();
	geocoder.geocode({'address': 'US'}, function (results, status) {
      var ne = results[0].geometry.viewport.getNorthEast();
      var sw = results[0].geometry.viewport.getSouthWest();

       map.fitBounds(results[0].geometry.viewport);
    });

    var rateById = d3.map();

	var quantize = d3.scale.quantize()
		.domain([0, 50])
		.range(d3.range(9).map(function(i) { return "q" + i + "-9"; }));

	queue()
		.defer(d3.json, "/static/zips_us_topo.json")
		.defer(d3.csv, "/static/impact.csv", function(d) {rateById.set(d.id, +d.rate);})
		.await(ready);

	function ready(error, us) {
		var overlay = new google.maps.OverlayView();

		overlay.onAdd = function () {

			var layer = d3.select(this.getPanes().overlayLayer).append("div").attr("class", "SvgOverlay");
			var svg = layer.append("svg")
				.attr("width", $map.width())
				.attr("height", $map.height());
			var zips = svg.append("g").attr("class", "zips");

			overlay.draw = function () {
				var markerOverlay = this;
				var overlayProjection = markerOverlay.getProjection();

				var googleMapProjection = function (coordinates) {
					var googleCoordinates = new google.maps.LatLng(coordinates[1], coordinates[0]);
					var pixelCoordinates = overlayProjection.fromLatLngToDivPixel(googleCoordinates);
					return [pixelCoordinates.x, pixelCoordinates.y];
				};

				path = d3.geo.path().projection(googleMapProjection);
				zips.selectAll("path")
					.data(topojson.feature(us, us.objects.zip_codes_for_the_usa).features)
					.attr("d", path)
				.enter().append("svg:path")
					.attr("class", function(d) { return quantize(rateById.get(d.properties.zip)); })
					.attr("data-zip", function(d) {return d.properties.zip; })
					.attr("data-state", function(d) {return d.properties.state; })
					.attr("data-name", function(d) {return d.properties.name; })
					.attr("d", path);

			};

		};

		var infowindow = new google.maps.InfoWindow();
		var markers = [];
		for (var i=0; i < output.length; i++) {
			var marker = new google.maps.Marker({
				position: new google.maps.LatLng(output[i]["latitude"], output[i]["longitude"]),
				map: map,
				title: output[i]["title"],
				id: output[i]["id"]
			});
			// marker.metadata = {id: output[i]["id"]};
			markers.push(marker);
			// marker.setMap(map);
			google.maps.event.addListener(marker, 'click', function() {
				console.log(this.id);
				infowindow.setContent("<a href='/project/"+this.id+"'><h3>"+this.title+"</h3></a>"+" Infotext");
				infowindow.open(map, this);
				});
		}
		var markerCluster = new MarkerClusterer(map, markers);

		overlay.setMap(map);

	}


});



