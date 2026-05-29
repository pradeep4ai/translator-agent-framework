from __future__ import annotations

from framework.agent import BaseAgent
from framework.context import Context
from framework.llm import LLMProvider


LANG_NAMES = {
    "hi": "Hindi", "te": "Telugu", "mr": "Marathi", "gu": "Gujarati",
    "bho": "Bhojpuri", "kn": "Kannada", "ne": "Nepali",
    "en": "English", "de": "German", "fr": "French",
}


SYSTEM_PROMPT = (
    "You are a precise multilingual translator. Translate the user's text from "
    "{source_name} into {target_name}. "
    "Rules: (1) Preserve meaning, tone, and named entities. "
    "(2) Do NOT transliterate when a true translation exists. "
    "(3) Output ONLY the translated text - no prefixes, quotes, explanations, or notes. "
    "(4) If the input is a single word, output a single word."
)


class TranslatorAgent(BaseAgent):
    name = "translator"

    def __init__(self, providers: dict[str, LLMProvider]) -> None:
        self.providers = providers

    def run(self, ctx: Context) -> Context:
        if not ctx.chosen_provider or not ctx.chosen_model:
            ctx.fail("translator: router did not set provider/model")
            return ctx

        provider = self.providers.get(ctx.chosen_provider)
        if provider is None:
            ctx.fail(f"translator: provider not available: {ctx.chosen_provider}")
            return ctx

        source_name = LANG_NAMES.get(ctx.source_lang, ctx.source_lang)
        target_name = LANG_NAMES.get(ctx.target_lang, ctx.target_lang)

        system = SYSTEM_PROMPT.format(source_name=source_name, target_name=target_name)

        if ctx.chosen_provider == "indictrans2":
            # IndicTrans2 expects raw text; system prompt is ignored.
            response = provider.complete(ctx.input_text, model=ctx.chosen_model)
        else:
            response = provider.complete(
                ctx.input_text,
                system=system,
                model=ctx.chosen_model,
                temperature=0.2,
                max_tokens=1024,
            )

        ctx.output_text = response.text
        ctx.attempts += 1
        return ctx
