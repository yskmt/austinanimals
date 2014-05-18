var map;
var currentPosition;

// // get the current address
// if (navigator.geolocation) {
// navigator.geolocation.getCurrentPosition(function(position) {
// currentPosition = position;
// /* map.setCenter(new google.maps.LatLng(position.coords.latitude, */
// /* position.coords.longitude)) */
// }, function() {
// // alert('We cannot get your current location!!');
// });
// } else {
// // alert('Your browser is not compatible with geolocation!!');
// }

// geocoding
var geocoder = new google.maps.Geocoder();
geocoder.geocode({
	'address' : 'Austin, TX'
}, showMainMap);

function moveMap() {
	var geocoder = new google.maps.Geocoder();
	geocoder.geocode({
		'address' : document.getElementById('address').value
	}, function(result, status) {
		if (status == google.maps.GeocoderStatus.OK) {
			map.panTo(result[0].geometry.location);
		} else {
			alert("Address Geocoding ERROR!!");
		}
	});
}

function showMainMap(result, status) {
	if (status == google.maps.GeocoderStatus.OK) {
		var latlng;
		if (currentPosition !== undefined) {
			latlng = new google.maps.LatLng(currentPosition.coords.latitude, currentPosition.coords.longitude);
		} else {
			latlng = result[0].geometry.location;
		}

		var options = {
			zoom : 11,
			center : latlng,
			mapTypeId : google.maps.MapTypeId.ROADMAP,
			panControl : true,
			zoomControl : true,
			scaleControl : true
		};

		// define map
		map = new google.maps.Map(document.getElementById('map'), options);

		// add markers on click
		// addMinionMarker(map);
	} else {
		alert('Error Geocoding!');
	}

}

function addPetMarker(map, pet) {

	var trailerLatLng = new google.maps.LatLng(pet.lat, pet.lng);

	if (pet.pet_type === 'DOG'){
		icon_url = 'dog.png';
		// http://findicons.com/icon/38862/dog
	}
	else{
		icon_url = 'cat.png';
		// http://findicons.com/icon/38863/cat
	}

	var marker = new google.maps.Marker({
		position : trailerLatLng,
		map : map,
		icon : {
			url : icon_url,
			scaledSize : new google.maps.Size(40, 45)
		},
		title : pet.petID,
		draggable : false
	});
	// map.panTo(trailerLatLng);
	markersArray.push(marker);

	petInfoWindow(map, marker, pet, trailerLatLng);

}

function petInfoWindow(map, marker, pet, trailerLatLng) {

	infoContent = '<p>' + pet.petinfo.join(" ") + '</p>'
	+ '<a href="' + pet.link + '">' + 'details</a>' + pet.image_link;
	// '<img border="1" height="300" oncontextmenu="return false" src="http://www.petharbor.com/get_image.asp?RES=Detail&amp;ID=A679223&amp;LOCATION=ASTN"/>';

	var infoWindow = new google.maps.InfoWindow({
		content : infoContent,
		position : map.getCenter(),
		maxWidth: 320
	});
	google.maps.event.addListener(marker, 'click', function() {
		infoWindow.open(map, marker);
	});

	console.log(pet.petinfo.join(" "));

}
