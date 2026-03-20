"""LLM-based feature extraction from script chunks."""

import json

from backend.models.schemas import ScriptFeatures

EXTRACTION_PROMPT = """Analyze this TV script excerpt and extract the following features.
Return valid JSON matching this schema exactly.

Features to extract:
- themes: list of major themes (e.g. "power", "family dysfunction", "class")
- tone: list of tonal qualities (e.g. "dark", "satirical", "warm")
- humor_type: list of humor styles if any (e.g. "dry wit", "absurdist", "physical")
- dialogue_style: list of dialogue characteristics (e.g. "rapid-fire", "poetic", "naturalistic")
- emotional_register: list of emotional qualities (e.g. "restrained", "vulnerable", "manic")
- pacing: single word or short phrase (e.g. "fast", "slow-burn")
- genre_blend: list of genres (e.g. "drama", "comedy")
- narrative_structure: single descriptor (e.g. "serialized", "episodic")
- vocabulary_complexity: one of "simple", "moderate", "dense"
- style_summary: one sentence describing the overall writing style

Script excerpt:
---
{script_text}
---

Return ONLY valid JSON, no markdown formatting."""


def parse_features_response(response_text: str, show_title: str) -> ScriptFeatures:
    """Parse LLM response into ScriptFeatures."""
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        # Try extracting JSON from markdown code blocks
        if "```" in response_text:
            json_str = response_text.split("```")[1]
            if json_str.startswith("json"):
                json_str = json_str[4:]
            data = json.loads(json_str.strip())
        else:
            raise

    return ScriptFeatures(show_title=show_title, **data)
