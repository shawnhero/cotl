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
        // alert(result);
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
            
            $('<a/>')
                .append($('<img>').prop('src', sUrl))
                .prop('href', bUrl)
                .prop('title', photo.photo.title)
                .attr('data-gallery', '')
                .appendTo(linksContainer);
        });
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
