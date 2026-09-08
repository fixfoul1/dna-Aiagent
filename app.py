import streamlit as st
from agent import client, SYSTEM_INSTRUCTION
from dna_tools import calculate_gc_content, get_reverse_complement, translate_dna, find_mutations
from google.genai import types

st.title("🧬 DNA Mutation Analysis Agent")

user_query = st.text_area("أدخل سؤالك أو السلسلتين للمقارنة:")

if st.button("تحليل"):
    chat = client.chats.create(
        model="gemini-3.6-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_INSTRUCTION,
            temperature=0.1,
            tools=[calculate_gc_content, get_reverse_complement, translate_dna, find_mutations],
        ),
    )
    response = chat.send_message(user_query)
    st.write(response.text)