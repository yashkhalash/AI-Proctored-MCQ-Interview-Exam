import streamlit as st
from exam_engine import ExamEngine
from proctor import Proctor
from storage import save_result
from network import NetworkMonitor

st.set_page_config(page_title="AI Interview Exam", page_icon="🎯", layout="wide")

if "engine" not in st.session_state:
    st.session_state.engine = ExamEngine()
if "proctor" not in st.session_state:
    st.session_state.proctor = Proctor()
if "started" not in st.session_state:
    st.session_state.started = False
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "camera_consent" not in st.session_state:
    st.session_state.camera_consent = False

@st.dialog("Camera Access Required")
def camera_permission_modal():
    st.write(
        "This exam uses your webcam to proctor the session — checking for your "
        "face, detecting when you look away, and flagging multiple faces in frame."
    )
    st.caption("No video is uploaded anywhere; frames are analyzed locally in this session only.")
    if st.button("Enable Camera", type="primary"):
        st.session_state.camera_consent = True
        st.rerun()

st.title("🎯 AI-Proctored MCQ Interview Exam")
st.caption("Local-first demo: MCQs + webcam proctoring + offline/network recovery.")

with st.sidebar:
    st.header("Exam Controls")
    duration = st.number_input("Duration (minutes)", 1, 180, 30)
    warning_limit = st.number_input("Warnings before disqualification", 1, 10, 2)
    st.session_state.proctor.warning_limit = warning_limit
    st.divider()
    st.write("Rules")
    st.write("• Look away / no face / multiple faces can generate warnings.")
    st.write("• 2 warnings → final warning.")
    st.write("• 3rd violation → disqualification.")
    st.write("• Network interruptions are queued locally.")

if not st.session_state.started:
    st.subheader("Candidate Setup")
    name = st.text_input("Candidate name")
    if st.button("Start Exam", type="primary", disabled=not name.strip()):
        st.session_state.candidate = name.strip()
        st.session_state.started = True
        st.rerun()
    st.info("Camera permission is required for proctoring.")
    st.stop()

if st.session_state.submitted:
    if st.session_state.get("disqualified"):
        st.error("❌ Exam auto-submitted: disqualified for repeated proctoring violations.")
    else:
        st.success("Exam submitted.")
    st.stop()

candidate = st.session_state.candidate
st.write(f"Candidate: **{candidate}**")

alert_slot = st.empty()
violations = st.session_state.proctor.violations
limit = st.session_state.proctor.warning_limit
if violations > 0:
    with alert_slot.container():
        st.markdown(
            f"""
            <div style="background-color:#4a0000;border:2px solid #ff4b4b;
                        border-radius:8px;padding:14px 18px;margin-bottom:12px;">
                <span style="color:#ff4b4b;font-weight:700;font-size:1.05rem;">
                    🔴 Proctoring Warning {violations}/{limit + 1}
                </span><br>
                <span style="color:#ffcccc;">
                    {st.session_state.proctor.events[-1]['message']}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

col1, col2 = st.columns([2,1])
with col1:
    st.subheader("MCQ Exam")
    question = st.session_state.engine.current_question()
    if question is None:
        st.warning("No questions available.")
    else:
        st.markdown(f"### Q{st.session_state.engine.index + 1}. {question['question']}")
        answer = st.radio("Choose one answer", question["options"], key=f"q_{st.session_state.engine.index}")
        if st.button("Next / Submit", type="primary"):
            st.session_state.engine.answer(answer)
            if st.session_state.engine.finished:
                result = st.session_state.engine.result()
                save_result(candidate, result)
                st.session_state.submitted = True
            st.rerun()

with col2:
    st.subheader("Webcam")
    if not st.session_state.camera_consent:
        st.info("Camera access is required to continue the proctored exam.")
        if st.button("Request Camera Access"):
            camera_permission_modal()
    else:
        camera = st.camera_input("Take a proctoring frame", key="proctor_camera")
        if camera:
            event = st.session_state.proctor.analyze(camera.getvalue())
            if event:
                if event["disqualified"]:
                    st.toast("❌ Final warning — exam disqualified", icon="🚨")
                    st.error("🚨 FINAL WARNING: Exam auto-submitted due to repeated violations.")
                    save_result(candidate, {
                        **st.session_state.engine.result(),
                        "status": "DISQUALIFIED",
                        "proctor": st.session_state.proctor.summary()
                    })
                    st.session_state.submitted = True
                    st.session_state.disqualified = True
                    st.rerun()
                else:
                    st.toast(event["message"], icon="⚠️")
                    st.rerun()
        else:
            st.caption("For a production implementation, use continuous browser webcam capture via a custom Streamlit component/WebRTC.")

    st.divider()
    monitor = NetworkMonitor()
    online = monitor.is_online()
    st.metric("Network", "ONLINE" if online else "OFFLINE")
    st.caption("Answers are maintained in Streamlit session state; production deployment should persist an encrypted local queue.")

if st.session_state.proctor.events:
    with st.expander("Proctoring event log"):
        for e in st.session_state.proctor.events:
            st.write(e)
