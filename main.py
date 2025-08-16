import streamlit as st
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as RLImage, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------- Google Gemini Client ----------
client = genai.Client(api_key="YOUR_API_KEY_HERE")  # Replace with your API key

# ---------- Hardcoded Credentials ----------
USER_CREDENTIALS = {
    "admin": "admin123",
    "ayushi": "mypassword"
}

# ---------- Initialize Session State ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------- Login Function ----------
def login():
    st.title("🔒 AI Storybook Generator Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    
    login_pressed = st.button("Login")
    
    if login_pressed:
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Logged in as {username}")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

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
def generate_story(prompt: str, story_type: str, pages: int = 5):
    story_pages = []
    for i in range(1, pages + 1):
        page_prompt = (
            f"Page {i} of a {story_type.lower()} children's story: {prompt}. "
            "Write a detailed and engaging story for children, around 150–200 words, "
            "including dialogues, emotions, and vivid descriptions."
        )
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

# ---------- MAIN APP ----------
if not st.session_state.logged_in:
    login()
else:
    st.title(f"🖍️ Welcome to AI Storybook Generator")
    st.write("Enter a story prompt, select the type of story, and generate a storybook with AI-generated text and images.")

    # User Inputs
    user_prompt = st.text_area("Story Prompt:", "")
    story_type = st.selectbox(
        "Select Story Type:",
        ["Fiction", "Adventure", "Mystery", "Fantasy", "Sci-Fi", "Comedy", "Educational"]
    )
    pages = st.number_input("Number of pages:", min_value=1, max_value=10, value=5)

    if st.button("Generate Storybook"):
        if user_prompt.strip() == "":
            st.error("Please enter a story prompt.")
        else:
            with st.spinner("Generating storybook... This may take a few minutes!"):
                story_pages = generate_story(user_prompt, story_type, pages=pages)
                pdf_file = create_pdf(story_pages)
            st.success(f"{story_type} Storybook generated!")

            # PDF Download
            with open(pdf_file, "rb") as f:
                st.download_button(
                    label="📥 Download Storybook PDF",
                    data=f,
                    file_name="storybook.pdf",
                    mime="application/pdf"
                )

            # Preview first page
            if story_pages[0][1]:
                st.image(story_pages[0][1], caption="Preview: Page 1")
