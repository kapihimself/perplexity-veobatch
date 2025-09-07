import os, subprocess, uuid, tempfile
from imageio_ffmpeg import get_ffmpeg_exe

def extract_frames(src, dst, fps, sample_rate):
    os.makedirs(dst, exist_ok=True)
    cmd = [get_ffmpeg_exe(), "-i", src, "-vf", f"fps={fps}/{sample_rate}", os.path.join(dst, "frame_%06d.png")]
    subprocess.run(cmd, check=True)
    return sorted(os.listdir(dst))

def assemble_video(frames_dir, fps, out_path):
    cmd = [get_ffmpeg_exe(), "-framerate", str(fps), "-i", f"{frames_dir}/edited_%06d.png",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", out_path]
    subprocess.run(cmd, check=True)

def mix_audio(video_path, src_video, out_path):
    cmd = ["ffmpeg", "-i", video_path, "-i", src_video, "-map", "0:v", "-map", "1:a",
           "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", out_path]
    subprocess.run(cmd, check=True)
