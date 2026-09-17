from datetime import datetime
import cv2
import numpy as np

class Proctor:
    """
    Lightweight demo detector.
    It intentionally does NOT claim to be a definitive cheating detector.
    For production, replace/augment with a calibrated MediaPipe/ONNX model.
    """

    def __init__(self):
        self.warning_limit = 2
        self.violations = 0
        self.events = []
        self.face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.eye = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    def analyze(self, image_bytes):
        arr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if frame is None:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face.detectMultiScale(gray, 1.1, 5, minSize=(80,80))

        reason = None
        if len(faces) == 0:
            reason = "No face detected. Please face the camera."
        elif len(faces) > 1:
            reason = "Multiple faces detected. Only one candidate should be visible."
        else:
            x,y,w,h = faces[0]
            roi = gray[y:y+h, x:x+w]
            eyes = self.eye.detectMultiScale(roi, 1.1, 5, minSize=(18,18))
            if len(eyes) == 0:
                reason = "Eyes were not detected. Please look toward the camera."

        if reason is None:
            return None

        self.violations += 1
        event = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "violation": self.violations,
            "message": f"⚠️ Warning {self.violations}: {reason}",
            "disqualified": self.violations >= self.warning_limit + 1
        }
        self.events.append(event)
        return event

    def summary(self):
        return {"violations": self.violations, "events": self.events}
