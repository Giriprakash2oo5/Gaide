import os
import tempfile
import streamlit as st
from moviepy.editor import TextClip, AudioFileClip
from gtts import gTTS
import numpy as np

def synthesize_video_from_text(prompt):
    """
    Generate a video from text using moviepy + gTTS in a cloud-safe way.
    Works without ImageMagick dependency on Streamlit Cloud.
    """
    try:
        if not prompt.strip():
            return None, "❌ Empty prompt, cannot generate video."

        st.info("🎤 Generating audio from text...")
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            audio_path = f.name
        gTTS(prompt, lang='en').save(audio_path)

        st.info("📝 Creating video clip (using PIL backend)...")
        # Explicitly force the caption method (no ImageMagick)
        txt_clip = TextClip(
            prompt,
            fontsize=30,
            color='white',
            size=(720, 480),
            bg_color='black',
            method='caption'
        )

        audio_clip = AudioFileClip(audio_path)
        txt_clip = txt_clip.set_duration(audio_clip.duration)
        txt_clip = txt_clip.set_audio(audio_clip)

        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            video_path = f.name

        st.info("🎬 Rendering video...")
        txt_clip.write_videofile(
            video_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            threads=4,          # safer for Streamlit Cloud
            logger=None
        )

        # Cleanup
        txt_clip.close()
        audio_clip.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return video_path, None

    except Exception as e:
        # Show full exception for debugging
        return None, f"❌ Video generation failed: {str(e)}"


def generate_video_from_text(text_prompt):
    """High-level function for Streamlit usage."""
    try:
        video_path, error = synthesize_video_from_text(text_prompt)
        if error:
            return None, error
        if not video_path or not os.path.exists(video_path):
            return None, "❌ Video synthesis failed."
        return video_path, None
    except Exception as e:
        return None, f"❌ Unexpected error: {e}"
