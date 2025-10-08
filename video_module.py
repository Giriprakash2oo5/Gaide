import os
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
from moviepy.editor import concatenate_videoclips
from gtts import gTTS  # For text-to-speech

def synthesize_video_from_text(prompt, out_path="output_explanation_video.mp4"):
    """
    Generate a simple educational video using moviepy + gTTS.
    """
    try:
        # Step 1: Convert text to speech
        tts = gTTS(prompt, lang='en')
        audio_path = "temp_audio.mp3"
        tts.save(audio_path)

        # Step 2: Create text overlay video
        txt_clip = TextClip(prompt, fontsize=40, color='white', size=(1280, 720),
                            bg_color='black', method='caption', align='center')

        # Duration matches audio
        audio_clip = AudioFileClip(audio_path)
        txt_clip = txt_clip.set_duration(audio_clip.duration)
        txt_clip = txt_clip.set_audio(audio_clip)

        # Step 3: Export final video
        txt_clip.write_videofile(out_path, fps=24, codec='libx264', audio_codec='aac')

        # Clean up temp audio
        if os.path.exists(audio_path):
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
