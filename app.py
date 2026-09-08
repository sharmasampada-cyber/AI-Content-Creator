import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="AI Content Creator Suite",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Content Creator Suite")
st.write("Create amazing content with AI ✨")

st.divider()

# Store history
if "history" not in st.session_state:
    st.session_state.history = []

st.header("✨ Create Your Content")

content_type = st.selectbox(
    "What do you want to create?",
    [
        "Instagram Caption",
        "Blog Post",
        "YouTube Description",
        "Tweet",
        "LinkedIn Post"
    ]
)

topic = st.text_input(
    "💡 Enter your topic",
    placeholder="Example: College trip, AI, Friendship..."
)

tone = st.selectbox(
    "🎭 Choose the tone",
    ["Professional", "Casual", "Funny", "Creative", "Inspirational"]
)

language = st.selectbox(
    "🌐 Choose language",
    ["English", "Hindi", "Hinglish"]
)

length = st.selectbox(
    "📏 Content length",
    ["Short", "Medium", "Long"]
)

include_hashtags = st.checkbox("🏷️ Generate hashtags")

# Generate
if st.button("🚀 Generate Content", use_container_width=True):

    if not topic:
        st.warning("⚠️ Please enter a topic first.")

    else:

        prompt = f"""
        Create a {content_type} about: {topic}.

        Tone: {tone}
        Language: {language}
        Length: {length}

        Make it engaging, natural and suitable
        for the selected platform.
        """

        if include_hashtags:
            prompt += """
            Also generate 5-10 relevant hashtags
            at the end.
            """

        with st.spinner("✨ Creating your content..."):

            try:
                response = client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )

                generated_content = response.output_text

                # Save latest content
                st.session_state.current_content = generated_content

                # Save history
                st.session_state.history.append({
                    "type": content_type,
                    "topic": topic,
                    "tone": tone,
                    "content": generated_content
                })

            except Exception as e:
                st.error(f"Something went wrong: {e}")


# Show generated content
if "current_content" in st.session_state:

    st.divider()
    st.subheader("📝 Generated Content")

    st.text_area(
        "Your content",
        st.session_state.current_content,
        height=300
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🔄 Regenerate", use_container_width=True):

            prompt = f"""
            Create another NEW version of a {content_type}
            about: {topic}.

            Tone: {tone}
            Language: {language}
            Length: {length}

            Make it different from the previous version.
            """

            with st.spinner("🔄 Regenerating..."):

                response = client.responses.create(
                    model="gpt-5-mini",
                    input=prompt
                )

                st.session_state.current_content = response.output_text
                st.rerun()

    with col2:
        st.download_button(
            "⬇️ Download",
            st.session_state.current_content,
            file_name="generated_content.txt",
            mime="text/plain",
            use_container_width=True
        )


# History
if st.session_state.history:

    st.divider()
    st.header("📜 Content History")

    for i, item in enumerate(
        reversed(st.session_state.history)
    ):

        with st.expander(
            f"{item['type']} — {item['topic']}"
        ):

            st.write(f"**Tone:** {item['tone']}")
            st.write(item["content"])