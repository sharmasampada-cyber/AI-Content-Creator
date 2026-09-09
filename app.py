import streamlit as st
from google import genai
from dotenv import load_dotenv
import os
import time
import re


# =========================================================
# CONFIGURATION
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error("❌ GEMINI_API_KEY not found in .env file.")
    st.stop()

client = genai.Client(api_key=API_KEY)

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
]


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Content Creator Suite",
    page_icon="🤖",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.7;
        margin-bottom: 25px;
    }

    .output-card {
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-top: 10px;
    }

    .feature-card {
        padding: 18px;
        border-radius: 16px;
        border: 1px solid rgba(128,128,128,0.2);
        text-align: center;
        min-height: 145px;
    }

    .feature-icon {
        font-size: 30px;
    }

    .feature-title {
        font-size: 17px;
        font-weight: 700;
        margin-top: 8px;
    }

    .feature-description {
        font-size: 13px;
        opacity: 0.7;
        margin-top: 5px;
    }

    .footer {
        text-align: center;
        opacity: 0.6;
        padding: 25px;
        font-size: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "current_content" not in st.session_state:
    st.session_state.current_content = ""

if "idea_results" not in st.session_state:
    st.session_state.idea_results = ""

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = ""


# =========================================================
# GEMINI FUNCTION
# =========================================================

def generate_content(prompt):

    last_error = None

    for model in MODELS:

        for attempt in range(2):

            try:

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                if response.text:
                    return response.text

            except Exception as e:

                last_error = e
                error_text = str(e)

                if "503" in error_text or "UNAVAILABLE" in error_text:

                    if attempt == 0:
                        time.sleep(3)
                        continue

                break

    raise Exception(
        f"Gemini API is currently unavailable.\n\n{last_error}"
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("⚙️ Content Settings")
    st.caption("Customize your AI-generated content")

    st.markdown("---")

    content_type = st.selectbox(
        "📱 Content Type",
        [
            "Instagram Caption",
            "Blog Post",
            "YouTube Description",
            "Tweet",
            "LinkedIn Post"
        ]
    )

    tone = st.selectbox(
        "🎭 Tone",
        [
            "Professional",
            "Casual",
            "Funny",
            "Creative",
            "Inspirational",
            "Formal",
            "Friendly",
            "Gen-Z",
            "Persuasive"
        ]
    )

    language = st.selectbox(
        "🌐 Language",
        [
            "English",
            "Hindi",
            "Hinglish"
        ]
    )

    length = st.selectbox(
        "📏 Content Length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

    include_hashtags = st.checkbox(
        "🏷️ Generate Hashtags"
    )

    st.markdown("---")

    st.subheader("📊 Project Info")

    st.write(
        "AI Content Creator Suite uses Gemini AI "
        "to generate, analyze and improve content "
        "for different digital platforms."
    )

    st.markdown("---")

    if st.button(
        "🗑️ Clear History",
        use_container_width=True
    ):

        st.session_state.history = []
        st.session_state.current_content = ""
        st.session_state.idea_results = ""
        st.session_state.analysis_results = ""

        st.success("History cleared!")
        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">🤖 AI Content Creator Suite</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Create, improve, analyze and transform your content with AI ✨'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# METRICS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "📝 Content Created",
        len(st.session_state.history)
    )

with col2:
    st.metric(
        "🎯 Content Type",
        content_type
    )

with col3:
    st.metric(
        "🌐 Language",
        language
    )


st.markdown("<br>", unsafe_allow_html=True)


# =========================================================
# FEATURES
# =========================================================

st.subheader("✨ What can you do?")

feature1, feature2, feature3, feature4 = st.columns(4)

with feature1:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">✍️</div>
            <div class="feature-title">Create Content</div>
            <div class="feature-description">
                Generate AI-powered content.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature2:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Get Ideas</div>
            <div class="feature-description">
                Generate creative content ideas.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature3:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Analyze Quality</div>
            <div class="feature-description">
                Evaluate your content quality.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with feature4:
    st.markdown(
        """
        <div class="feature-card">
            <div class="feature-icon">🛠️</div>
            <div class="feature-title">Improve Content</div>
            <div class="feature-description">
                Rewrite and transform content.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<br>", unsafe_allow_html=True)
st.divider()


# =========================================================
# CONTENT IDEAS GENERATOR
# =========================================================

st.header("💡 Content Ideas Generator")

st.write(
    "Generate creative and practical content ideas."
)

idea_topic = st.text_input(
    "🔎 Enter a topic for ideas",
    placeholder="Example: AI, college life, fitness, travel..."
)

idea_col1, idea_col2 = st.columns(2)

with idea_col1:

    idea_count = st.selectbox(
        "🔢 Number of ideas",
        [5, 10],
        key="idea_count"
    )

with idea_col2:

    idea_platform = st.selectbox(
        "📱 Platform",
        [
            "Instagram",
            "YouTube",
            "Blog",
            "Twitter/X",
            "LinkedIn"
        ],
        key="idea_platform"
    )


if st.button(
    "💡 Generate Ideas",
    use_container_width=True
):

    if not idea_topic.strip():

        st.warning("⚠️ Please enter a topic first.")

    else:

        idea_prompt = f"""
Generate {idea_count} creative content ideas for
{idea_platform}.

Topic: {idea_topic}

Language: {language}
Tone: {tone}

For each idea provide:

1. Title
2. Description
3. Content Angle

Make every idea different.

Return only the numbered ideas.
"""

        with st.spinner("💡 Generating ideas..."):

            try:

                ideas = generate_content(idea_prompt)

                st.session_state.idea_results = ideas

                st.success("✅ Content ideas generated!")

            except Exception as e:

                st.error(f"❌ Something went wrong:\n\n{e}")


if st.session_state.idea_results:

    st.subheader("✨ Your Content Ideas")

    st.text_area(
        "AI-generated ideas",
        st.session_state.idea_results,
        height=350,
        key="ideas_display"
    )

    st.download_button(
        "⬇️ Download Ideas",
        st.session_state.idea_results,
        file_name="content_ideas.txt",
        mime="text/plain",
        use_container_width=True
    )


st.divider()


# =========================================================
# CREATE CONTENT
# =========================================================

st.header("✨ Create Your Content")

topic = st.text_area(
    "💡 Enter your topic",
    placeholder=(
        "Example: College trip with friends, "
        "Artificial Intelligence, Friendship..."
    ),
    height=100
)


if st.button(
    "🚀 Generate Content",
    use_container_width=True
):

    if not topic.strip():

        st.warning("⚠️ Please enter a topic first.")

    else:

        prompt = f"""
Create a {content_type} about:

{topic}

Tone: {tone}
Language: {language}
Length: {length}

Make it engaging, natural, creative and suitable
for the selected platform.

Return only the final content.
"""

        if include_hashtags:

            prompt += """
Also add 5-10 relevant hashtags at the end.
"""

        with st.spinner("✨ Creating your content..."):

            try:

                generated_content = generate_content(prompt)

                st.session_state.current_content = generated_content
                st.session_state.analysis_results = ""

                st.session_state.history.append(
                    {
                        "type": content_type,
                        "topic": topic,
                        "tone": tone,
                        "content": generated_content
                    }
                )

                st.success("✅ Content generated successfully!")

            except Exception as e:

                st.error(f"❌ Something went wrong:\n\n{e}")


# =========================================================
# GENERATED CONTENT
# =========================================================

if st.session_state.current_content:

    st.divider()

    st.header("📝 Generated Content")

    st.text_area(
        "Your AI-generated content",
        st.session_state.current_content,
        height=300,
        key="generated_content_display"
    )

    st.download_button(
        "⬇️ Download Content",
        st.session_state.current_content,
        file_name="generated_content.txt",
        mime="text/plain",
        use_container_width=True
    )


    # =====================================================
    # ANALYZER
    # =====================================================

    st.markdown("---")

    st.subheader("📊 Content Quality Analyzer")

    st.write(
        "Evaluate your content using AI and receive "
        "scores and improvement suggestions."
    )

    analyze_clicked = st.button(
        "🔍 Analyze Content",
        use_container_width=True,
        key="analyze_content_button"
    )


    if analyze_clicked:

        analysis_prompt = f"""
Analyze the following {content_type}.

CONTENT:
{st.session_state.current_content}

Give scores out of 10 for:

OVERALL SCORE
CREATIVITY
ENGAGEMENT
GRAMMAR & CLARITY
PLATFORM SUITABILITY

Then provide:

STRENGTHS:
- Two strengths

IMPROVEMENT SUGGESTIONS:
- Three specific suggestions

FINAL RECOMMENDATION:
Tell whether the content is ready to publish.

Use EXACTLY this format:

OVERALL SCORE: X/10
CREATIVITY: X/10
ENGAGEMENT: X/10
GRAMMAR & CLARITY: X/10
PLATFORM SUITABILITY: X/10

STRENGTHS:
- ...
- ...

IMPROVEMENT SUGGESTIONS:
- ...
- ...
- ...

FINAL RECOMMENDATION:
...

Keep the analysis concise.
"""

        with st.spinner("🔍 Analyzing your content..."):

            try:

                analysis = generate_content(analysis_prompt)

                st.session_state.analysis_results = analysis

                st.success("✅ Content analysis completed!")

                st.rerun()

            except Exception as e:

                st.error(
                    f"❌ Analysis failed:\n\n{e}"
                )


    # =====================================================
    # ANALYSIS REPORT
    # =====================================================

    if st.session_state.analysis_results:

        analysis_text = st.session_state.analysis_results

        st.markdown("---")

        st.subheader("📈 AI Analysis Report")


        def get_score(label):

            pattern = rf"{re.escape(label)}\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10"

            match = re.search(
                pattern,
                analysis_text,
                re.IGNORECASE
            )

            if match:
                return float(match.group(1))

            return None


        overall = get_score("OVERALL SCORE")
        creativity = get_score("CREATIVITY")
        engagement = get_score("ENGAGEMENT")
        grammar = get_score("GRAMMAR & CLARITY")
        platform = get_score("PLATFORM SUITABILITY")


        # Overall

        if overall is not None:

            st.markdown("### ⭐ Overall Quality")

            score_col1, score_col2 = st.columns([1, 3])

            with score_col1:

                st.metric(
                    "AI Quality Score",
                    f"{overall}/10"
                )

            with score_col2:

                st.progress(
                    min(max(int(overall * 10), 0), 100)
                )

                if overall >= 8:

                    st.success(
                        "🌟 Excellent content quality!"
                    )

                elif overall >= 6:

                    st.info(
                        "👍 Good content with room for improvement."
                    )

                else:

                    st.warning(
                        "⚠️ Content needs improvement."
                    )


        # Detailed scores

        st.markdown("### 📊 Detailed Scores")

        score1, score2 = st.columns(2)

        with score1:

            if creativity is not None:

                st.metric(
                    "🎨 Creativity",
                    f"{creativity}/10"
                )

                st.progress(
                    min(max(int(creativity * 10), 0), 100)
                )

            if grammar is not None:

                st.metric(
                    "✍️ Grammar & Clarity",
                    f"{grammar}/10"
                )

                st.progress(
                    min(max(int(grammar * 10), 0), 100)
                )


        with score2:

            if engagement is not None:

                st.metric(
                    "🔥 Engagement",
                    f"{engagement}/10"
                )

                st.progress(
                    min(max(int(engagement * 10), 0), 100)
                )

            if platform is not None:

                st.metric(
                    "📱 Platform Suitability",
                    f"{platform}/10"
                )

                st.progress(
                    min(max(int(platform * 10), 0), 100)
                )


        st.markdown("---")

        st.markdown("### 🤖 AI Feedback")

        st.text_area(
            "Detailed Analysis",
            analysis_text,
            height=400,
            key="analysis_display"
        )

        st.download_button(
            "⬇️ Download Analysis",
            analysis_text,
            file_name="content_quality_analysis.txt",
            mime="text/plain",
            use_container_width=True
        )


    # =====================================================
    # AI CONTENT TOOLS
    # =====================================================

    st.markdown("---")

    st.subheader("🛠️ AI Content Tools")


    tool_col1, tool_col2 = st.columns(2)


    # Improve

    with tool_col1:

        if st.button(
            "✨ Improve Content",
            use_container_width=True
        ):

            prompt = f"""
Improve this content.

Make it:
- More engaging
- More natural
- Better structured
- Grammatically correct

Keep the original meaning.

Content:
{st.session_state.current_content}

Return only the improved content.
"""

            with st.spinner("✨ Improving..."):

                try:

                    result = generate_content(prompt)

                    st.session_state.current_content = result
                    st.session_state.analysis_results = ""

                    st.session_state.history.append(
                        {
                            "type": f"{content_type} - Improved",
                            "topic": topic,
                            "tone": tone,
                            "content": result
                        }
                    )

                    st.success("✅ Content improved!")
                    st.rerun()

                except Exception as e:

                    st.error(f"❌ Error:\n\n{e}")


    # Rewrite

    with tool_col2:

        if st.button(
            "🔄 Rewrite",
            use_container_width=True
        ):

            prompt = f"""
Rewrite this content completely.

Keep the same main idea but create a fresh,
different and engaging version.

Tone: {tone}
Language: {language}

Content:
{st.session_state.current_content}

Return only the rewritten content.
"""

            with st.spinner("🔄 Rewriting..."):

                try:

                    result = generate_content(prompt)

                    st.session_state.current_content = result
                    st.session_state.analysis_results = ""

                    st.session_state.history.append(
                        {
                            "type": f"{content_type} - Rewritten",
                            "topic": topic,
                            "tone": tone,
                            "content": result
                        }
                    )

                    st.success("✅ Content rewritten!")
                    st.rerun()

                except Exception as e:

                    st.error(f"❌ Error:\n\n{e}")


    tool_col3, tool_col4 = st.columns(2)


    # Change Tone

    with tool_col3:

        new_tone = st.selectbox(
            "🎭 Select new tone",
            [
                "Professional",
                "Casual",
                "Funny",
                "Creative",
                "Inspirational",
                "Formal",
                "Friendly",
                "Gen-Z",
                "Persuasive"
            ],
            key="change_tone"
        )

        if st.button(
            "🎭 Change Tone",
            use_container_width=True
        ):

            prompt = f"""
Rewrite the content using a {new_tone} tone.

Keep the same meaning.

Language: {language}

Content:
{st.session_state.current_content}

Return only the final content.
"""

            with st.spinner("🎭 Changing tone..."):

                try:

                    result = generate_content(prompt)

                    st.session_state.current_content = result
                    st.session_state.analysis_results = ""

                    st.session_state.history.append(
                        {
                            "type": f"{content_type} - {new_tone} Tone",
                            "topic": topic,
                            "tone": new_tone,
                            "content": result
                        }
                    )

                    st.success(
                        f"✅ Tone changed to {new_tone}!"
                    )

                    st.rerun()

                except Exception as e:

                    st.error(f"❌ Error:\n\n{e}")


    # Shorten

    with tool_col4:

        if st.button(
            "✂️ Shorten Content",
            use_container_width=True
        ):

            prompt = f"""
Shorten the following content.

Keep:
- Main idea
- Important information
- Original meaning

Remove unnecessary words and repetition.

Content:
{st.session_state.current_content}

Return only the shortened content.
"""

            with st.spinner("✂️ Shortening..."):

                try:

                    result = generate_content(prompt)

                    st.session_state.current_content = result
                    st.session_state.analysis_results = ""

                    st.session_state.history.append(
                        {
                            "type": f"{content_type} - Shortened",
                            "topic": topic,
                            "tone": tone,
                            "content": result
                        }
                    )

                    st.success("✅ Content shortened!")
                    st.rerun()

                except Exception as e:

                    st.error(f"❌ Error:\n\n{e}")


    # Regenerate

    st.markdown("---")

    if st.button(
        "🔄 Regenerate",
        use_container_width=True
    ):

        prompt = f"""
Create another NEW and DIFFERENT version of a
{content_type} about:

{topic}

Tone: {tone}
Language: {language}
Length: {length}

Make it clearly different from the previous version.

Return only the final content.
"""

        if include_hashtags:

            prompt += "\nAdd 5-10 relevant hashtags."

        with st.spinner("🔄 Creating a new version..."):

            try:

                result = generate_content(prompt)

                st.session_state.current_content = result
                st.session_state.analysis_results = ""

                st.session_state.history.append(
                    {
                        "type": content_type,
                        "topic": topic,
                        "tone": tone,
                        "content": result
                    }
                )

                st.success("✅ New version generated!")
                st.rerun()

            except Exception as e:

                st.error(f"❌ Error:\n\n{e}")


# =========================================================
# HISTORY
# =========================================================

if st.session_state.history:

    st.divider()

    st.header("📜 Content History")

    for item in reversed(st.session_state.history):

        with st.expander(
            f"✨ {item['type']} — {item['topic']}"
        ):

            st.write(
                f"**🎭 Tone:** {item['tone']}"
            )

            st.markdown("---")

            st.write(
                item["content"]
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🤖 <b>AI Content Creator Suite</b><br>
        Powered by Gemini AI • Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True
)