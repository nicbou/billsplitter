$(document).ready(function(){
    //CORRECTIONS
    if (screen.width > 768 && screen.height > 768) {
        //Only use the standard date field on touchscreen devices
        var datepickers = $('input[type="date"]');
        try{
            datepickers.prop('type','text');
        }
        catch(e){
            //Expected to fail with no consequences in IE
            console.log('Could not change input type from date to text');
        }
        datepickers.datepicker({dateFormat: "yy-mm-dd", changeYear: true, yearRange: "-2:+5"});

    } else {
        //Elements that take 100% of the viewport on mobile devices
        //This simply compensates for the 20px padding on the body
        $('.full-width').css({
            'width':'+=40',
            'margin-left':'-20px',
        })
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