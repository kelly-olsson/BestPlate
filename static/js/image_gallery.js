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
    showLoadingOverlay()

    fetch('/process-image/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCSRFToken(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imageUrl: url })
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect_url) {
            window.location.href = data.redirect_url;
        } else {
            console.log('Processed Image:', data);
        }
        // Hide loading overlay after processing is complete
        document.getElementById('loading-overlay').style.display = 'none';
    })
    .catch(error => {
        console.error('Error:', error);
        // Hide loading overlay even if there's an error
        document.getElementById('loading-overlay').style.display = 'none';
    });
}