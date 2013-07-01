$(document).ready(function(){
    //Only use the standard date field on touchscreen devices
    if (screen.width > 768 && screen.height > 768) {
        var datepickers = $('input[type="date"]');
        try{
            datepickers.prop('type','text');
        }
        catch(e){
            //Expected to fail with no consequences in IE
            console.log('Could not change input type from date to text')
        }
        datepickers.datepicker({dateFormat: "yy-mm-dd", changeYear: true, yearRange: "-2:+5"});
    }

    //Numeric field
    $('#id_amount').numeric();

    //Parallax on home page
    var scrollPos;
    var header = $('.jumbotron');
    var header_static = $('.jumbotron h1');
    $(window).scroll(function () {
        //Position in the page
        scrollPos = jQuery(this).scrollTop();

        //Scroll the banner text
        header.css({
            'background-position': "left " + (scrollPos * -0.5 - 100) + "px"
        });
        header_static.css({
            'top': (scrollPos * -0.5 + 520) + "px"
        });
    });
});