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

$('#uid_newsfeed').bind('submit',function(e) {
    e.preventDefault(); //Will prevent the submit...
    var uid_value=$("#uid").val();
    if (! $.isNumeric(uid_value)){
        alert("Enter a valid UID!");
        return;
    }

      $.ajax({
        // Flickr API is SSL only:
        // https://code.flickr.net/2014/04/30/flickr-api-going-ssl-only-on-june-27th-2014/
        url: 'http://c0tl.com/api/uid/'+uid_value,
        // data: {
        //     format: 'json',
        //     method: 'flickr.interestingness.getList',
        //     api_key: '7617adae70159d09ba78cfec73c13be3' // jshint ignore:line
        // },
        // dataType: 'jsonp'//'jsonp',
        jsonp: 'jsoncallback'
    }).done(function (result) {
        // var returnedData = eval(result);
        var returnedData = JSON.parse(result);

        var linksContainer = $('#links'),
            baseUrl;

        // first remove all the images
        $('#links')
            .empty();
        // Add the demo images as links with thumbnails to the page:

        $.each(returnedData, function (index, photo) {
            
            baseUrl = photo.photo.URL;
            var sUrl =  baseUrl;
            var bUrl = baseUrl;
            if(baseUrl.charAt(baseUrl.length-5)=='b'){
                baseUrl = baseUrl.slice(0,baseUrl.length-5);
                sUrl =  baseUrl+'m.jpg';
                bUrl = baseUrl+'b.jpg';
            }
            
            $("<a class='photo'/>")
                .append($('<img>').prop('src', sUrl))
                .prop('href', bUrl)
                .prop('title', photo.photo.title[0])
                .attr('data-gallery', '')
                // .append("<span class='score' style='font-size:300'>88</span>")
                .appendTo(linksContainer);
        });
        // find all the image and then add sibling




        $("img").one("load", function(){
            var img = this;
            var it = $(this);
            setTimeout(function(){
                // do something based on img.width and/or img.height
                // alert(String(img.height));
                 // img.addClass( "bigImg" );
                var itstyle = "style='color:rgba(255, 255, 255, 0.8);position:absolute;left:"+String(img.width/2 - 55)+"px;top: -55px;font-family:Impact, Charcoal, sans-serif;;display: table-cell;font-size:100px;'"
                it.after( "<span class='score' "+itstyle+">88</span>" );
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
