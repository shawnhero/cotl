$(function () {

    // Initiate the chart
    $('#container').highcharts('Map', {
        // chart: {
        //     events: {
        //         // below is the local test to add point to the map
        //         load: function () {

        //             // set up the updating of the chart each second
        //             var series = this.series[2];
        //             setInterval(function () {
        //                 var lat = 37+Math.random();
        //                     lon = -122+Math.random();
        //                 series.addPoint({
        //                     named: "random",
        //                     lat: lat,
        //                     lon: lon
        //                 });
        //             }, 1000);
        //         }
        //     }
        // },
        title: {
            text: 'Cotl Demo'
        },
        subtitle : {
            text : 'Live Photo Stream'
        },

        legend: {
            enabled: false
        },

        mapNavigation: {
            enabled: true,
            enableDoubleClickZoomTo: true,
            buttonOptions: {
                verticalAlign: 'bottom'
            }
        },        
        tooltip: {
            // Use lat/lon instead of x/y in tooltip
            formatter: function () {
                return this.point.named + '<br>Lat: ' + this.point.lat + ' Lon: ' + this.point.lon;
            },
        },
        
        series: [{
            // Use the gb-all map with no data as a basemap
            mapData: Highcharts.maps['countries/us/custom/us-all-mainland'],
            name: 'Basemap',
            borderColor: '#707070',
            color: '#E0E0E0',
            //nullColor: Highcharts.getOptions().colors[0],
            showInLegend: false
        }, {
            name: 'Separators',
            type: 'mapline',
            data: Highcharts.geojson(Highcharts.maps['countries/us/custom/us-all-mainland'], 'mapline'),
            color: '#707070',
            showInLegend: false,
            enableMouseTracking: false
        }, {
            // Specify points using lat/lon
            type: 'mappoint',
            name: 'Cities',
            color: Highcharts.getOptions().colors[1],
            showInLegend: false, 
             marker: {
                        "fillColor": "green",
                        "lineColor": "green",
                        "lineWidth": 1,
                        "radius": 1
                    },
            data: [{
                named: "Insight Data Science",
                lat: 37.426296, 
                lon: -122.140971,
            },
            {
                named: "UCLA",
                lat: 34.068948, 
                lon: -118.445192

            }

            ]
        }]
    });


 


    // listen to the incoming msgs, and add points
    if (!!window.EventSource) {
    var source = new EventSource('/subscribe');
    var date = new Date();
    source.onmessage = function(e) {
        console.log(e.data);
        alert(e.data);
    };
    // counter matches what you send in lib/realtime_analytics.rb
    // source.addEventListener('FOOBAR', function(e) {
    //   x = (new Date().getTime());
    //   y = parseFloat(e.data)
    //   chart.series[0].addPoint([x, y], true, true);
    //   $("#last_received").html(y);
    //   $("#last_received").effect( "highlight", {}, 500 );
    // }, false);

    source.addEventListener('message', function(e) {
      //console.log(e.data);
      alert(e.data);
    }, false);

    source.addEventListener('open', function(e) {
      console.log("SSE connection opened");
    }, false);

    source.addEventListener('error', function(e) {
      if (e.readyState == EventSource.CLOSED) {
        console.log("SSE connection closed");
      }
    }, false);
    } else {
    console.log("SSE not supported by your browser");
    }
});