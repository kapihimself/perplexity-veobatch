import json

def build_manifest(video_url, style, fps, resolution, preserve_audio, sample_rate):
    manifest = {
        "pipeline_steps": ["extract_frames","sample_frames","per_frame_edit","temporal_consistency_enforce","recompose_video","audio_mix","final_encode"],
        "input": {"video_url": video_url, "target_style": style, "fps_output": fps, "resolution": resolution, "preserve_audio": preserve_audio, "frame_sample_rate": sample_rate},
        "frames": []
    }
    # Sample only first 5 frames for demo
    for i in range(5):
        manifest["frames"].append({
            "frame_index": i,
            "frame_path": f"frames/frame_{i:06d}.png",
            "nano_banana_prompt": f"Apply {style}, frame {i}",
            "seed_hint": 10000,
            "api_parameters": {"model":"nano-banana","guidance_scale":9,"temperature":0.0}
        })
    manifest["final"] = {"video_path":"output.mp4","format":"mp4"}
    return json.dumps(manifest, indent=2)
