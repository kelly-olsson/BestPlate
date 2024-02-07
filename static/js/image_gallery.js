function getCSRFToken() {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        let [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return decodeURIComponent(value);
        }
    }
    return '';
}

var isLast = function(word) {
    return $(word).next().length > 0 ? false : true;
}

var getNext = function(word) {
    return $(word).next();
}

var getVisible = function () {
    return document.getElementsByClassName('is-visible');
}

var getFirst =  function() {
    var node = $('.words-wrapper').children().first();
    return node;
}

function switchWords(current, next) {
    $(current).removeClass('is-visible').addClass('is-hidden');
    $(next).removeClass('is-hidden').addClass('is-visible');
}

function getStarted() {
    var current = $('.words-wrapper b.is-visible');
    var next = current.next().length ? current.next() : $('.words-wrapper b').first();
    switchWords(current, next);
}

function init() {
    getStarted();
    setInterval(getStarted, 5000);
}

$(document).ready(function() {
    init();
});

function handleImageClick(url) {
    // Show loading overlay
    document.getElementById('loading-overlay').style.display = 'flex';

    // Simulate an API call with a delay
    setTimeout(() => {
        console.log('Simulated processing complete for image URL:', url);

        // Hide loading overlay after simulated processing is complete
        document.getElementById('loading-overlay').style.display = 'none';
    }, 10000); // 3000 milliseconds = 3 seconds
}