import summarizer_helper
from transformers import pipeline

class Summarizer:
    def __init__(self, model_name="facebook/bart-large-cnn"):

        self.summarizer = pipeline("summarization", model=model_name)

    def generate_summary(self, messages):
        keywords = summarizer_helper.extract_keywords(messages)
        preprocessed_text = summarizer_helper.preprocess_messages(messages)

        summary = self.summarizer(preprocessed_text, max_length=150, min_length=50, do_sample=False)[0]['summary_text']

        return (
            f"💬 Summary of the chat:\n\n"
            f"In short, the group discussed {', '.join(keywords)}. "
            f"{summary.capitalize()} The conversation was friendly and engaging, "
            f"with participants sharing tips and ideas.\n\n"
            f"🕐 Total messages: {len(messages)}\n"
            f"👥 Participants: {', '.join(set(msg['author'] for msg in messages))}"
        )




