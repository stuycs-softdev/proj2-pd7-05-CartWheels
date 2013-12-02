$(function () {
    "use strict";

    //Google maps initialization
    var mapOptions = {
        center: new google.maps.LatLng(40.786383, -73.822921),
        zoom: 11,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    var map = new google.maps.Map($("#map-canvas").get(0),
        mapOptions),
        markers = [];

    //Searching functions
    var submit_form = function (e, key, val) {
        var obj = {};
        obj[key] = val;

        $.getJSON($SCRIPT_ROOT + '/_data', obj, function (data) {
            //Recenter the map
            var latitude = parseFloat(data.results[0].lat, 10),
                longitude = parseFloat(data.results[0].lng, 10),
                center = new google.maps.LatLng(latitude, longitude);

            map.setCenter(center);
            map.panTo(center);

            //Clear current markers
            $.each(markers, function (index, marker) {
                marker.setMap(null);
            });
            markers = [];

            //Create new markers
            $.each(data.results, function (index, value) {
                if ('lat' in value && 'lng' in value) {
                    //Make the marker
                    var lat = parseFloat(value.lat, 10),
                        lng = parseFloat(value.lng, 10),
                        latLng = new google.maps.LatLng(lat, lng);

                    var marker = new google.maps.Marker({
                        position: latLng,
                        animation: google.maps.Animation.DROP,
                        title: value.owner
                    });

                    //Info window
                    var contentString = '<div id="content">' +
                        '<div id="siteNotice">' +
                        '</div>' +
                        '<a href=/carts/' + value._id + ' >' + value.owner + '</p>' +
                        '</div>';

                    var infowindow = new google.maps.InfoWindow({
                        content: contentString
                    });

                    //Bind events to marker
                    var overMarker = function () {
                        infowindow.open(map, marker);
                    };
                    google.maps.event.addListener(marker, 'click', overMarker);

                    //Render the marker
                    markers.push(marker);
                    marker.setMap(map);
                }
            });
        });
        return false;
    };

    $('.map-form').submit(function (e) {
        event.preventDefault();
        var key = $("#key").val(),
            val = $("#val").val();
        submit_form(e, key, val.toUpperCase());
    });
});
