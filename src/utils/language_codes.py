ENGLISH = "en"
SPANISH = "es"
FRENCH = "fr"

LANGUAGE_ALIASES = {
    "en": ["English", "Inglés", "Anglais"],
    "es": ["Spanish", "Español", "Espagnol"],
    "fr": ["French", "Francés", "Français"],
}

LANGUAGE_MAP = {
    alias: code for code, aliases in LANGUAGE_ALIASES.items() for alias in aliases
}

# --- TTS ---
TOP_LEVEL_DOMAIN_ALIASES = {
    "com.au": ["English (Australia)", "Inglés (Australia)", "Anglais (Australie)"],
    "co.uk": [
        "English (United Kingdom)",
        "Inglés (Reino Unido)",
        "Anglais (Royaume-Uni)",
    ],
    "us": [
        "English (United States)",
        "Inglés (Estados Unidos)",
        "Anglais (États-Unis)",
        "Spanish (United States)",
        "Español (Estados Unidos)",
        "Espagnol (États-Unis)",
    ],
    "ca": [
        "English (Canada)",
        "Inglés (Canadá)",
        "Anglais (Canada)",
        "French (Canada)",
        "Francés (Canadá)",
        "Français (Canada)",
    ],
    "co.in": ["English (India)", "Inglés (India)", "Anglais (Inde)"],
    "ie": ["English (Ireland)", "Inglés (Irlanda)", "Anglais (Irlande)"],
    "co.za": [
        "English (South Africa)",
        "Inglés (Sudáfrica)",
        "Anglais (Afrique du Sud)",
    ],
    "com.ng": ["English (Nigeria)", "Inglés (Nigeria)", "Anglais (Nigéria)"],
    "fr": ["French (France)", "Francés (Francia)", "Français (France)"],
    "zh-CN": [
        "Madarin (China Mainland)",
        "Mandarín (China Continental)",
        "Mandarin (Chine continentale)",
    ],
    "zh-TW": ["Madarin (Taiwan)", "Mandarín (Taiwán)", "Mandarin (Taïwan)"],
    "com.br": ["Portuguese (Brazil)", "Portugués (Brasil)", "Portugais (Brésil)"],
    "pt": ["Portuguese (Portugal)", "Portugués (Portugal)", "Portugais (Portugal)"],
    "com.mx": ["Spanish (Mexico)", "Español (México)", "Espagnol (Mexique)"],
    "es": ["Spanish (Spain)", "Español (España)", "Espagnol (Espagne)"],
}

TOP_LEVEL_DOMAIN_ALIASES_MAP = {
    alias: code
    for code, aliases in TOP_LEVEL_DOMAIN_ALIASES.items()
    for alias in aliases
}

# --- Edge TTS ---
TOP_LEVEL_DOMAIN_ALIASES_MALE_EDGE = {
    "en-AU-WilliamMultilingualNeural": [
        "English (Australia)",
        "Inglés (Australia)",
        "Anglais (Australie)",
    ],
    "en-GB-RyanNeural": [
        "English (United Kingdom)",
        "Inglés (Reino Unido)",
        "Anglais (Royaume-Uni)",
    ],
    "en-US-AndrewNeural": [
        "English (United States)",
        "Inglés (Estados Unidos)",
        "Anglais (États-Unis)",
        "Spanish (United States)",
        "Español (Estados Unidos)",
        "Espagnol (États-Unis)",
    ],
    "en-CA-LiamNeural": [
        "English (Canada)",
        "Inglés (Canadá)",
        "Anglais (Canada)",
        "French (Canada)",
        "Francés (Canadá)",
        "Français (Canada)",
    ],
    "en-IN-PrabhatNeural": ["English (India)", "Inglés (India)", "Anglais (Inde)"],
    "en-IE-ConnorNeural": [
        "English (Ireland)",
        "Inglés (Irlanda)",
        "Anglais (Irlande)",
    ],
    "en-ZA-LukeNeural": [
        "English (South Africa)",
        "Inglés (Sudáfrica)",
        "Anglais (Afrique du Sud)",
    ],
    "en-NG-AbeoNeural": ["English (Nigeria)", "Inglés (Nigeria)", "Anglais (Nigéria)"],
    "fr-FR-HenriNeural": ["French (France)", "Francés (Francia)", "Français (France)"],
    "zh-CN-YunyangNeural": [
        "Madarin (China Mainland)",
        "Mandarín (China Continental)",
        "Mandarin (Chine continentale)",
    ],
    "zh-TW-YunJheNeural": [
        "Madarin (Taiwan)",
        "Mandarín (Taiwán)",
        "Mandarin (Taïwan)",
    ],
    "pt-BR-AntonioNeural": [
        "Portuguese (Brazil)",
        "Portugués (Brasil)",
        "Portugais (Brésil)",
    ],
    "pt-PT-DuarteNeural": [
        "Portuguese (Portugal)",
        "Portugués (Portugal)",
        "Portugais (Portugal)",
    ],
    "es-MX-JorgeNeural": ["Spanish (Mexico)", "Español (México)", "Espagnol (Mexique)"],
    "es-ES-AlvaroNeural": ["Spanish (Spain)", "Español (España)", "Espagnol (Espagne)"],
}

TOP_LEVEL_DOMAIN_ALIASES_MAP_MALE_EDGE = {
    alias: code
    for code, aliases in TOP_LEVEL_DOMAIN_ALIASES_MALE_EDGE.items()
    for alias in aliases
}


LANGUAGE_CODES_ALIASES = {
    "en": [
        "English (Australia)",
        "Inglés (Australia)",
        "Anglais (Australie)",
        "English (United Kingdom)",
        "Inglés (Reino Unido)",
        "Anglais (Royaume-Uni)",
        "English (United States)",
        "Inglés (Estados Unidos)",
        "Anglais (États-Unis)",
        "English (Canada)",
        "Inglés (Canadá)",
        "Anglais (Canada)",
        "English (India)",
        "Inglés (India)",
        "Anglais (Inde)",
        "English (Ireland)",
        "Inglés (Irlanda)",
        "Anglais (Irlande)",
        "English (South Africa)",
        "Inglés (Sudáfrica)",
        "Anglais (Afrique du Sud)",
        "English (Nigeria)",
        "Inglés (Nigeria)",
        "Anglais (Nigéria)",
    ],
    "fr": [
        "French (Canada)",
        "Francés (Canadá)",
        "Français (Canada)",
        "French (France)",
        "Francés (Francia)",
        "Français (France)",
    ],
    "zh-CN": [
        "Madarin (China Mainland)",
        "Mandarín (China Continental)",
        "Mandarin (Chine continentale)",
    ],
    "zh-TW": ["Madarin (Taiwan)", "Mandarín (Taiwán)", "Mandarin (Taïwan)"],
    "pt": [
        "Portuguese (Brazil)",
        "Portugués (Brasil)",
        "Portugais (Brésil)",
        "Portuguese (Portugal)",
        "Portugués (Portugal)",
        "Portugais (Portugal)",
    ],
    "es": [
        "Spanish (Mexico)",
        "Español (México)",
        "Espagnol (Mexique)",
        "Spanish (Spain)",
        "Español (España)",
        "Espagnol (Espagne)",
        "Spanish (United States)",
        "Español (Estados Unidos)",
        "Espagnol (États-Unis)",
    ],
}

LANGUAGE_CODES_ALIASES_MAP = {
    alias: code for code, aliases in LANGUAGE_CODES_ALIASES.items() for alias in aliases
}
