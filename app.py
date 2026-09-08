import streamlit as st
import google.genai as genai
from google.genai import types
from dna_tools import calculate_gc_content, get_reverse_complement, translate_dna, find_mutations
# في بداية كود app.py
import streamlit as st

st.sidebar.title("Configuration")
user_api_key = st.sidebar.text_input("Enter your Gemini API Key (Optional):", type="password")

# استخدام مفتاح الزائر إذا أدخله، أو المفتاح الافتراضي للموقع
api_key = user_api_key if user_api_key else st.secrets["GEMINI_API_KEY"]

# ضبط إعدادات الصفحة
st.set_page_config(page_title="DNA Mutation AI Agent", page_icon="🧬", layout="wide")

st.title("🧬 DNA Mutation Detection AI Agent")
st.markdown("An intelligent bioinformatics toolkit powered by **Gemini** & **Biopython**.")

# شريط جانبي لإدخال مفتاح API اختيارياً أو استخدام الافتراضي
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Gemini API Key", type="password", help="Leave blank if set in environment variables.")

# تهيئة العميل
try:
    client = genai.Client(api_key=api_key) if api_key else genai.Client()
except Exception as e:
    st.error("Please provide a valid Gemini API Key in the sidebar or set GEMINI_API_KEY environment variable.")

SYSTEM_INSTRUCTION = """
You are an expert Bioinformatics and Genomics AI assistant.
Your goal is to analyze DNA sequences, compute metrics like GC content, 
detect sequence mutations, and explain the biological implications clearly.

Always rely on your provided python tools to perform accurate calculations 
and alignments rather than estimating or guessing results yourself.
"""

# إدخال البيانات من المستخدم
col1, col2 = st.columns(2)
with col1:
    ref_seq = st.text_area("Reference Sequence (DNA)", "ATGCGATCGTAA", height=100)
with col2:
    sample_seq = st.text_area("Sample / Mutated Sequence (DNA)", "ATGCAATCGTAA", height=100)

query = st.text_input("Ask a specific question (Optional):", f"Compare reference '{ref_seq}' and sample '{sample_seq}'. Find all mutations and explain their biological impact.")

if st.button("Run AI Analysis", type="primary"):
    if not ref_seq or not sample_seq:
        st.warning("Please provide both DNA sequences.")
    else:
        with st.spinner("Analyzing sequences and running alignment..."):
            try:
                chat = client.chats.create(
                    model="gemini-3.6-flash",
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.1,
                        tools=[calculate_gc_content, get_reverse_complement, translate_dna, find_mutations],
                    ),
                )
                response = chat.send_message(query)

                # عرض الأرقام السريعة كـ Metrics
                st.subheader("📊 Quick Sequence Metrics")
                m1, m2, m3 = st.columns(3)
                m1.metric("Ref GC Content", f"{calculate_gc_content(ref_seq)}%")
                m2.metric("Sample GC Content", f"{calculate_gc_content(sample_seq)}%")
                m3.metric("Ref Length", f"{len(ref_seq)} bp")

                # عرض التقرير الذكي
                st.subheader("📝 AI Biological Report")
                st.info(response.text)

            except Exception as e:
                st.error(f"Error executing analysis: {e}")