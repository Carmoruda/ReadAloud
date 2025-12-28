import edge_tts
import gradio as gr
from pydub import AudioSegment

from utils.language_codes import (
    TOP_LEVEL_DOMAIN_ALIASES_MAP_MALE_EDGE,
)
from utils.reader import PDFReader as reader
from utils.translator import translator

SELECTED_ACCENT = "English (United States)"
ROBOTIC_ACTIVE = False
ROBOTIC_BITRATE = 12000
ROBOTIC_ECO = False
OUTPUT_FORMAT = "mp3"

input_text_component = None
convert_btn_component = None
audio_output_component = None
input_type_component = None
input_file_component = None
output_robotic_component = None
output_robotic_bitrate_component = None
output_robotic_eco_component = None
tts_description = None
language_component = None
output_format_component = None

pdf_selected = True


def get_selected_language(accent):
    """
    Returns the selected language code and domain based on the provided accent.

    Args:
        accent (str): The accent/language name (e.g., "Spanish (Spain)")

    Returns:
        voice_code (str): The corresponding language code for edge-tts.
    """
    voice_code = TOP_LEVEL_DOMAIN_ALIASES_MAP_MALE_EDGE.get(
        accent, "English (United States)"
    )

    print(f"Found voice: {voice_code}")

    return voice_code


def change_accent(language):
    global SELECTED_ACCENT
    SELECTED_ACCENT = language
    print(f"Selected accent: {SELECTED_ACCENT}")


def change_output_format(output_format):
    """Change the format of the generated file.

    Args:
        output_format (str): The desired output format (e.g., "mp3", "wav", "ogg")
    """
    global OUTPUT_FORMAT
    OUTPUT_FORMAT = output_format
    print(f"Selected output format: {OUTPUT_FORMAT}")


def update_tts_components():
    """
    Updates the labels and values of the TTS components when the language changes.
    Returns a list of gr.update() objects.
    """
    global ROBOTIC_ACTIVE
    global ROBOTIC_ECO

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
    if output_robotic_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_Robotic_input"),
                value=robotic_value,
            )
        )

    # If there is a component for robotic tone eco option, changes the
    # label to the translated value
    eco_value = "On" if ROBOTIC_ECO else "Off"
    if output_robotic_eco_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_Robotic_Eco"),
                value=eco_value,
            )
        )

    # If there is a component for robotic tone bitrate, changes the
    # label to the translated value
    if output_robotic_bitrate_component:
        updates.append(
            gr.update(
                label=translator.t("TTS_Robotic_Bitrate"),
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

    # If there is a component for the output format selection,
    # updates the choices and label to the translated values
    if output_format_component:
        updates.append(
            gr.update(
                choices=[
                    "mp3",
                    "wav",
                    "ogg",
                ],
                label=translator.t("TTS_Output_Format"),
                value=OUTPUT_FORMAT,
            )
        )

    # Return the list of updates to be
    # applied to the TTS components
    return updates


async def convert_to_audio(text, pdf):
    """
    Convert the input text to speech using GTTS (Google Text-to-Speech).

    Args:
        text (str): The text to convert to speech.

    Returns:
        str: The path to the generated audio file.
    """
    global SELECTED_ACCENT
    global ROBOTIC_ACTIVE
    global ROBOTIC_BITRATE
    global ROBOTIC_ECO
    global OUTPUT_FORMAT

    audio_file = None

    # Get the selected language code and domain based on the selected accent
    voice_code = get_selected_language(SELECTED_ACCENT)

    if pdf_selected:
        # --- Generate audio from PDF ---
        # 1. Read the PDF content
        content = reader.read_pdf(pdf)
        # 2. Use the content from the reader and the
        # selected language code and domain
        tts = edge_tts.Communicate(text=content, voice=voice_code)
    else:
        # --- Generate audio from text ---
        # 1. Use the input text and the selected language code and domain
        tts = edge_tts.Communicate(text=text, voice=voice_code)

    # Always save the raw TTS output as MP3 (gTTS native format)
    base_mp3 = "output/output.mp3"
    await tts.save(base_mp3)

    print(f"Generated audio file: {base_mp3} (Voice code: {voice_code})")

    # Prepare final output path based on selected format
    final_path = (
        base_mp3 if OUTPUT_FORMAT == "mp3" else f"output/output.{OUTPUT_FORMAT}"
    )

    # Apply robotic effects and/or format conversion if needed
    if ROBOTIC_ACTIVE or OUTPUT_FORMAT != "mp3":
        audio = AudioSegment.from_mp3(base_mp3)

        if ROBOTIC_ACTIVE:
            ## 1. Bitcrush Effect:
            # Lower the fidelity to lose the "human" shine of edge-tts
            audio = audio.set_frame_rate(ROBOTIC_BITRATE).set_frame_rate(44100)

            if ROBOTIC_ECO:
                # 2. Cyborg ring: Double-layered micro-delays
                # This simulates a metallic chassis reflection
                metallic_layer_1 = audio - 12  # A bit softer
                metallic_layer_2 = audio - 15  # Even softer
                metallic_layer_3 = audio - 18  # Very soft

                # Overlay with extremely short delays (less than 50ms)
                # This does not create an echo, but a "phase" that sounds robotic
                audio = audio.overlay(metallic_layer_1, position=20)
                audio = audio.overlay(metallic_layer_2, position=40)
                audio = audio.overlay(metallic_layer_3, position=60)

            # 3. Add a bit of compression
            # Robots don't have inflections. We can flatten the volume a bit
            audio = audio.compress_dynamic_range()

        audio.export(final_path, format=OUTPUT_FORMAT)

    # Return the path to the generated audio file
    audio_file = final_path

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
        return [gr.Slider(visible=True), gr.Radio(visible=True)]
    else:
        ROBOTIC_ACTIVE = False
        return [gr.Slider(visible=False), gr.Radio(visible=False)]


def update_slider(bitrate):
    """Update the robotic tone bitrate based on the selected value.

    Args:
        bitrate (gr.Slider): The slider component indicating the robotic tone bitrate.

    Returns:
        None
    """
    global ROBOTIC_BITRATE

    ROBOTIC_BITRATE = bitrate


def update_eco_component(radio):
    """Update the robotic eco option based on the selected value.

    Args:
        radio (gr.Radio): The radio button component indicating the robotic eco option.

    Returns:
        None
    """
    global ROBOTIC_ECO

    value = radio

    if value == "On":
        ROBOTIC_ECO = True
    else:
        ROBOTIC_ECO = False


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
        output_robotic_component, \
        output_robotic_bitrate_component, \
        output_robotic_eco_component, \
        tts_description, \
        language_component, \
        output_format_component

    # Create the Edge TTS page using the column layout
    with gr.Column() as tts_page:
        # Set the title for the Edge TTS page
        gr.Markdown("## Edge Text-to-Speech (Edge TTS)")

        # Set the description for the Edge TTS page. It explains the functionality of the
        # edge-tts module/library and how it can be used to convert text to speech.
        tts_description = gr.Markdown(translator.t("Edge_TTS_Description"))

        # Group for the input type selection and language selection
        with gr.Group():
            # Radio button for selecting the input type (PDF or plain text)
            # The default value is set to "PDF" input
            input_type_component = gr.Radio(
                [translator.t("TTS_PDF_input"), translator.t("TTS_Plain_Text_input")],
                label=translator.t("TTS_input_type"),
                value=translator.t("TTS_PDF_input"),
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

        with gr.Row():
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

            # Dropdown that allows the user to select the output audio format
            # The choices are "mp3", "wav", and "ogg"
            # The default value is set to "mp3"
            output_format_component = gr.Dropdown(
                choices=[
                    "mp3",
                    "wav",
                    "ogg",
                ],
                label=translator.t("TTS_Output_Format"),
                value=OUTPUT_FORMAT,
                interactive=True,
            )

        # Row for the robotic tone option
        with gr.Row():
            # Toggle for selecting robotic tone effect
            # The default value is set to "Off"
            output_robotic_component = gr.Radio(
                ["On", "Off"],
                label=translator.t("TTS_Robotic_input"),
                value="Off",
            )

            # Toggle for selecting robotic eco effect
            # The default value is set to "Off" and
            # is initially hidden
            output_robotic_eco_component = gr.Radio(
                ["On", "Off"],
                label=translator.t("TTS_Robotic_Eco"),
                value="Off",
                visible=False,
            )

            # Slider for selecting the robotic tone bitrate
            # The default value is set to 16000 Hz and is initially hidden
            output_robotic_bitrate_component = gr.Slider(
                minimum=8000,
                maximum=16000,
                step=100,
                label=translator.t("TTS_Robotic_Bitrate"),
                value=ROBOTIC_BITRATE,
                visible=False,
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
            inputs=[input_text_component, input_file_component],
            outputs=audio_output_component,
        )

        # Set the function to change the accent when the user selects a different accent and
        # dialect from the dropdown.
        language_component.change(
            fn=change_accent,
            inputs=language_component,
        )

        # Set the function to change the output format when the user selects a different format
        # from the dropdown.
        output_format_component.change(
            fn=change_output_format,
            inputs=output_format_component,
        )

        # Set the function to update the robotic tone option when the user toggles it.
        output_robotic_component.change(
            fn=update_robotic_component,
            inputs=output_robotic_component,
            outputs=[output_robotic_bitrate_component, output_robotic_eco_component],
        )

        output_robotic_eco_component.change(
            fn=update_eco_component,
            inputs=output_robotic_eco_component,
        )

        # Set the function to update the slider when the user moves it.
        output_robotic_bitrate_component.change(
            fn=update_slider,
            inputs=output_robotic_bitrate_component,
        )

    # Return the TTS page layout with all components
    return tts_page


def reload_page():
    """Reloads the TTS page components to reflect the current language settings.

    Returns:
        list: A list of gr.update() objects to update the TTS components.
    """

    return update_tts_components()
