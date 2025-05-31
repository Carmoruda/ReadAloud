import json
import os

from utils.language_codes import LANGUAGE_MAP


class Translator:
    """
    A simple translator class to handle translations for different languages.
    It loads translations from a JSON file and provides methods to set the language
    and retrieve translated strings based on a key.

    Attributes:
        lang (str): The current language set for translations.
        translations (dict): A dictionary containing translations for different keys and languages.
    """

    def __init__(self, default_lang="en"):
        """Initializes the Translator with a default language and loads translations.

        Args:
            default_lang (str, optional): The default language to use for translations. Defaults to "en".
        """
        self.lang = default_lang
        self.translations = {}
        self.load_translations()

    def get_language_code(self, language_name: str) -> str:
        """Returns the language code for a given language name.

        Args:
            language_name (str): The name of the language.

        Returns:
            str | None: The corresponding language code, or None if not found.
        """
        return LANGUAGE_MAP.get(language_name, "en")

    def load_translations(self) -> None:
        """Loads translations from a JSON file located in the data directory."""

        path = os.path.join("data", "translations.json")

        with open(path, "r", encoding="utf-8") as f:
            self.translations = json.load(f)

    def set_language(self, lang: str) -> None:
        """Sets the current language for translations.

        Args:
            lang (str): The language code to set for translations (e.g., "en", "es", "fr").
        """
        self.lang = lang.lower()

    def t(self, key: str) -> str:
        """Retrieves the translated string for a given key in the current language.
        If the key does not exist in the translations for the current language,
        it returns the key wrapped in square brackets as a fallback.

        Args:
            key (str): The key for which to retrieve the translation.

        Returns:
            str: The translated string in the current language, or the key wrapped in brackets if not found.
        """
        return self.translations.get(key, {}).get(self.lang, f"[{key}]")


translator = Translator()
