/*------------------------------------------------------------------------------------
    
JS INDEX
=============

01 - Range Slider JS
02 - Main Slider JS
03 - Agent Slider JS
04 - Best Deal Slide JS
05 - Reviews Slider JS
06 - Property Slider JS
07 - Property-2 Slider JS
08 - Accordian Js
09 - Select Dropdown JS
10 - Responsive Menu JS
11 - Btn To Top JS
12 - Sticky Header JS



-------------------------------------------------------------------------------------*/


(function ($) {
	"use strict";

    jQuery(document).ready(function($){
        
        /* 
        =================================================================
        01 - Range Slider JS
        =================================================================	
        */
        
          $('.nstSlider').nstSlider({
              "left_grip_selector": ".leftGrip",
              "right_grip_selector": ".rightGrip",
              "value_bar_selector": ".bar",
              "value_changed_callback": function(cause, leftValue, rightValue) {
              $(this).parent().find('.leftLabel').text(leftValue);
              $(this).parent().find('.rightLabel').text(rightValue);
              }
          });
        
        
        /* 
        =================================================================
        02 - Main Slider JS
        =================================================================	
        */
        
        
        $(".afloon-slide").owlCarousel({
            animateOut: 'fadeOut',
            animateIn: 'fadeIn',
            items: 1,
            nav: true,
            dots: false,
            autoplay: true,
            loop: true,
            navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
            mouseDrag: true,
            touchDrag: true
        });
        
        $(".afloon-slide").on("translate.owl.carousel", function(){
            $(".afloon-main-slide h2, .afloon-main-slide p").removeClass("animated fadeInUp").css("opacity", "0");
            $(".afloon-main-slide .afloon-btn").removeClass("animated fadeInDown").css("opacity", "0");
        });
        $(".afloon-slide").on("translated.owl.carousel", function(){
            $(".afloon-main-slide h2, .afloon-main-slide p").addClass("animated fadeInUp").css("opacity", "1");
            $(".afloon-main-slide .afloon-btn").addClass("animated fadeInDown").css("opacity", "1");
        });
        
        $(".afloon-slide").on("translate.owl.carousel", function(){
            $(".afloon-main-slide h3").removeClass("animated slideInDown").css("opacity", "0");
        });
        $(".afloon-slide").on("translated.owl.carousel", function(){
            $(".afloon-main-slide h3").addClass("animated slideInDown").css("opacity", "1");
        });
        
        
         /* 
        =================================================================
        03 - Agent Slider JS
        =================================================================	
        */
        $(".afloon-agent-slide").owlCarousel({
            autoplay:true,
            loop:true,
            margin:20,
            touchDrag:false,
            mouseDrag:false,
            nav: false,
            dots: true,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            responsive:{
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
        
        
         /* 
        =================================================================
        04 - Best Deal Slide JS
        =================================================================	
        */
        $(".deal-property-slide").owlCarousel({
            autoplay:true,
            loop:true,
            margin:20,
            touchDrag:false,
            mouseDrag:false,
            nav: false,
            dots: true,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            responsive:{
                0: {
                    items: 1
                },
                480: {
                    items: 1
                },
                600: {
                    items: 2
                },
                1000: {
                    items: 3
                },
                1200: {
                    items: 3
                }
            }
        });
        
        
        /* 
        =================================================================
        05 - Reviews Slider JS
        =================================================================	
        */
        
        $(".client-slider").owlCarousel({
            items: 1,
            nav: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            loop: true,
            navText: ["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
            mouseDrag: false,
            touchDrag: false
        });
        
        
        /* 
        =================================================================
        06 - Property Slider JS
        =================================================================	
        */
        
        $('.property-slide').owlCarousel({
            items: 1,
            loop: false,
            center: false,
            callbacks: true,
            URLhashListener: true,
            autoplayHoverPause: true,
            startPosition: 'URLHash',
            dots:false
        });
        
        
        /* 
        =================================================================
        07 - Property-2 Slider JS
        =================================================================	
        */
        
        $(".property-2-slide").owlCarousel({
            items: 1,
            nav: true,
            dots: false,
            autoplay: true,
            autoplayTimeout: 6000,
            autoplaySpeed: 1200,
            autoplayHoverPause:true,
            loop: true,
            navText: ["<i class='fa fa-long-arrow-left'></i>", "<i class='fa fa-long-arrow-right'></i>"],
            mouseDrag: false,
            touchDrag: false
        });
        
        /* 
        =================================================================
        08 - Accordian Js
        =================================================================	
        */
        
        $('.accordion').on('shown.bs.collapse', function (e) {
            $(e.target).parent().addClass('active_acc');
            $(e.target).prev().find('.switch').removeClass('fa-plus');
            $(e.target).prev().find('.switch').addClass('fa-minus');
        });
        $('.accordion').on('hidden.bs.collapse', function (e) {
            $(e.target).parent().removeClass('active_acc');
            $(e.target).prev().find('.switch').addClass('fa-plus');
            $(e.target).prev().find('.switch').removeClass('fa-minus');
        });
        
        $('.accordion2').on('shown.bs.collapse', function (e) {
            $(e.target).parent().addClass('active_acc');
            $(e.target).prev().find('.switch').removeClass('fa-plus');
            $(e.target).prev().find('.switch').addClass('fa-minus');
        });
        $('.accordion2').on('hidden.bs.collapse', function (e) {
            $(e.target).parent().removeClass('active_acc');
            $(e.target).prev().find('.switch').addClass('fa-plus');
            $(e.target).prev().find('.switch').removeClass('fa-minus');
        });
        
        
        /* 
        =================================================================
        09 - Select Dropdown JS
        =================================================================	
        */

        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.pro-status').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.pro-status').val($(this).data('value'));
            });  
          };
        
        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.pro-type').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.pro-type').val($(this).data('value'));
            });  
          };
        
        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.pro-room').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.pro-room').val($(this).data('value'));
            });  
          };
        
        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.pro-age').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.pro-age').val($(this).data('value'));
            });  
          };
        
        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.pro-bed').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.pro-bed').val($(this).data('value'));
            });  
          };
        
        if ($(".dropdown-menu li").length) {
            $(".dropdown-menu li").on('click', function(){
              $(this).parents(".dropdown").find('.pro-bath').html($(this).text() + ' <i class="fa fa-angle-down"></i>');
              $(this).parents(".dropdown").find('.pro-bath').val($(this).data('value'));
            });  
          };

        
        /* 
        =================================================================
        10 - Responsive Menu JS
        =================================================================	
        */
        $("ul#afloon_navigation").slicknav({
            prependTo: ".afloon-responsive-menu"
        });
        
        
        /* 
        =================================================================
        11 - Btn To Top JS
        =================================================================	
        */
        if ($("body").length) {
            var btnUp = $('<div/>', {
                'class': 'btntoTop'
            });
            btnUp.appendTo('body');
            $(document).on('click', '.btntoTop', function() {
                $('html, body').animate({
                    scrollTop: 0
                }, 700);
            });
            $(window).on('scroll', function() {
                if ($(this).scrollTop() > 200) $('.btntoTop').addClass('active');
                else $('.btntoTop').removeClass('active');
            });
        }
        
        
        
        /* 
        =================================================================
        12 - Sticky Header JS
        =================================================================	
        */
        var $window = $(window);
        var  $mainHeaderBar = $('.white_header');
         var  $mainHeaderBarAnchor = $('#mainHeaderBarAnchor');
            if($('#mainHeaderBarAnchor').length){
            // Run this on scroll events.
            $window.scroll(function() {
            var window_top = $window.scrollTop();
            var div_top = $mainHeaderBarAnchor.offset().top;
	        if (window_top > div_top) {
                // Make the div sticky.
                $mainHeaderBar.addClass('static');
		        $mainHeaderBarAnchor.height($mainHeaderBar.height());
            }
                else {
                  // Unstick the div.
                  $mainHeaderBar.removeClass('static');
                  $mainHeaderBarAnchor.height(0);
               }
            });
            }
        

    });

}(jQuery));	
