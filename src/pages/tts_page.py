import gradio as gr
from gtts import gTTS
from pydub import AudioSegment

from utils.language_codes import (
    LANGUAGE_CODES_ALIASES_MAP,
    TOP_LEVEL_DOMAIN_ALIASES_MAP,
)
from utils.reader import PDFReader as reader
from utils.translator import translator

SELECTED_ACCENT = "TTS_English_United_States"
ROBOTIC_ACTIVE = False

input_text_component = None
convert_btn_component = None
audio_output_component = None
input_type_component = None
input_file_component = None
input_robotic_component = None
tts_description = None
language_component = None

pdf_selected = True


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

    # If there is a component for robotic tone option, changes the
    # label and info to the translated values
    robotic_value = "On" if ROBOTIC_ACTIVE else "Off"
    if input_robotic_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_Robotic_input"),
                value=robotic_value,
            )
        )

    # If there is a component for TTS description (it's text), changes the
    # value to the translated description
    if tts_description:
        updates.append(gr.update(value=translator.t("TTS_Description")))

    # If there is a component for the language and dialect selection,
    # updates the choices and label to the translated values
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

    # Return the list of updates to be
    # applied to the TTS components
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

    # Get the selected language code and domain based on the selected accent
    code, domain = get_selected_language(SELECTED_ACCENT)

    if pdf_selected:
        # --- Generate audio from PDF ---
        # 1. Read the PDF content
        content = reader.read_pdf(pdf)
        # 2. Use the content from the reader and the
        # selected language code and domain
        tts = gTTS(text=content, lang=code, tld=domain)

    else:
        # --- Generate audio from text ---
        # 1. Use the input text and the selected language code and domain
        tts = gTTS(text=text, lang=code, tld=domain)

    # Save the audio file to the output directory
    audio_file = "output/output.mp3"
    # Save the audio file
    tts.save(audio_file)

    print(ROBOTIC_ACTIVE)

    if ROBOTIC_ACTIVE:
        # 1.. Load the audio with Pydub
        audio = AudioSegment.from_mp3(audio_file)

        # --- ROBOTIC TONE EFFECTS ---

        # Lower the sample rate (Lo-Fi effect)
        audio = audio.set_frame_rate(16000)

        # Increase the speed (raises the pitch slightly)
        audio = audio._spawn(
            audio.raw_data, overrides={"frame_rate": int(audio.frame_rate * 1.2)}
        ).set_frame_rate(audio.frame_rate)

        # 2. Export the modified audio back to the same file
        audio.export(audio_file, format="mp3")

    # Return the path to the generated audio file
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


def update_robotic_component(radio):
    """Update the robotic tone option based on the selected value.

    Args:
        radio (gr.Radio): The radio button component indicating the robotic tone option.

    Returns:
        gr.Radio: The updated state of the robotic tone component.
    """
    global ROBOTIC_ACTIVE

    value = radio

    if value == "On":
        ROBOTIC_ACTIVE = True
    else:
        ROBOTIC_ACTIVE = False


def create_page():
    """Creates the TTS page with input components, buttons, and audio output.

    Returns:
        gr.Column: The TTS page layout with all components.
    """
    global \
        input_text_component, \
        convert_btn_component, \
        audio_output_component, \
        input_type_component, \
        input_file_component, \
        input_robotic_component, \
        tts_description, \
        language_component

    # Create the TTS page using the column layout
    with gr.Column() as tts_page:
        # Set the title for the TTS page
        gr.Markdown("## Google Text-to-Speech (gTTS)")

        # Set the description for the TTS page. It explains the functionality of the
        # gtts module/library and how it can be used to convert text to speech.
        tts_description = gr.Markdown(translator.t("TTS_Description"))

        # Row for the input type selection and language selection
        with gr.Row():
            # Radio button for selecting the input type (PDF or plain text)
            # The default value is set to "PDF" input
            input_type_component = gr.Radio(
                [translator.t("TTS_PDF_input"), translator.t("TTS_Plain_Text_input")],
                label=translator.t("TTS_input_type"),
                value=translator.t("TTS_PDF_input"),
            )

            # Dropdown that allows the user to select the language and dialect for TTS
            # The choices are based on the available languages and dialects in the gtts library
            # The default value is set to "English (United States)"
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

        # Row for the robotic tone option
        with gr.Row():
            # Toggle for selecting robotic tone effect
            # The default value is set to "Off"
            input_robotic_component = gr.Radio(
                ["On", "Off"],
                label=translator.t("TTS_Robotic_input"),
                value="Off",
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

        # Set

        # Set the function to convert the input text or PDF to audio when the user clicks
        # the convert button. It takes the input text and file as inputs and outputs the
        # generated audio file to the audio output component.
        convert_btn_component.click(
            fn=convert_to_audio,
            inputs=[input_text_component, input_file_component],
            outputs=audio_output_component,
        )

        # Set the function to change the accent when the user selects a different accent and
        # dialect from the dropdown.
        language_component.change(
            fn=change_accent,
            inputs=language_component,
        )

        # Set the function to update the robotic tone option when the user toggles it.
        input_robotic_component.change(
            fn=update_robotic_component,
            inputs=input_robotic_component,
        )

    # Return the TTS page layout with all components
    return tts_page


def reload_page():
    """Reloads the TTS page components to reflect the current language settings.

    Returns:
        list: A list of gr.update() objects to update the TTS components.
    """

    return update_tts_components()
