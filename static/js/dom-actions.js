$(function () {
    "use strict";

    $('#carts').click(function (e) {
        event.preventDefault();
        $('div#cart-results').removeClass('hidden');
        $('div#rev-results').addClass('hidden');
    });

    $('#revs').click(function (e) {
        event.preventDefault();
        $('div#cart-results').addClass('hidden');
        $('div#rev-results').removeClass('hidden');
    });
});
