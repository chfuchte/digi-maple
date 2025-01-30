from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configurations for file uploads
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size

# In-memory storage for markers (you can replace it with a database if needed)
markers = markers.db []

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route to upload a map image
@app.route('/upload-map', methods=['POST'])
def upload_map():
    if 'map' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['map']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'map_url': url_for('uploaded_file', filename=filename)}), 200
    return jsonify({'error': 'File type not allowed'}), 400

# Route to serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return app.send_static_file(f'uploads/{filename}')

# Route to add a marker
@app.route('/add-marker', methods=['POST'])
def add_marker():
    data = request.json
    x = data.get('x')
    y = data.get('y')
    marker_type = data.get('type')
    map_url = data.get('mapUrl')
    
    if x is None or y is None or marker_type is None or map_url is None:
        return jsonify({'error': 'Missing marker data'}), 400

    marker = {'x': x, 'y': y, 'type': marker_type, 'map_url': map_url}
    markers.append(marker)
    return jsonify({'message': 'Marker added successfully', 'marker': marker}), 200

# Route to get all markers for a map
@app.route('/get-markers', methods=['GET'])
def get_markers():
    return jsonify(markers), 200

# Route to render the main page (HTML for interacting with the map)
@app.route('/')
def index():
    return render_template('indexx.html')

if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
