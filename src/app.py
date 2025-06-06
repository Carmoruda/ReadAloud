import gradio as gr

import tts_page
from utils.translator import translator

SELECTED_LANGUAGE = "Languages_EN"


def reload_interface(language):
    """
    Reload the interface to apply the selected language.

    Args:
        language (str): The name of the language selected by the user.

    Returns:
        gr.update: An update object to refresh the interface.
    """
    global SELECTED_LANGUAGE

    change_language(language)

    select_value = translator.t(SELECTED_LANGUAGE).replace("[", "").replace("]", "")

    print(f"Setting dropdown value to: {select_value}, type: {type(select_value)}")
    tts_updates = tts_page.reload_page()

    return (
        # Update the configuration text and language dropdown
        gr.update(value=f"### {translator.t('Configuration')}"),
        gr.update(
            choices=[
                translator.t("Languages_ES"),
                translator.t("Languages_EN"),
                translator.t("Languages_FR"),
            ],
            label=translator.t("Language"),
            value=select_value,
        ),
        # Update the app description
        gr.update(value=translator.t("App_Description")),
        # Update the TTS page components
        *tts_updates,
    )


def change_language(language):
    """
    Change the language of the application based on user selection.
    This function retrieves the language code from the translator module and sets the application's language accordingly.

    Args:
        language (str): The name of the language selected by the user.
    """
    global SELECTED_LANGUAGE

    # Get the language code from the translator module
    code = translator.get_language_code(language)

    # Set the language in the translator module
    translator.set_language(code)

    # Update the global variable for selected language
    SELECTED_LANGUAGE = translator.t("Languages_" + code.upper())

    # Print the selected language for debugging purposes
    print(f"Language changed to: {SELECTED_LANGUAGE} ({code})")


# --- MAIN APPLICATION ---

with gr.Blocks(title="ReadAloud") as demo:
    # Main content
    gr.Markdown("# ReadAloud")

    app_description = gr.Markdown(translator.t("App_Description"))

    with gr.Tabs() as tabs:
        with gr.Tab("GTTS", id="GTTS"):
            other_page = tts_page.create_page()

        # with gr.Tab("Google Cloud TTS", id="GoogleCloudTTS"):
        #     google_page = google_cloud_page.create_page()

    with gr.Sidebar():
        gr.Markdown("# ReadAloud")
        gr.Markdown("---")

        configuration_text = gr.Markdown(f"### {translator.t('Configuration')}")
        language = gr.Dropdown(
            choices=[
                translator.t("Languages_ES"),
                translator.t("Languages_EN"),
                translator.t("Languages_FR"),
            ],
            label=translator.t("Language"),
            value=translator.t(SELECTED_LANGUAGE),
            interactive=True,
        )

        language.change(
            fn=reload_interface,
            inputs=language,
            outputs=[
                configuration_text,
                language,
                app_description,
                tts_page.input_text_component,
                tts_page.convert_btn_component,
                tts_page.audio_output_component,
                tts_page.input_type_component,
                tts_page.input_file_component,
                tts_page.tts_description,
                tts_page.language_component,
            ],
        )

lang_code = SELECTED_LANGUAGE.split("_")[1]
translator.set_language(lang_code)
demo.launch()
