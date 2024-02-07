function switchWords(current, next) {
    $(current).removeClass('is-visible').addClass('is-hidden');
    $(next).removeClass('is-hidden').addClass('is-visible');
}

function getStarted() {
    var current = $('.words-wrapper b.is-visible');
    var next = current.next().length ? current.next() : $('.words-wrapper b').first();
    switchWords(current, next);
}

function initOverlayAnimation() {
    getStarted();
    setInterval(getStarted, 5000);
}

$(document).ready(function() {
    initOverlayAnimation();
});