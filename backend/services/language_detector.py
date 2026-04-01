"""Language detection service wrapping langdetect."""

from langdetect import detect as _detect, LangDetectException

# Minimum probability threshold for a confident detection.
# langdetect doesn't expose per-call probability easily, so we rely on
# exception handling and a known-good language list as a secondary guard.
_SUPPORTED_LANGUAGES = {
    "en", "fr", "es", "de", "ar", "zh-cn", "ja", "pt", "it", "hi"
}

_FALLBACK = "en"


def detect(text: str) -> str:
    """Detect the BCP 47 language code of *text*.

    Returns a BCP 47 language code string (e.g. ``"en"``, ``"fr"``).
    Falls back to ``"en"`` when:
    - *text* is empty or whitespace-only
    - ``langdetect`` raises :class:`LangDetectException`
    - The detected code is not in the supported language set
    """
    if not text or not text.strip():
        return _FALLBACK

    try:
        code = _detect(text.strip())
        # langdetect returns "zh-cn" / "zh-tw"; both are valid BCP 47 variants.
        # Accept any result — the supported-language check below acts as a
        # confidence proxy: if the library returns something exotic for a very
        # short or ambiguous input, we fall back to English.
        if code not in _SUPPORTED_LANGUAGES:
            return _FALLBACK
        return code
    except LangDetectException:
        return _FALLBACK
