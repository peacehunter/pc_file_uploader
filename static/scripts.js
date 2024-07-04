function uploadFiles() {
    var form = document.getElementById('upload-form');
    var formData = new FormData(form);
    var xhr = new XMLHttpRequest();

    xhr.open('POST', '/', true);

    xhr.upload.addEventListener('progress', function(e) {
        if (e.lengthComputable) {
            var percentComplete = (e.loaded / e.total) * 100;
            document.getElementById('progress-bar').style.width = percentComplete + '%';
            document.getElementById('progress-text').textContent = Math.round(percentComplete) + '%';
        }
    });

    xhr.addEventListener('load', function() {
        if (xhr.status == 200) {
            var response = JSON.parse(xhr.responseText);
            document.getElementById('message').textContent = response.message;
        } else {
            document.getElementById('message').textContent = 'An error occurred while uploading the files.';
        }
        closeModal();
    });

    xhr.send(formData);
    showModal();
}

function showModal() {
    document.getElementById('upload-modal').style.display = 'block';
}

function closeModal() {
    document.getElementById('upload-modal').style.display = 'none';
}
