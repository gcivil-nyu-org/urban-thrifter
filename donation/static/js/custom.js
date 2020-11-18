jQuery(function ($) {
    var path = window.location.href; // because the 'href' property of the DOM element is the absolute path
    $('.side-bar ul a').each(function () {
        var link_path = this.href;
        // console.log("link: "+link_path)
        if (link_path === path) {
            $(this).addClass('active');
        }
    });
});