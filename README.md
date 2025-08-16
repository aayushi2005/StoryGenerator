# 🖍️ AI Storybook Generator

Welcome to **AI Storybook Generator**, a **Streamlit web app** that creates multi-page children's storybooks using **AI-generated text and images**. This project leverages **Google Gemini AI** to produce engaging stories with visuals, making it perfect for parents, teachers, and kids who love creative storytelling. 📚✨

---

## 🌟 Features

-  **AI-Generated Story Text:** Generates engaging and age-appropriate text for each page.  
-  **AI-Generated Images:** Visual illustrations matching the story content.  
-  **Multiple Story Types:** Choose from Fiction, Adventure, Mystery, Fantasy, Sci-Fi, Comedy, Educational.  
-  **Detailed Stories:** ~150–200 words per page with dialogues, emotions, and vivid descriptions.  
-  **PDF Output:** Download the full storybook as a professionally formatted PDF.  
-  **Streamlit Interface:** Simple and interactive web interface for easy use.  
-  **Page Preview:** Preview the first page image before downloading.  
-  **Customizable Pages:** Choose the number of pages (1–10).  

---

## 🧩 How It Works

1. **User Input:**  
   - Enter a story prompt (e.g., "A robot exploring a magical forest").  
   - Select the story type (genre).  
   - Choose the number of pages.  

2. **Story Generation:**  
   - Each page prompt is sent to **Google Gemini AI**.  
   - The AI generates **detailed text** (~150–200 words) including dialogues, emotions, and descriptions.  
   - It also generates an **image** matching the page content.  

3. **PDF Creation:**  
   - Uses **ReportLab** to compile all text and images into a single PDF.  
   - Adds headings for each page.  
   - Allows preview and download via Streamlit.  

---
