import gradio as gr
from gtts import gTTS

from utils.language_codes import (
    LANGUAGE_CODES_ALIASES_MAP,
    TOP_LEVEL_DOMAIN_ALIASES_MAP,
)
from utils.reader import reader
from utils.translator import translator

input_text_component = None
convert_btn_component = None
audio_output_component = None
input_type_component = None
input_file_component = None
tts_description = None
language_component = None

pdf_selected = True

SELECTED_ACCENT = "TTS_English_United_States"


def get_selected_language(accent):
    """
    Returns the selected language code and domain based on the provided accent.

    Args:
        accent (str): The accent/language name (e.g., "Spanish (Spain)")

    Returns:
        tuple: (language_code, domain)
    """
    # Search for the language code
    code = LANGUAGE_CODES_ALIASES_MAP.get(accent, "en")

    # Search for the domain
    domain = TOP_LEVEL_DOMAIN_ALIASES_MAP.get(accent, "com")

    return code, domain


def change_accent(language):
    global SELECTED_ACCENT
    SELECTED_ACCENT = language
    print(f"Selected accent: {SELECTED_ACCENT}")


def update_tts_components():
    """
    Updates the labels and values of the TTS components when the language changes.
    Returns a list of gr.update() objects.
    """
    updates = []

    if input_text_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_Text_input"),
                placeholder=translator.t("TTS_Text_input_placeholder"),
            )
        )

    if convert_btn_component:
        updates.append(gr.update(value=translator.t("TTS_Button")))

    if audio_output_component:
        updates.append(gr.update(label=translator.t("Generated_Audio")))

    if input_type_component:
        updates.append(
            gr.update(
                choices=[
                    translator.t("TTS_PDF_input"),
                    translator.t("TTS_Plain_Text_input"),
                ],
                label=translator.t("TTS_input_type"),
                value=translator.t("TTS_PDF_input"),
            )
        )

    if input_file_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_PDF_input_placeholder"),
            )
        )

    if tts_description:
        updates.append(gr.update(value=translator.t("TTS_Description")))

    if language_component:
        updates.append(
            gr.update(
                choices=[
                    translator.t("TTS_English_Australia"),
                    translator.t("TTS_English_United_Kingdom"),
                    translator.t("TTS_English_United_States"),
                    translator.t("TTS_English_Canada"),
                    translator.t("TTS_English_India"),
                    translator.t("TTS_English_Ireland"),
                    translator.t("TTS_English_South_Africa"),
                    translator.t("TTS_English_Nigeria"),
                    translator.t("TTS_French_Canada"),
                    translator.t("TTS_French_France"),
                    translator.t("TTS_Mandarin_China_Mainland"),
                    translator.t("TTS_Mandarin_Taiwan"),
                    translator.t("TTS_Portuguese_Brazil"),
                    translator.t("TTS_Portuguese_Portugal"),
                    translator.t("TTS_Spanish_Mexico"),
                    translator.t("TTS_Spanish_Spain"),
                    translator.t("TTS_Spanish_United_States"),
                ],
                label=translator.t("TTS_Local_Accent"),
                value=translator.t("TTS_English_United_States"),
            )
        )

    return updates


def convert_to_audio(text, pdf):
    """
    Convert the input text to speech using GTTS (Google Text-to-Speech).

    Args:
        text (str): The text to convert to speech.

    Returns:
        str: The path to the generated audio file.
    """
    global SELECTED_ACCENT
    audio_file = None

    code, domain = get_selected_language(SELECTED_ACCENT)

    if pdf_selected:
        # Generate audio from PDF
        reader.read_pdf(pdf)
        tts = gTTS(text=reader.content, lang=code, tld=domain)
        audio_file = "output/output.mp3"
        tts.save(audio_file)
    else:
        # Generate audio from text
        tts = gTTS(text=text, lang=code, tld=domain)
        audio_file = "output/output.mp3"
        tts.save(audio_file)

    return audio_file


def update_visibility(radio):
    """Update the visibility of the input PDF and text components based on the selected input type.

    Args:
        radio (gr.Radio): The radio button component indicating the input type.

    Returns:
        gr.Textbox: The updated visibility state of the input text component.
    """
    global pdf_selected

    value = radio

    if value == translator.t("TTS_PDF_input"):
        pdf_selected = True
        return (gr.Textbox(visible=False), gr.File(visible=True))
    else:
        pdf_selected = False
        return (gr.Textbox(visible=True), gr.File(visible=False))


def create_page():
    global \
        input_text_component, \
        convert_btn_component, \
        audio_output_component, \
        input_type_component, \
        input_file_component, \
        tts_description, \
        language_component

    with gr.Column() as tts_page:
        tts_description = gr.Markdown(translator.t("TTS_Description"))

        with gr.Row():
            input_type_component = gr.Radio(
                [translator.t("TTS_PDF_input"), translator.t("TTS_Plain_Text_input")],
                label=translator.t("TTS_input_type"),
                value=translator.t("TTS_PDF_input"),
            )

            language_component = gr.Dropdown(
                choices=[
                    translator.t("TTS_English_Australia"),
                    translator.t("TTS_English_United_Kingdom"),
                    translator.t("TTS_English_United_States"),
                    translator.t("TTS_English_Canada"),
                    translator.t("TTS_English_India"),
                    translator.t("TTS_English_Ireland"),
                    translator.t("TTS_English_South_Africa"),
                    translator.t("TTS_English_Nigeria"),
                    translator.t("TTS_French_Canada"),
                    translator.t("TTS_French_France"),
                    translator.t("TTS_Mandarin_China_Mainland"),
                    translator.t("TTS_Mandarin_Taiwan"),
                    translator.t("TTS_Portuguese_Brazil"),
                    translator.t("TTS_Portuguese_Portugal"),
                    translator.t("TTS_Spanish_Mexico"),
                    translator.t("TTS_Spanish_Spain"),
                    translator.t("TTS_Spanish_United_States"),
                ],
                label=translator.t("TTS_Local_Accent"),
                value=translator.t("TTS_English_United_States"),
                interactive=True,
            )

            language_component.change(
                fn=change_accent,
                inputs=language_component,
            )

        input_text_component = gr.Textbox(
            label=translator.t("TTS_Text_input"),
            placeholder=translator.t("TTS_Text_input_placeholder"),
            lines=5,
            visible=False,
        )

        input_file_component = gr.File(
            label=translator.t("TTS_PDF_input_placeholder"),
            file_types=[".pdf"],
            visible=True,
            file_count="single",
        )

        convert_btn_component = gr.Button(
            value=translator.t("TTS_Button"), variant="primary"
        )

        audio_output_component = gr.Audio(
            label=translator.t("Generated_Audio"), show_download_button=True
        )

        input_type_component.change(
            fn=update_visibility,
            inputs=input_type_component,
            outputs=[input_text_component, input_file_component],
        )

        convert_btn_component.click(
            fn=convert_to_audio,
            inputs=[input_text_component, input_file_component],
            outputs=audio_output_component,
        )

    return tts_page


def reload_page():
    return update_tts_components()
