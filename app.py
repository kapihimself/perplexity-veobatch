import os, tempfile, uuid, subprocess
import streamlit as st
from src.utils import extract_frames, assemble_video, mix_audio
from src.nano_banana import edit_frame
from src.orchestrator import build_manifest

st.set_page_config(layout="wide", page_title="Veobatch Clone")
st.sidebar.title("Veobatch Controls")
video_file = st.sidebar.file_uploader("Upload Video", type=["mp4","mov"])
video_url  = st.sidebar.text_input("Video URL")
presets    = {"Neon Noir":"Teal/magenta high contrast grain","Retro Film":"Sepia grain FX"}
choice     = st.sidebar.selectbox("Preset", list(presets.keys()))
fps        = st.sidebar.slider("FPS", 1,60,24)
sample_r   = st.sidebar.slider("Sample Rate", 1,5,2)
if st.sidebar.button("Run Pipeline"):
    tmp = tempfile.mkdtemp()
    src = os.path.join(tmp, video_file.name) if video_file else os.path.join(tmp,f"{uuid.uuid4()}.mp4")
    if video_file:
        with open(src,"wb") as f: f.write(video_file.read())
    else:
        subprocess.run(["ffmpeg","-i",video_url,"-c","copy",src], check=True)

    frames_dir = os.path.join(tmp,"frames"); os.makedirs(frames_dir)
    frame_files = extract_frames(src, frames_dir, fps, sample_r)
    edited_dir = os.path.join(tmp,"edited"); os.makedirs(edited_dir)

    progress = st.progress(0); preview = st.empty()
    for i, fn in enumerate(frame_files):
        raw = os.path.join(frames_dir, fn)
        out = edit_frame(raw, presets[choice], 10000)
        dest = os.path.join(edited_dir,f"edited_{i:06d}.png")
        with open(dest,"wb") as f: f.write(out)
        if i % max(1,len(frame_files)//10)==0:
            preview.image(dest, width=320)
        progress.progress((i+1)/len(frame_files))

    no_audio = os.path.join(tmp,"no_audio.mp4")
    assemble_video(edited_dir, fps, no_audio)
    final = os.path.join(tmp,"final.mp4")
    mix_audio(no_audio, src, final)

    st.video(final)
    manifest = build_manifest(video_url or video_file.name, choice, fps, "1280x720", True, sample_r)
    st.code(manifest, language="json")
