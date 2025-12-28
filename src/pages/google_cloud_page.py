import os

import gradio as gr
from google.cloud import texttospeech_v1 as texttospeech

from utils.reader import PDFReader as reader
from utils.translator import translator

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "secret/Credentials.json"
os.environ["GOOGLE_CLOUD_PROJECT"] = "modular-glider-461309-v9"
SELECTED_ACCENT = "TTS_English_United_States"

input_text_component = None
convert_btn_component = None
audio_output_component = None
input_type_component = None
input_file_component = None
google_cloud_tts_description = None
output_name_component = None

pdf_selected = True


def update_google_cloud_tts_components():
    """
    Updates the labels and values of the Google Coud TTS components when the language changes.
    Returns a list of gr.update() objects.
    """
    # Initialize the list of updates
    updates = []

    # If there is a component for raw input text, changes the
    # label and placeholder to the translated values
    if input_text_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_Text_input"),
                placeholder=translator.t("TTS_Text_input_placeholder"),
            )
        )

    # If there is a component for the convert button, changes the
    # value to the translated button text
    if convert_btn_component:
        updates.append(gr.update(value=translator.t("TTS_Button")))

    # If there is a component for audio output, changes the
    # label to the translated audio label
    if audio_output_component:
        updates.append(gr.update(label=translator.t("Generated_Audio")))

    # If there is a component for input type (PDF or text), changes the
    # choices and label to the translated values
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

    # If there is a component for input file (PDF), changes the
    # label to the translated PDF input placeholder
    if input_file_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_PDF_input_placeholder"),
            )
        )

    # If there is a component for Google Cloud TTS description (it's text), changes the
    # value to the translated description
    if google_cloud_tts_description:
        updates.append(gr.update(value=translator.t("Google_Cloud_TTS_Description")))

    # Return the list of updates to be
    # applied to the Google Cloud TTS components
    return updates


def convert_to_audio(text, pdf, output_name):
    """
    Convert the input text to speech using GTTS (Google Text-to-Speech).

    Args:
        text (str): The text to convert to speech.

    Returns:
        str: The path to the generated audio file.
    """
    global SELECTED_ACCENT

    audio_file = None

    if pdf_selected:
        # --- Generate audio from PDF ---
        content = reader.read_pdf(pdf)

        # Crear cliente
        client = texttospeech.TextToSpeechLongAudioSynthesizeClient()

        # Texto a convertir
        synthesis_input = texttospeech.SynthesisInput(text=content)

        # Configuración de voz (puedes cambiar idioma o nombre de voz)
        voice = texttospeech.VoiceSelectionParams(
            language_code="es-ES",  # o "es-US" para español latino
            name="es-ES-Chirp3-HD-Alnilam",  # busca otras voces disponibles si quieres
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        # Configuración del audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Solicitud de síntesis
        parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/us-central1"
        request = texttospeech.SynthesizeLongAudioRequest(
            parent=parent,
            input=synthesis_input,
            audio_config=audio_config,
            voice=voice,
            output_gcs_uri=f"gs://audio_podcast_carmoruda/{output_name}.wav",
        )

        # Ejecutar la operación (esto es largo y bloqueante)
        operation = client.synthesize_long_audio(request=request)

        # Esperar el resultado
        response = operation.result(timeout=300)

        # Descargar el archivo resultante
        audio_bytes = response.audio_content
        os.makedirs(
            os.path.dirname(f"output/{output_name_component}.wav"), exist_ok=True
        )
        with open(f"output/{output_name_component}.wav", "wb") as out:
            out.write(audio_bytes)

        print(f"✅ Audio generado y guardado en: 'output/{output_name_component}.wav'")
        return f"output/{output_name_component}.wav"

    else:
        # --- Generate audio from text ---
        client = texttospeech.TextToSpeechClient()

        # Texto a convertir
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Configuración de voz (puedes cambiar idioma o nombre de voz)
        voice = texttospeech.VoiceSelectionParams(
            language_code="es-ES",  # o "es-US" para español latino
            name="es-ES-Chirp3-HD-Alnilam",  # busca otras voces disponibles si quieres
            ssml_gender=texttospeech.SsmlVoiceGender.MALE,
        )

        # Configuración del audio
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        # Solicitud de síntesis
        audio_file = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        with open("output/voz_hd.wav", "wb") as out:
            out.write(audio_file.audio_content)
            print('Audio generado como "voz_hd.wav"')

    # Return the path to the generated audio file
    return "output/voz_hd.wav"


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
    """Creates the Google Cloud TTS page with input components, buttons, and audio output.

    Returns:
        gr.Column: The Google Cloud TTS page layout with all components.
    """
    global \
        input_text_component, \
        convert_btn_component, \
        audio_output_component, \
        input_type_component, \
        input_file_component, \
        google_cloud_tts_description, \
        output_name_component

    # Create the TTS page using the column layout
    with gr.Column() as google_cloud_page:
        # Set the title for the GCTTS page
        gr.Markdown("## Google Cloud Text-to-Speech")

        # Set the description for the Google Cloud Text to Speech page. It explains the functionality of the
        # gtts module/library and how it can be used to convert text to speech.
        google_cloud_tts_description = gr.Markdown(
            translator.t("Google_Cloud_TTS_Description")
        )

        # Row for the input type selection and language selection
        with gr.Row():
            # Radio button for selecting the input type (PDF or plain text)
            # The default value is set to "PDF" input
            input_type_component = gr.Radio(
                [translator.t("TTS_PDF_input"), translator.t("TTS_Plain_Text_input")],
                label=translator.t("TTS_input_type"),
                value=translator.t("TTS_PDF_input"),
            )

            output_name_component = gr.Textbox(
                label="Output File Name",
                placeholder="Enter the name for the output audio file",
                value="voz_had",
            )

        # Textbox where the user can input text to be converted to speech.
        # This component is initially hidden and will be shown when the user selects
        # the "Plain Text" input type.
        input_text_component = gr.Textbox(
            label=translator.t("TTS_Text_input"),
            placeholder=translator.t("TTS_Text_input_placeholder"),
            lines=5,
            visible=False,
        )

        # File component where the user can upload a PDF file to be converted to speech.
        # This component is initially visible and will be hidden when the user selects
        # the "Plain Text" input type.
        # When the user selects the "PDF" input type, this component will be shown
        # and the user can upload a PDF file to be converted to speech.
        input_file_component = gr.File(
            label=translator.t("TTS_PDF_input_placeholder"),
            file_types=[".pdf"],
            visible=True,
            file_count="single",
        )

        # Button that the user clicks to convert the input text or PDF to speech.
        convert_btn_component = gr.Button(
            value=translator.t("TTS_Button"), variant="primary"
        )

        # Audio output component that will play the generated audio file.
        # This component shows a download button for the generated audio file.
        audio_output_component = gr.Audio(
            label=translator.t("Generated_Audio"), show_download_button=True
        )

        # Set the function to update the visibility of the input text and file components
        # based on the selected input type (PDF or plain text).
        # When the user selects "PDF", the input file component will be shown
        # and the input text component will be hidden.
        input_type_component.change(
            fn=update_visibility,
            inputs=input_type_component,
            outputs=[input_text_component, input_file_component],
        )

        # Set the function to convert the input text or PDF to audio when the user clicks
        # the convert button. It takes the input text and file as inputs and outputs the
        # generated audio file to the audio output component.
        convert_btn_component.click(
            fn=convert_to_audio,
            inputs=[input_text_component, input_file_component, output_name_component],
            outputs=audio_output_component,
        )

    # Return the google cloud page layout with all components
    return google_cloud_page


def reload_page():
    """Reloads the TTS page components to reflect the current language settings.

    Returns:
        list: A list of gr.update() objects to update the TTS components.
    """

    return update_google_cloud_tts_components()
