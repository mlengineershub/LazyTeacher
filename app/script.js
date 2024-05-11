document.getElementById('uploadBtn').addEventListener('click', function() {
    alert('Bouton de chargement cliqué!');
});

document.getElementById('uploadBtn').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        fetch('http://127.0.0.1:8000/upload/', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                console.log('Success:', data);
                document.getElementById('results').innerText = data.text;
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    } else {
        alert('Please select a file to upload.');
    }
});