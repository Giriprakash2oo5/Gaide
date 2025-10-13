# animation_module.py

import os
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip, concatenate_videoclips
from gtts import gTTS  # For text-to-speech
import random
import string

def generate_ai_animation_video(explanation_text, out_path=None):
    """
    Generate a 2D AI-style animation video from explanation text.
    Uses gTTS for speech and MoviePy for simple text + animation.
    """

    try:
        if not explanation_text.strip():
            return None, "❌ Empty explanation text provided."

        # Generate a temporary audio file from the text
        audio_file = "temp_audio.mp3"
        tts = gTTS(explanation_text, lang="en")
        tts.save(audio_file)
        audio_clip = AudioFileClip(audio_file)

        # Create multiple text clips with slight random positions for "animation" effect
        words = explanation_text.split()
        clips = []
        for i in range(0, len(words), 10):  # Chunk 10 words at a time
            chunk = " ".join(words[i:i+10])
            txt_clip = TextClip(
                chunk,
                fontsize=40,
                color=random.choice(["white", "yellow", "cyan", "orange"]),
                size=(1280, 720),
                method="caption",
                align="center",
                bg_color="black",
            )
            # Random duration and position
            txt_clip = txt_clip.set_duration(max(1.5, audio_clip.duration / (len(words)/10)))
            txt_clip = txt_clip.set_position(
                ("center", random.randint(100, 600))
            )
            clips.append(txt_clip)

        # Concatenate all text clips
        video_clip = concatenate_videoclips(clips, method="compose")
        video_clip = video_clip.set_audio(audio_clip)

        # Set output path
        if not out_path:
            random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
            out_path = f"ai_animation_{random_suffix}.mp4"

        # Export video
        video_clip.write_videofile(
            out_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )

        # Cleanup temporary files
        if os.path.exists(audio_file):
            os.remove(audio_file)

        return out_path, None

    except Exception as e:
        return None, f"❌ AI animation video generation failed: {e}"
