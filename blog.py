import streamlit as st
from constants import groq_key
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------- LLM SETUP --------
llm = ChatGroq(api_key=groq_key, model_name="llama3-8b-8192")

# -------- PAGE CONFIG --------
st.set_page_config(page_title="OpenBook Blog Forge", layout="centered")

# -------- CSS FOR OPENBOOK AESTHETIC --------
st.markdown("""
    <style>
        html, body {
            background-color: #0f1117;
            color: #dcdcdc;
            font-family: 'Segoe UI', sans-serif;
        }
        .stButton button {
            background-color: #4c8bf5;
            color: white;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-weight: bold;
        }
        .stSlider > div {
            color: white !important;
        }
        .small-font {
            font-size: 13px;
            color: #888;
        }
    </style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.title("📝 OpenBook Blog Forge")
st.caption("Crafted for thinkers, leaders, and curious minds.")
st.markdown("<div class='small-font'>“Words shape narratives. Let’s write yours.”</div>", unsafe_allow_html=True)

# -------- INPUTS --------
topic = st.text_input("🔍 Enter Blog Topic", placeholder="e.g. Future of AI in India")

col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.slider("🧮 Word Limit", 100, 1000, 300, step=100)

with col2:
    blog_style = st.selectbox('🧠 Audience:', 
                              ('Researchers', 'Data Scientist', 'Common people'))

tone = st.selectbox("🎙️ Tone", ['Professional', 'Conversational', 'Persuasive'])
format_type = st.radio("📄 Output Format", ['Paragraph', 'Bullet Points'], horizontal=True)

# -------- PROMPT TEMPLATE --------
blog_template = (
    "Write a {tone} tone blog for a {blog_style} on the topic '{topic}' "
    "in {format_type} format, strictly within {no_words} words."
)

prompt = PromptTemplate(
    input_variables=["topic", "no_words", "blog_style", "tone", "format_type"],
    template=blog_template
)

chain = LLMChain(llm=llm, prompt=prompt)

# -------- GENERATE BLOG --------
if st.button("🚀 Generate Blog"):
    if not topic:
        st.warning("Please enter a topic to proceed.")
    else:
        with st.spinner("Cooking up brilliance..."):
            response = chain.run({
                "topic": topic,
                "no_words": no_words,
                "blog_style": blog_style,
                "tone": tone,
                "format_type": format_type
            })
        st.success("✨ Blog Ready!")
        st.subheader("📄 Generated Blog")
        st.write(response)

        # -------- DOWNLOAD OPTION --------
        st.download_button(
            label="📥 Download as .txt",
            data=response,
            file_name=f"{topic.replace(' ', '_')}.txt",
            mime="text/plain"
        )

