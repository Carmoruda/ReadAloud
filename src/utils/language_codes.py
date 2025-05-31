ENGLISH = "en"
SPANISH = "es"
FRENCH = "fr"

LANGUAGE_ALIASES = {
    "en": ["English", "Inglés", "Anglais"],
    "es": ["Spanish", "Español", "Espagnol"],
    "fr": ["French", "Francés", "Français"],
}

LANGUAGE_MAP = {alias: code for code, aliases in LANGUAGE_ALIASES.items() for alias in aliases}
