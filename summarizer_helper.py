from collections import Counter
import re

def extract_keywords(messages):
    stop_words = {"a", "the", "i", "you", "and", "is", "it", "how", "hi", "are", "to", "on", "of", "can"}
    all_text = " ".join(msg['text'] for msg in messages)
    words = re.findall(r'\b\w+\b', all_text.lower())
    filtered_words = [word for word in words if word not in stop_words]
    common_words = Counter(filtered_words).most_common(3)  # Extract top 3 topics
    return [word for word, _ in common_words]


def preprocess_messages(messages):
    meaningful_messages = [
        f"{msg['author']}: {msg['text']}"
        for msg in messages
        if len(msg['text']) > 5  # Skip trivial messages
    ]
    return " ".join(meaningful_messages)


def group_dialogues(messages, window=5):
    dialogues = []
    seen_questions = set()  # Track questions to avoid duplicates
    for i, msg in enumerate(messages):
        if "?" in msg['text'] and msg['text'] not in seen_questions:  # Identify unique questions
            seen_questions.add(msg['text'])
            # Look for a response within a larger window
            response = None
            for j in range(i + 1, min(i + window, len(messages))):
                if messages[j]['author'] != msg['author']:
                    response = messages[j]
                    break
            if response:
                dialogues.append(f"{msg['author']} asked: '{msg['text']}'\n"
                                 f"{response['author']} replied: '{response['text']}'")
    return dialogues


def filter_messages(messages):
    filtered = []
    for msg in messages:
        if len(msg['text']) > 3 and not msg['text'].lower() in {"no", "stop", "yes", "hmm"}:
            filtered.append(msg)
    return filtered