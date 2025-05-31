import gradio as gr
from gtts import gTTS

from utils.translator import translator

input_text_component = None
convert_btn_component = None
audio_output_component = None


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

    return updates


def convert_text(text):
    """
    Convert the input text to speech using GTTS (Google Text-to-Speech).

    Args:
        text (str): The text to convert to speech.

    Returns:
        str: The path to the generated audio file.
    """

    # Generate audio from text
    tts = gTTS(text=text, lang=translator.lang)
    audio_file = "output/output.mp3"
    tts.save(audio_file)

    return audio_file


def create_page():
    global input_text_component, convert_btn_component, audio_output_component

    with gr.Column() as tts_page:
        input_text_component = gr.Textbox(
            label=translator.t("TTS_Text_input"),
            placeholder=translator.t("TTS_Text_input_placeholder"),
            lines=5,
        )

        convert_btn_component = gr.Button(value=translator.t("TTS_Button"), variant="primary")

        audio_output_component = gr.Audio(
            label=translator.t("Generated_Audio"), show_download_button=True
        )

        convert_btn_component.click(
            fn=convert_text, inputs=input_text_component, outputs=audio_output_component
        )

    return tts_page


def reload_page():
    return update_tts_components()
