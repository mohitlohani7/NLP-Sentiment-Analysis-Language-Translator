from langdetect import detect
from deep_translator import GoogleTranslator
import argostranslate.translate

LANGUAGE_MAP = {
    "en": "English",
    "hi": "Hindi",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "ta": "Tamil",
    "te": "Telugu",
    "bn": "Bengali",
    "mr": "Marathi"
}

def detect_language(text):
    return detect(text)

def translate_online(text, src, tgt):
    if src == tgt:
        return text
    try:
        return GoogleTranslator(source=src, target=tgt).translate(text)
    except Exception:
        return text

def translate_offline(text, src, tgt):
    if src == tgt:
        return text

    installed_languages = argostranslate.translate.get_installed_languages()
    from_lang = next((l for l in installed_languages if l.code == src), None)
    to_lang = next((l for l in installed_languages if l.code == tgt), None)

    if not from_lang or not to_lang:
        return text

    translation = from_lang.get_translation(to_lang)
    return translation.translate(text)
