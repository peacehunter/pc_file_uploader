from flask import Flask, request, render_template_string, send_from_directory, jsonify
import os

app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the HTML form with external CSS and JavaScript
html_form = '''
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Upload Files</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="upload-container">
        <h1>Upload Files</h1>
        <form id="upload-form" method="post" enctype="multipart/form-data">
            <input type="file" id="file-input" name="file[]" multiple>
            <input type="button" value="Upload" onclick="uploadFiles()">
        </form>
        <div id="message"></div>
    </div>

    <div id="upload-modal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeModal()">&times;</span>
            <h2>Uploading Files</h2>
            <div id="progress-container">
                <div id="progress-bar"></div>
            </div>
            <p id="progress-text">0%</p>
        </div>
    </div>

    <script src="/static/scripts.js"></script>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'POST':
        files = request.files.getlist('file[]')
        if not files:
            return jsonify({'message': 'No selected files'}), 400

        num_files = 0
        for file in files:
            if file.filename == '':
                continue
            if file:
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                num_files += 1

        message = f'{num_files} file(s) successfully uploaded'
        return jsonify({'message': message}), 200

    return render_template_string(html_form)

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
