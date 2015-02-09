/*
 * Bootstrap Image Gallery JS Demo 3.0.1
 * https://github.com/blueimp/Bootstrap-Image-Gallery
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/*jslint unparam: true */
/*global blueimp, $ */
// $('[data-toggle="tooltip"]').tooltip({
//     'placement': 'top'
// });

$('#findnearby').bind('submit',function(e) {
    e.preventDefault(); //Will prevent the submit...
    var lat=$("#lat").val();
    var lon=$("#lon").val();
    var R=$("#r").val();
    if (! $.isNumeric(lat) || ! $.isNumeric(lon) || ! $.isNumeric(R)){
        alert("Enter valid numbers!");
        return;
    }
    var formData = {lat: lat, lon: lon, r: R};

    $.ajax({
        url: 'http://c0tl.com/api/nearby/',
        type: "POST",
        data : formData,
        jsonp: 'jsoncallback'
    }).done(function (result) {
        // var returnedData = eval(result);
        var returnedData = JSON.parse(result);

        var linksContainer = $('#links');

        // first remove all the images
        $('#links')
            .empty();
        // Add the demo images as links with thumbnails to the page:
        var pos = 0;
         $.each(returnedData, function (index, photo) {
            
            baseUrl = photo.photo.URL;
            var sUrl =  baseUrl;
            var bUrl = baseUrl;
            if(baseUrl.charAt(baseUrl.length-5)=='b'){
                baseUrl = baseUrl.slice(0,baseUrl.length-5);
                sUrl =  baseUrl+'m.jpg';
                bUrl = baseUrl+'b.jpg';
            }
            
            var tooltip_str = 'Distance: '+String(photo.distance)+'km\nNumLiked:'+String(photo.numLiked)+'\nNumPassed:'+String(photo.numViewed)+"\n";
            $("<a class='photo' />")
                .append($("<img numlikes="+String(photo.numLiked)+" data-toggle='tooltip' data-placement='top' title='"+tooltip_str+"'>").prop('src', sUrl))
                .prop('href', bUrl)
                .prop('title', photo.photo.title)
                .attr('data-gallery', '')
                // .append("<span class='score' style='font-size:300'>88</span>")
                .appendTo(linksContainer);
        });
        // find all the image and then add sibling
        $('[data-toggle="tooltip"]').tooltip()



        $("img").one("load", function(){
            var img = this;
            var it = $(this);
            setTimeout(function(){
                // do something based on img.width and/or img.height
                // alert(String(img.height));
                 // img.addClass( "bigImg" );
                var itstyle = "style='color:rgba(255, 255, 255, 0.8);position:absolute;left:"+String(img.width/2 - 55)+"px;top: -55px;font-family:Impact, Charcoal, sans-serif;;display: table-cell;font-size:100px;'"
                it.after( "<span class='score' "+itstyle+">"+it.attr('numlikes')+"</span>" );
                // 
                // 
            }, 0);
        });

        // $('.score').attr('style', 'color:white;font-size:100px;position: absolute;left: 5px;bottom: 0;font-family:Impact, Charcoal, sans-serif;opacity: 0.8;');

    });

    // $('#borderless-checkbox').on('change', function () {
    //     var borderless = $(this).is(':checked');
    //     $('#blueimp-gallery').data('useBootstrapModal', !borderless);
    //     $('#blueimp-gallery').toggleClass('blueimp-gallery-controls', borderless);
    // });

    // $('#fullscreen-checkbox').on('change', function () {
    //     $('#blueimp-gallery').data('fullScreen', $(this).is(':checked'));
    // });

    $('#image-gallery-button').on('click', function (event) {
        event.preventDefault();
        blueimp.Gallery($('#links a'), $('#blueimp-gallery').data());
    });




  //Add additional code here
});

$(function () {
    'use strict';

    // Load demo images from flickr:
  

 
});
