"""LLM client service for generating responses via an OpenAI-compatible API."""

import os

from openai import OpenAI, OpenAIError

_MAX_RESPONSE_CHARS = 2000
_TRUNCATION_NOTICE = "... [response truncated]"


def generate(prompt: str, language: str) -> str:
    """Generate an LLM response for *prompt*, instructing the model to reply in *language*.

    Args:
        prompt: The user's message text.
        language: BCP 47 language code (e.g. ``"fr"``, ``"es"``) that the LLM
                  should use when composing its reply.

    Returns:
        The assistant's response text, truncated to 2000 characters if needed.

    Raises:
        RuntimeError: If ``LLM_API_KEY`` is not set or the API call fails.
    """
    api_key = os.environ.get("LLM_API_KEY", "ollama")
    base_url = os.environ.get("LLM_BASE_URL", "http://host.docker.internal:11434/v1")

    if not api_key:
        raise RuntimeError(
            "LLM_API_KEY environment variable is not set. "
            "Cannot connect to the LLM API."
        )

    client = OpenAI(api_key=api_key, base_url=base_url)

    system_message = (
        f"You are a helpful assistant. "
        f"You MUST reply exclusively in the following language: {language}. "
        f"Do not switch to any other language under any circumstances."
    )

    try:
        completion = client.chat.completions.create(
            model=os.environ.get("LLM_MODEL", "gpt-3.5-turbo"),
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt},
            ],
        )
    except OpenAIError as exc:
        raise RuntimeError(
            f"LLM API request failed: {exc}"
        ) from exc

    response_text = completion.choices[0].message.content or ""

    if len(response_text) > _MAX_RESPONSE_CHARS:
        response_text = response_text[:_MAX_RESPONSE_CHARS] + _TRUNCATION_NOTICE

    return response_text
