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