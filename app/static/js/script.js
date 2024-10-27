function call_add(album_id) {
    console.log("Function called with album ID:", album_id);
    fetch(`/add/${album_id}`, {
        method: 'POST'
    })
    .then(response => {
        if (response.ok) {
            alert('Album added to collection.');
        } else {
            console.error('Failed to add album to collection');
        }
    })
    .catch(error => console.error('Error:', error));
}