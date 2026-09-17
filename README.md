# AI-Proctored MCQ Interview Exam

Python + Streamlit starter project for an interview/exam platform.

## Included

- MCQ exam engine
- Score and percentage calculation
- Candidate setup
- Webcam frame capture
- Face detection
- Eye detection
- Multiple-face detection
- No-face detection
- Warning counter
- Default policy: warning 1, warning 2, then disqualification on violation 3
- Network online/offline indicator
- Local JSON result storage
- Offline-friendly session state
- Modular code structure

## Important limitation

This starter uses OpenCV Haar cascades and Streamlit's `camera_input`, which captures frames rather than providing a guaranteed continuous real-time webcam stream. Eye detection is therefore a prototype, not a reliable high-stakes proctoring system.

For production, use a continuous webcam component (WebRTC/custom Streamlit component) and a calibrated face/landmark model such as MediaPipe Face Landmarker or an ONNX model. Treat gaze/eye-contact detection as a probabilistic signal and provide a review/appeal workflow rather than automatically judging candidates solely from one frame.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL shown by Streamlit.

## Production features to add

1. Continuous webcam stream at a controlled FPS.
2. Face landmarks + head-pose estimation.
3. Eye aspect ratio/blink detection.
4. Gaze direction estimation.
5. Face identity verification at exam start.
6. Tab/window focus events using a browser component.
7. Screen-share consent and recording policy where legally appropriate.
8. Question randomization and question banks.
9. Server-side encrypted exam/session state.
10. Automatic reconnect and local encrypted event queue.
11. Admin dashboard and candidate reports.
12. Manual review queue for proctoring events.
13. Accessibility accommodations and configurable rules.
14. Audit log with timestamps.
15. Rate limiting and authentication.
16. Database persistence (PostgreSQL recommended).
17. Object storage for approved evidence, with retention/deletion controls.

## Suggested architecture

Streamlit UI
  -> Exam Engine
  -> Proctoring Service
      -> Face detector
      -> Face landmarks
      -> Gaze/head pose
      -> Event/risk scoring
  -> Offline Queue
  -> API
  -> PostgreSQL
  -> Admin Dashboard

## Warning policy

The demo implements:
- Violation 1: Warning
- Violation 2: Warning / final warning
- Violation 3: Disqualification

In a real hiring/exam product, make the threshold configurable and avoid using gaze alone as proof of misconduct because camera angle, lighting, disability/accessibility needs, glasses, and hardware can cause false positives.
# AI-Proctored-MCQ-Interview-Exam
