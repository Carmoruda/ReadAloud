import gradio as gr
from gtts import gTTS

from utils.reader import reader
from utils.translator import translator

input_text_component = None
convert_btn_component = None
audio_output_component = None
input_type_component = None
input_file_component = None

pdf_selected = True


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

    return updates


def convert_to_audio(text, pdf):
    """
    Convert the input text to speech using GTTS (Google Text-to-Speech).

    Args:
        text (str): The text to convert to speech.

    Returns:
        str: The path to the generated audio file.
    """
    audio_file = None

    if pdf_selected:
        reader.read_pdf(pdf)
        tts = gTTS(text=reader.content, lang=translator.lang)
        audio_file = "output/output.mp3"
        tts.save(audio_file)
    else:
        # Generate audio from text
        tts = gTTS(text=text, lang=translator.lang)
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
        input_file_component

    with gr.Column() as tts_page:
        input_type_component = gr.Radio(
            [translator.t("TTS_PDF_input"), translator.t("TTS_Plain_Text_input")],
            label=translator.t("TTS_input_type"),
            value=translator.t("TTS_PDF_input"),
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

        convert_btn_component = gr.Button(value=translator.t("TTS_Button"), variant="primary")

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
