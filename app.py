
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini client
client = genai.Client(api_key=API_KEY) if API_KEY else None

# Page configuration
st.set_page_config(
    page_title="AI Email Generator",
    page_icon="📧",
    layout="centered"
)

# Custom styling
st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
h1 {
    color: #8AB4F8;
    text-align: center;
}
.subtitle {
    text-align: center;
    color: #B0BEC5;
}
.stButton>button {
    background-color: #4285F4;
    color: white;
    border-radius: 10px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# Application heading
st.title("📧 AI Email Generator")
st.markdown(
    '<p class="subtitle">Your intelligent assistant for writing professional emails.</p>',
    unsafe_allow_html=True
)

st.divider()

# Select operation
st.subheader("Compose Your Email")

operation = st.selectbox(
    "What would you like to do?",
    ["Write a New Email", "Rewrite an Email", "Generate an Email Reply"]
)

# Recipient
recipient = st.text_input(
    "Recipient",
    placeholder="e.g. Professor, HR Manager, Team Leader"
)

# Email purpose or existing content
if operation == "Write a New Email":
    content = st.text_area(
        "What should the email be about?",
        placeholder="Describe your email requirements...",
        height=130
    )
elif operation == "Rewrite an Email":
    content = st.text_area(
        "Paste your existing email",
        placeholder="Paste the email you want to improve...",
        height=160
    )
else:
    content = st.text_area(
        "Paste the email you received",
        placeholder="Paste the message you want to reply to...",
        height=160
    )

col1, col2 = st.columns(2)

with col1:
    category = st.selectbox(
        "Email Category",
        ["Professional", "Formal", "Academic", "Informal", "Business"]
    )

    tone = st.selectbox(
        "Preferred Tone",
        ["Polite", "Friendly", "Persuasive",
         "Apologetic", "Confident", "Appreciative"]
    )

with col2:
    length = st.selectbox(
        "Email Length",
        ["Short", "Medium", "Detailed"]
    )

    language = st.selectbox(
        "Language",
        ["English", "Simple English", "Hindi"]
    )

# Generate button
if st.button("✨ Generate Email"):

    if not recipient.strip() or not content.strip():
        st.warning("Please fill in the recipient and email content.")

    elif not client:
        st.error("Gemini API key is missing. Please check your .env file.")

    else:
        if operation == "Write a New Email":
            task = "Write a completely new email based on the user's requirements."
        elif operation == "Rewrite an Email":
            task = "Rewrite and improve the provided email while preserving its original meaning."
        else:
            task = "Write an appropriate reply to the provided email."

        prompt = f"""
        You are an expert professional email writing assistant.

        TASK:
        {task}

        RECIPIENT: {recipient}
        CATEGORY: {category}
        TONE: {tone}
        LENGTH: {length}
        LANGUAGE: {language}

        USER INPUT:
        {content}

        INSTRUCTIONS:
        1. Generate a suitable subject line.
        2. Include an appropriate greeting.
        3. Write a clear and meaningful email.
        4. Maintain the requested tone and length.
        5. Include an appropriate closing.
        6. Do not invent facts or personal details.
        7. Use placeholders for missing sender information.
        8. Return the subject and complete email body.
        """

        try:
            with st.spinner("✨ AI is preparing your email..."):

                response = client.models.generate_content(
                    model="gemini-flash-latest",
                    contents=prompt
                )

                result = response.text

                if result:
                    st.session_state["generated_email"] = result
                else:
                    st.error("The AI returned an empty response.")

        except Exception as e:
            st.error(f"Generation failed: {e}")

# Display result
if "generated_email" in st.session_state:

    st.divider()
    st.subheader("✨ Your Generated Email")

    email = st.session_state["generated_email"]

    edited_email = st.text_area(
        "Review and edit your email",
        value=email,
        height=300
    )

    st.download_button(
        label="⬇️ Download Email",
        data=edited_email,
        file_name="generated_email.txt",
        mime="text/plain"
    )

    if st.button("🔄 Clear and Start Again"):
        del st.session_state["generated_email"]
        st.rerun()

    st.success("Your email is ready!")
    
st.divider()

st.caption("Powered by Google Gemini | AI Email Generator")
