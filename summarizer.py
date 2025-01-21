from transformers import pipeline

# Initialize the HuggingFace summarizer
summarizer = pipeline("summarization", model="t5-small")


def summarize_messages(messages):
    """Summarize a list of messages."""
    combined_text = " ".join(messages)  # Combine all messages into one string

    # HuggingFace summarizer requires limits on input length (the model can't handle very long texts)
    # We will split the text into chunks if necessary, but for now, we'll keep it simple.
    summary = summarizer(combined_text, max_length=150, min_length=50, do_sample=False)

    return summary[0]['summary_text']
