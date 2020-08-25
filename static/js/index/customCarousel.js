 AOS.init({
 	duration: 800,
 	easing: 'slide',
 	once: true
 });

jQuery(document).ready(function($) {

	"use strict";

	// loader
	$(".loader").delay(1000).fadeOut("slow");
  $("#overlayer").delay(1000).fadeOut("slow");	

	var siteCarousel = function () {
		if ( $('.nonloop-block-13').length > 0 ) {
			$('.nonloop-block-13').owlCarousel({
		    center: false,
		    items: 1,
		    loop: true,
				stagePadding: 0,
		    margin: 20,
		    autoplay: true,
		    autoHeight: true,
		    nav: true,
				navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
		    responsive:{
	        600:{
	        	margin: 0,
	        	stagePadding: 10,
	          items: 1
	        },
	        1000:{
	        	margin: 0,
	        	stagePadding: 0,
	          items: 1
	        },
	        1200:{
	        	margin: 0,
	        	stagePadding: 0,
	          items: 1
	        }
		    }
			});
		}

		$('.nonloop-block-13').owlCarousel({
	    center: false,
	    items: 1,
	    loop: true,
	    autoplay: true,
			stagePadding: 0,
	    margin: 20,
	    nav: true,
			navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">'],
	    responsive:{
        600:{
        	margin: 0,
        	stagePadding: 0,
          items: 2
        },
        1000:{
        	margin: 0,
        	stagePadding: 0,
          items: 2
        },
        1200:{
        	margin: 0,
        	stagePadding: 0,
          items: 3
        }
	    }
		});

		if ( $('.slide-one-item').length > 0 ) {
			$('.slide-one-item').owlCarousel({
		    center: false,
		    items: 1,
		    loop: true,
				stagePadding: 0,
		    margin: 0,
		    autoplay: true,
		    pauseOnHover: false,
		    nav: true,
		    navText: ['<span class="icon-arrow_back">', '<span class="icon-arrow_forward">']
		  });
	  }


	  var owl = $('.centernonloop').owlCarousel({
	    center: true,
	    items: 1,
	    loop: true,
	    margin:10,
	    dots: true,
	    smartSpeed: 1000,
	    responsive:{
	      600:{
	        items: 3
	      }
	    }
	  });

	  $('.customNextBtn').click(function(event) {
	  	event.preventDefault();
			owl.trigger('next.owl.carousel');
		});
		$('.customPrevBtn').click(function(event) {
			event.preventDefault();
			owl.trigger('prev.owl.carousel');
		});

	};
	siteCarousel();
});