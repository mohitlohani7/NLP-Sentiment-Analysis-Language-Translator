from langdetect import detect
from deep_translator import GoogleTranslator

def detect_language(text):
    return detect(text)

def translate_online(text, src, tgt):
    if src == tgt:
        return text
    return GoogleTranslator(source=src, target=tgt).translate(text)

def translate_offline(text, src, tgt):
    # Cloud-safe fallback
    # Streamlit Cloud pe offline models avoid karo
    return translate_online(text, src, tgt)

LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "zh": "Chinese",
    "ja": "Japanese",
    "ko": "Korean"
}
