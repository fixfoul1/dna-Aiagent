import os
import google.genai as genai
from google.genai import types

# Import the toolkit functions directly from dna_tools.py
from dna_tools import (
    calculate_gc_content,
    get_reverse_complement,
    translate_dna,
    find_mutations,
)

# 1. Initialize the Gemini client
client = genai.Client()

# 2. Set system instructions
SYSTEM_INSTRUCTION = """
You are an expert Bioinformatics and Genomics AI assistant.
Your goal is to analyze DNA sequences, compute metrics like GC content, 
detect sequence mutations, and explain the biological implications clearly.

Always rely on your provided python tools to perform accurate calculations 
and alignments rather than estimating or guessing results yourself.
"""

def ask_agent(prompt: str) -> None:
    """Sends a user prompt to Gemini using the Chat API for Automatic Function Calling."""
    print(f"\nUser Query: {prompt}")
    print("-" * 60)

    try:
        # Create a chat session with AFC enabled
        chat = client.chats.create(
            model="gemini-2.5-flash",  # Updated supported model
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.1,
                tools=[
                    calculate_gc_content,
                    get_reverse_complement,
                    translate_dna,
                    find_mutations,
                ],
            ),
        )

        # Send the user query to the chat session
        response = chat.send_message(prompt)

        print("Agent Explanation:\n")
        print(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    test_query = (
        "I have a reference sequence 'ATGCGATCGTAA' and a sample sequence 'ATGCAATCGTAA'. "
        "Please analyze both: tell me their GC content, reverse complement of the reference, "
        "and explain any mutations found between them."
    )

    ask_agent(test_query)