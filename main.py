import streamlit as st
import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as RLImage, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------- Google Gemini Client ----------
client = genai.Client(api_key="AIzaSyB9KSN5Tsn-wZua99GtnxnjCstAITw3L-U")  # Replace with your key

# ---------- IMAGE + TEXT GENERATION ----------
def generate_text_and_image(prompt: str):
    response = client.models.generate_content(
        model="gemini-2.0-flash-preview-image-generation",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        ),
    )

    generated_texts = []
    generated_images = []

    for part in response.candidates[0].content.parts:
        if part.text:
            generated_texts.append(part.text)
        elif part.inline_data:
            img = Image.open(BytesIO(part.inline_data.data))
            generated_images.append(img)

    return generated_texts, generated_images

# ---------- STORY GENERATION ----------
def generate_story(prompt: str, pages: int = 5):
    story_pages = []
    for i in range(1, pages + 1):
        page_prompt = f"Page {i} of a children's story: {prompt}"
        texts, images = generate_text_and_image(page_prompt)

        page_text = texts[0] if texts else f"Page {i}: (No text generated)"
        page_image = images[0] if images else None
        story_pages.append((page_text, page_image))
    return story_pages

# ---------- PDF CREATION ----------
def create_pdf(story_pages, output_file="storybook.pdf"):
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    for i, (text, image) in enumerate(story_pages, start=1):
        elements.append(Paragraph(f"<b>Page {i}</b>", styles["Heading2"]))
        elements.append(Paragraph(text, styles["Normal"]))
        elements.append(Spacer(1, 12))

        if image:
            img_path = f"temp_page_{i}.png"
            image.save(img_path)
            elements.append(RLImage(img_path, width=350, height=250))
            elements.append(Spacer(1, 24))

    doc.build(elements)
    return output_file

# ---------- STREAMLIT APP ----------
st.title("🖍️ Children's Storybook Generator")
st.write("Enter a story prompt and generate a multi-page storybook with images.")

# User inputs
user_prompt = st.text_area("Story Prompt:", "")
pages = st.number_input("Number of pages:", min_value=1, max_value=10, value=5)

if st.button("Generate Storybook"):
    if user_prompt.strip() == "":
        st.error("Please enter a story prompt.")
    else:
        with st.spinner("Generating storybook... This may take a minute!"):
            story_pages = generate_story(user_prompt, pages=pages)
            pdf_file = create_pdf(story_pages)
        st.success("Storybook generated!")

        # Provide PDF download
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Download Storybook PDF",
                data=f,
                file_name="storybook.pdf",
                mime="application/pdf"
            )

        # Show preview of first page image
        if story_pages[0][1]:
            st.image(story_pages[0][1], caption="Preview: Page 1")