function initMap() {
        // Default position of map
        var map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: 55.740750, lng: 37.608874},
          zoom: 17
        });
        var infoWindow = new google.maps.InfoWindow({map: map});


        $.getJSON("/static/json/map_style.json", function (data) {
            map.setOptions({styles: data});
        });


        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(
              function(position) {
                var pos = {
                  lat: position.coords.latitude,
                  lng: position.coords.longitude
                };

                infoWindow.setPosition(pos);
                infoWindow.setContent('Coffee needed here');
                map.setCenter(pos);       
                $.get("/points/?lat="+pos.lat + '&lng='+pos.lng, function(data) {                     
                     $('#cafes').html(data)                     
                });

                $.getJSON('/points-result-json/?lat='+pos.lat + '&lng='+pos.lng, function(data){
                  for (i = 0; i < data['cafes'].length; i++) {
                    var cafeMarker = new google.maps.Marker({
                      position: {lat: data['cafes'][i][1], lng: data['cafes'][i][2]},
                      map: map                      
                    });
                  };
                });            
              }, function() {
                  handleLocationError(true, infoWindow, map.getCenter());
              });
        } else {          
          handleLocationError(false, infoWindow, map.getCenter());
        }
      }



function handleLocationError(browserHasGeolocation, infoWindow, pos) {
        infoWindow.setPosition(pos);
        infoWindow.setContent(browserHasGeolocation ?
                              'Error: The Geolocation service failed.' :
                              'Error: Your browser doesn\'t support geolocation.');
      }
