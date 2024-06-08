document.getElementById('uploadBtn').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('image', file);

        const progressBar = document.getElementById('progressBar');
        progressBar.style.width = '0%';
        document.getElementById('progressBarContainer').style.display = 'block';

        let progress = 0;
        const interval = setInterval(() => {
            if (progress < 100) {
                progress += 10;
                progressBar.style.width = progress + '%';
            } else {
                clearInterval(interval);
            }
        }, 100);

        fetch('/api/upload', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                clearInterval(interval);
                progressBar.style.width = '100%';
                console.log('Success:', data);
                document.getElementById('grade').innerText = data.note;
                document.getElementById('gradeOutput').style.display = 'block';
                // document.getElementById('results').innerText = data.text;
                // document.getElementById('results').style.display = 'block';
                document.getElementById('progressBarContainer').style.display = 'none';
                window.scrollTo(0, 0);
            })
            .catch((error) => {
                clearInterval(interval);
                progressBar.style.width = '0%';
                console.error('Error:', error);
                alert('Upload failed.');
                document.getElementById('progressBarContainer').style.display = 'none';
                document.getElementById('gradeOutput').style.display = 'none';
                // document.getElementById('results').style.display = 'none';
            });
    } else {
        alert('Please select a file to upload.');
    }
});

document.getElementById('refreshBtn').addEventListener('click', function () {
    window.location.reload();
});
