import os
from pdf2image import convert_from_path
from gtts import gTTS
from moviepy.editor import (
    ImageClip, TextClip, CompositeVideoClip,
    AudioFileClip, concatenate_videoclips
)


# ======================================================
# STEP 1 — Convert PDF pages into images (organized by lesson)
# ======================================================
def extract_images_from_pdf(pdf_path, output_root, poppler_path):
    """
    Converts PDF pages into PNG images and saves them in Lesson folders.
    """
    os.makedirs(output_root, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=200, poppler_path=poppler_path)

    image_paths = []
    for i, page in enumerate(pages, start=1):
        lesson_folder = os.path.join(output_root, f"Lesson_{i}")
        os.makedirs(lesson_folder, exist_ok=True)
        image_file = os.path.join(lesson_folder, f"page_{i}.png")
        page.save(image_file, "PNG")
        image_paths.append(image_file)
        print(f"✅ Saved: {image_file}")

    return image_paths


# ======================================================
# STEP 2 — Synthesize video from text + images
# ======================================================
def synthesize_video_from_text(prompt, image_path=None, out_path="output_explanation_video.mp4"):
    """
    Generates an educational video using:
    - gTTS for narration
    - MoviePy for text overlay on top of a background image
    """
    try:
        # 1️⃣ Convert text to speech
        audio_path = "temp_audio.mp3"
        gTTS(prompt, lang='en').save(audio_path)

        # 2️⃣ Load audio and determine duration
        audio_clip = AudioFileClip(audio_path)
        duration = audio_clip.duration

        # 3️⃣ Create background (image or color)
        if image_path and os.path.exists(image_path):
            bg_clip = ImageClip(image_path).resize((1280, 720)).set_duration(duration)
        else:
            bg_clip = TextClip("", size=(1280, 720), bg_color='black', duration=duration)

        # 4️⃣ Create text overlay
        txt_clip = TextClip(
            prompt,
            fontsize=40, color='white', size=(1100, 600),
            method='caption', align='center'
        ).set_position('center').set_duration(duration)

        # 5️⃣ Combine video + audio + text
        final_clip = CompositeVideoClip([bg_clip, txt_clip])
        final_clip = final_clip.set_audio(audio_clip)

        # 6️⃣ Export video
        final_clip.write_videofile(out_path, fps=24, codec='libx264', audio_codec='aac')

        # Cleanup
        audio_clip.close()
        if os.path.exists(audio_path):
            os.remove(audio_path)

        print(f"🎬 Video created: {out_path}")
        return out_path

    except Exception as e:
        print("❌ Video generation failed:", e)
        return None


# ======================================================
# STEP 3 — High-level function
# ======================================================
def generate_video_from_pdf_and_text(pdf_path, text_prompt, poppler_path, output_root="Samacheer_Images"):
    """
    Converts a Samacheer textbook PDF into lesson images and
    generates an educational video using the explanation text.
    """
    # Extract images
    image_paths = extract_images_from_pdf(pdf_path, output_root, poppler_path)

    if not image_paths:
        return None, "❌ No images extracted from PDF."

    # Pick first lesson image as background for video
    first_image = image_paths[0]
    print(f"🎨 Using {first_image} as video background")

    # Generate video
    video_path = synthesize_video_from_text(text_prompt, image_path=first_image)
    if not video_path:
        return None, "❌ Video synthesis failed."

    return video_path, None


# ======================================================
# Example usage
# ======================================================
if __name__ == "__main__":
    pdf_path = r"C:\Users\LENOVO\Documents\Samacheer_Textbook.pdf"
    poppler_path = r"C:\poppler\poppler-25.07.0\Library\bin"
    explanation_text = (
        "Photosynthesis is the process by which green plants convert sunlight into food. "
        "It occurs mainly in the leaves where chlorophyll absorbs light energy."
    )

    video_path, error = generate_video_from_pdf_and_text(
        pdf_path, explanation_text, poppler_path
    )

    if error:
        print(error)
    else:
        print(f"✅ Final video saved at: {video_path}")
