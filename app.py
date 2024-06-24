import os
import face_recognition
import numpy as np
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
import pandas as pd
import json
import logging
import traceback
from PIL import Image
import cv2
import io

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
KNOWN_FACES_FOLDER = 'known_faces'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['KNOWN_FACES_FOLDER'] = KNOWN_FACES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max-limit

# Ensure the upload and known_faces folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(KNOWN_FACES_FOLDER, exist_ok=True)

# Load known students from a JSON file
KNOWN_STUDENTS_FILE = 'known_students.json'

def load_known_students():
    if os.path.exists(KNOWN_STUDENTS_FILE):
        with open(KNOWN_STUDENTS_FILE, 'r') as f:
            data = json.load(f)
            return {k: np.array(v) for k, v in data.items()}
    return {}

def save_known_students(known_students):
    data = {k: v.tolist() for k, v in known_students.items()}
    with open(KNOWN_STUDENTS_FILE, 'w') as f:
        json.dump(data, f)

# Initialize known_students globally
known_students = {}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def before_request():
    global known_students
    known_students = load_known_students()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    if not known_students:
        return jsonify({"error": "No trained faces found. Please train the model first."}), 400

    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Read file directly from memory
            image = face_recognition.load_image_file(file)
            
            # Find all faces in the image
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Clear previous attendance data and initialize a new attendance list
            attendance = []
            matched_faces = set()

            # Check each detected face against our known faces
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(list(known_students.values()), face_encoding)
                face_distances = face_recognition.face_distance(list(known_students.values()), face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = list(known_students.keys())[best_match_index]
                    if name not in matched_faces:
                        matched_faces.add(name)
                        status = "Present"
                        attendance.append({"name": name, "status": status})
                else:
                    name = "Unknown"
                    status = "Present"
                    attendance.append({"name": name, "status": status})

            # Add absent students
            present_students = set(student["name"] for student in attendance if student["status"] == "Present")
            for student in known_students.keys():
                if student not in present_students:
                    attendance.append({"name": student, "status": "Absent"})

            return jsonify({"attendance": attendance})
        
        except Exception as e:
            logger.error(f"Error in process_image: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": f"An error occurred while processing the image: {str(e)}"}), 500
    
    return jsonify({"error": "Invalid file type"}), 400

@app.route('/download_excel', methods=['POST'])
def download_excel():
    attendance_data = request.json.get('attendance', [])
    df = pd.DataFrame(attendance_data)
    
    # Create an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Attendance', index=False)
    
    output.seek(0)
    
    return send_file(
        output,
        as_attachment=True,
        download_name='attendance.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

@app.route('/train_model', methods=['POST'])
def train_model():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        try:
            # Read file directly from memory
            image = face_recognition.load_image_file(file)

            # Get face encoding
            face_encodings = face_recognition.face_encodings(image)
            logger.info(f"Face encodings found: {len(face_encodings)}")

            if len(face_encodings) == 0:
                return jsonify({"error": "No face detected in the image"}), 400

            if len(face_encodings) > 1:
                return jsonify({"error": "Multiple faces detected. Please use an image with only one face."}), 400

            face_encoding = face_encodings[0]

            # Get the student name (without file extension)
            student_name = os.path.splitext(secure_filename(file.filename))[0]

            # Add to known_students
            known_students[student_name] = face_encoding

            # Save updated known_students
            save_known_students(known_students)

            logger.info(f"Successfully added {student_name} to the known faces")
            return jsonify({"message": f"Successfully added {student_name} to the known faces"}), 200

        except Exception as e:
            logger.error(f"Error in train_model: {str(e)}")
            logger.error(traceback.format_exc())
            return jsonify({"error": f"An error occurred: {str(e)}"}), 500

    return jsonify({"error": "Invalid file type"}), 400

if __name__ == '__main__':
    app.run(debug=True)
