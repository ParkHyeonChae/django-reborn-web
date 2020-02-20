$(document).ready(function(){
    if (screen.width <= 991.98) {
        btnHide();
        
        $('#navbar').css({
            left: "48px",
        });
    }
    else {
        if ($.cookie('sidebar_cookie') == 'true') {
            document.getElementById('sidebar').setAttribute('class', 'active')
            btnHide();
        
            $('#navbar').css({
                left: "48px",
            });
            $('#sidebar').css({
                transition:'0s',
            });
        }
        else {
            document.getElementById('sidebar').removeAttribute('class', 'active')
            btnShow();

            $('#navbar').css({
                left: "348px",
            });
            $('#sidebar').css({
                transition:'0s',
            });
        }
    }
});


(function ($) {
    "use strict";
    var fullHeight = function () {
        $('.js-fullheight').css('height', $(window).height());
        $(window).resize(function () {
            $('.js-fullheight').css('height', $(window).height());
        });
    };
    fullHeight();
    // $('#sidebarCollapseHide').on('click', function () {
    //     $('#sidebar').toggleClass('active');
    // });

})(jQuery);

function hide() {
    $('#sidebar').toggleClass('active');
    btnHide();

    $('#navbar').css({
        left: "48px",
        transition: "0.3s"
    });
    $('#sidebar').css({
        transition:'0.3s',
    });
    setSidebarCookie();
};

function show() {
    $('#sidebar').toggleClass('active');
    btnShow();

    $('#navbar').css({
        left: "348px",
        transition: "0.3s"
    });
    $('#sidebar').css({
        transition:'0.3s',
    });
    removeSidebarCookie();
};

function btnShow() {
    document.getElementById('sidebarCollapseShow').setAttribute('hidden', '')
    document.getElementById('sidebarCollapseHide').removeAttribute('hidden')
}

function btnHide() {
    document.getElementById('sidebarCollapseShow').removeAttribute('hidden')
    document.getElementById('sidebarCollapseHide').setAttribute('hidden', '')
}

function setSidebarCookie() {
    $.cookie('sidebar_cookie', 'true', { path: '/' });    
}

function removeSidebarCookie() {
    $.removeCookie('sidebar_cookie', { path: '/' });
}