from transformers import pipeline

from src.utils.config import cfg


def summarize_conversation(conversation):
    summarizer = pipeline("summarization", model=cfg["huggingface"]["summarizer_model"])  # Initialize summarizer

    # Get the last 3 messages
    last_messages = conversation[-3:]
    # Join them into a single string
    text_to_summarize = "\n".join([msg["content"] for msg in last_messages])
    # Summarize the text using transformers pipeline
    summary = summarizer(text_to_summarize, max_length=100, min_length=30)
    return summary[0]["summary_text"].strip()  # Extract and return the summary text
