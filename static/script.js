function deleteZgloszenie(url) {
    console.log(`Deleting task with URL: ${url}`);
    if (confirm('Czy na pewno chcesz usunąć to zgłoszenie?')) {
        console.log('Sending DELETE request...');
        fetch(url, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            console.log('Response received:', data);
            // Redirect to the zgloszenia page
            window.location.href = '{{ url_for("zgloszenia") }}';
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}