$(function () {
    "use strict";

    //Google maps initialization
    var mapOptions = {
        center: new google.maps.LatLng(-34.397, 150.644),
zoom: 11,
mapTypeId: google.maps.MapTypeId.ROADMAP
    };


    var map = new google.maps.Map(document.getElementById("map-canvas"),
        mapOptions);

    var markers = [];

    //Searching functions
    var submit_form = function (e, key, val) {
        var obj = {};
        obj[key] = val;
        $.getJSON($SCRIPT_ROOT + '/_data', obj, function (data) {
            var latitude = parseFloat(data.results[0].lat, 10);
            var longitude = parseFloat(data.results[0].lng, 10);
            var center = new google.maps.LatLng(latitude, longitude);
            //Recenter the map
            map.setCenter(center);
            map.panTo(center);

            $.each(markers, function (index, marker) {
                marker.setMap(null);
            });
            markers = [];

            $.each(data.results, function (index, value) {
                if ('lat' in value && 'lng' in value) {
                    //Make the marker
                    var lat = parseFloat(value.lat, 10);
                    var lng = parseFloat(value.lng, 10);
                    var latLng = new google.maps.LatLng(lat, lng);
                    var marker = new google.maps.Marker({
                        position: latLng,
                        animation: google.maps.Animation.DROP,
                        title: value.owner
                    });

                    //Info window
                    var contentString = '<div id="content">' +
                        '<div id="siteNotice">' +
                        '</div>' +
                        '<p>' + value.owner + '</p>' +
                        '</div>';
                    var infowindow = new google.maps.InfoWindow({
                        content: contentString
                    });

                    var overMarker = function () {
                        infowindow.open(map, marker);
                    };
                    google.maps.event.addListener(marker, 'click', overMarker);
                    markers.push(marker);
                    marker.setMap(map);
                }
            });
        });
        return false;
    };

    $('input[type=text]').bind('keydown', function (e) {
        if (e.keyCode === 13) {
            var key = $("#key").val(),
                val = $("#val").val();

            submit_form(e, key, val.toUpperCase());
        }
    });
});
