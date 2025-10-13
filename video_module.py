import os
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from moviepy.editor import concatenate_videoclips
from gtts import gTTS  # For text-to-speech
import tempfile

with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
    audio_path = f.name


def synthesize_video_from_text(prompt):
    try:
        # Use temp file for audio
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            audio_path = f.name

        tts = gTTS(prompt, lang='en')
        tts.save(audio_path)

        # Create text clip
        txt_clip = TextClip(prompt, fontsize=30, color='white', size=(720, 480),
                            bg_color='black', method='caption', align='center')

        audio_clip = AudioFileClip(audio_path)
        txt_clip = txt_clip.set_duration(audio_clip.duration)
        txt_clip = txt_clip.set_audio(audio_clip)

        # Save video in temp file
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f:
            out_path = f.name

        txt_clip.write_videofile(out_path, fps=24, codec='libx264', audio_codec='aac')

        # Clean up temp audio
        os.remove(audio_path)

        return out_path

    except Exception as e:
        print("❌ Video generation failed:", e)
        return None
    
def generate_video_from_text(text_prompt):
    """
    High-level function: takes explanation text and outputs a video file path.
    """
    if not text_prompt.strip():
        return None, "❌ Empty prompt, cannot generate video."

    try:
        local_video = synthesize_video_from_text(text_prompt)
        if not local_video or not os.path.exists(local_video):
            return None, "❌ Video synthesis failed."

        return local_video, None

    except Exception as e:
        return None, str(e)
    
