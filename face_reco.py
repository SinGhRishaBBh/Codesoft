import cv2 # type: ignore
import numpy as np
import face_recognition # type: ignore

class FaceDetectionRecognition:
    def __init__(self):
        # Load the pre-trained face detection model
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize empty lists for known face encodings and names
        self.known_face_encodings = []
        self.known_face_names = []

    def add_known_face(self, image_path, name):
        # Load the image and compute the face encoding
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        
        # Add the encoding and name to our lists
        self.known_face_encodings.append(encoding)
        self.known_face_names.append(name)

    def detect_and_recognize_faces(self, image):
        # Convert the image to grayscale for face detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Detect faces using the Haar cascade classifier
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Convert the image from BGR to RGB for face recognition
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Find all face locations and face encodings in the current frame
        face_locations = face_recognition.face_locations(rgb_image)
        face_encodings = face_recognition.face_encodings(rgb_image, face_locations)
        
        # Initialize list for face names
        face_names = []
        
        for face_encoding in face_encodings:
            # Compare the face with known faces
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            
            # Find the best match
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = self.known_face_names[best_match_index]
            
            face_names.append(name)
        
        # Draw rectangles and names for detected faces
        for (x, y, w, h), name in zip(faces, face_names):
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(image, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        return image

    def process_video(self, video_path=0):  # 0 for webcam, or provide a video file path
        cap = cv2.VideoCapture(video_path)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = self.detect_and_recognize_faces(frame)
            
            cv2.imshow('Face Detection and Recognition', processed_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# Usage example
if __name__ == "__main__":
    fdr = FaceDetectionRecognition()
    
    # Add known faces (replace with your own images and names)
    fdr.add_known_face("path_to_known_face1.jpg", "Person 1")
    fdr.add_known_face("path_to_known_face2.jpg", "Person 2")
    
    # Process video (use 0 for webcam or provide a video file path)
    fdr.process_video(0)