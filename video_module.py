# video_module.py
import os
import tempfile
import streamlit as st
from moviepy.editor import TextClip, AudioFileClip
from gtts import gTTS

def synthesize_video_from_text(prompt):
    """
    Generate a video from text using moviepy + gTTS in a cloud-safe way.
    All temporary files are created in /tmp or temporary file objects.
    """
    try:
        if not prompt.strip():
            return None, "❌ Empty prompt, cannot generate video."

        st.info("🎤 Generating audio from text...")
        # Temp file for audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            audio_path = f.name
        tts = gTTS(prompt, lang='en')
        tts.save(audio_path)

        st.info("📝 Creating video clip...")
        # Text clip (lower resolution for cloud)
        txt_clip = TextClip(
            prompt,
            fontsize=30,
            color='white',
            size=(720, 480),
            bg_color='black',
            method='caption',
            align='center'
        )

        # Attach audio
        audio_clip = AudioFileClip(audio_path)
        txt_clip = txt_clip.set_duration(audio_clip.duration)
        txt_clip = txt_clip.set_audio(audio_clip)

        # Temp file for video
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            video_path = f.name

        st.info("🎬 Rendering video...")
        txt_clip.write_videofile(
            video_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            logger=None
        )

        # Clean up temp audio
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return video_path, None

    except Exception as e:
        return None, f"❌ Video generation failed: {e}"


def generate_video_from_text(text_prompt):
    """
    High-level function for Streamlit usage.
    Returns video file path or error message.
    """
    try:
        video_path, error = synthesize_video_from_text(text_prompt)
        if error:
            return None, error
        if not video_path or not os.path.exists(video_path):
            return None, "❌ Video synthesis failed."
        return video_path, None
    except Exception as e:
        return None, f"❌ Unexpected error: {e}"
