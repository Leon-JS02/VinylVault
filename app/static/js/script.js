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

function delete_album(album_id) {
    if (confirm("Are you sure you want to delete this album?")) {
        fetch(`/delete_album`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
                },
            body: JSON.stringify({ album_id: album_id })
        })
        .then(response => {
            if (response.ok) {
                alert("Album deleted successfully!");
                window.location.href = "/collection";
            } else {
                alert("Failed to delete album. Please try again.");
            }
        });
    }
}