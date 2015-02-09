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
$(function () {
    'use strict';
      $.ajax({
        // Flickr API is SSL only:
        // https://code.flickr.net/2014/04/30/flickr-api-going-ssl-only-on-june-27th-2014/
        url: 'http://c0tl.com/api/top_tags',
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

        var linksContainer = $('#links');

        // first remove all the images
        $('#links')
            .empty();
        // Add the demo images as links with thumbnails to the page:
        var pos = 0;
        $.each(returnedData, function (index, tag) {
            if(tag.tag=="") return true;
            
            var buttonstyles = ["btn btn-default btn-lg", "btn btn-primary btn-lg", "btn btn-success btn-lg", "btn btn-info btn-lg", "btn btn-warning btn-lg", "btn btn-danger btn-lg"];
            // var ehover = "data-toggle='tooltip' data-placement='top' title='"+String(tag.count)+"'";
            // data-toggle='tooltip' data-placement='top'
              $("<button type='button' class='"+buttonstyles[pos++%6]+"' data-toggle='tooltip' data-placement='top' title='"+String(tag.count)+"'/>")
                .append(tag.tag)
                .appendTo(linksContainer);
        });
        $('[data-toggle="tooltip"]').tooltip()
        // add on click event to the buttons
        $( '[data-toggle="tooltip"]' ).click(function(event) {
            // add the title

            // clear all the tags
            $('#links').empty();
            var count = $(this).attr('data-original-title');
            var tagname = $(this).text();
            var titleContainer = $('#tagname');
            $("<button type='button' class='btn btn-success btn-lg'/><br><br>")
                .append(tagname)
                .appendTo(titleContainer);

            var formData = {name: tagname, num: count};
            // add all the photos under this tag
            $.ajax({
                url: 'http://c0tl.com/api/tag/',
                type: "POST",
                data : formData,
                jsonp: 'jsoncallback'
            }).done(function (result) {
                var returnedData = JSON.parse(result);
                var linksContainer = $('#links'),baseUrl;;

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
                        .append($("<img numlikes="+String(photo.numLiked)+" >").prop('src', sUrl))
                        .prop('href', bUrl)
                        .prop('title', photo.photo.title)
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
                        it.after( "<span class='score' "+itstyle+">"+it.attr('numlikes')+"</span>" );
                        // 
                        // 
                    }, 0);
                });

            });


        });
    });



  //Add additional code here
  // $('.tooltip').tooltip()
});

