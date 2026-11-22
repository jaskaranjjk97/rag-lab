"""Gradio web interface for the Icebreaker Bot."""

import logging
import sys
import uuid

import gradio as gr

import config

from modules.data_extraction import extract_linkedin_profile
from modules.data_preprocessing import (
    split_profile_data,
    create_vector_database,
)
from modules.query_engine import (
    generate_initial_facts,
    answer_user_query,
)

# Logging 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Store active profile indexes by session ID.
active_indices = {}

def process_profile(linkedin_url, use_mock):
    """Extract a LinkedIn profile and prepare its RAG index."""

    try:
        if not use_mock and not linkedin_url.strip():
            return "Please enter a LinkedIn profile URL.", None, []

        if use_mock and not linkedin_url.strip():
            linkedin_url = "https://www.linkedin.com/in/example/"

        profile_data = extract_linkedin_profile(
            linkedin_url,
            mock=use_mock,
            api_key=None if use_mock else config.APIFY_API_TOKEN,
        )

        if not profile_data:
            return "Failed to retrieve profile data.", None, []

        nodes = split_profile_data(profile_data)

        if not nodes:
            return "Failed to process profile data.", None, []

        index = create_vector_database(nodes)

        if index is None:
            return "Failed to create vector index.", None, []

        facts = generate_initial_facts(index)

        session_id = str(uuid.uuid4())
        active_indices[session_id] = index

        logger.info(
            "Profile processed successfully: %s",
            profile_data.get("full_name", "Unknown"),
        )

        result = (
            f"Profile processed successfully!\n\n"
            f"Name: {profile_data.get('full_name', 'Unknown')}\n\n"
            f"### Interesting facts\n\n{facts}"
        )

        return result, session_id, []

    except Exception:
        logger.exception("Error processing LinkedIn profile")
        return "An error occurred while processing the profile.", None, []

def chat_with_profile(session_id, user_query, chat_history):
    """Answer questions using the selected profile's vector index."""

    chat_history = chat_history or []

    if not user_query or not user_query.strip():
        return chat_history, ""

    if not session_id:
        chat_history.append(
            (user_query, "Please process a LinkedIn profile first.")
        )
        return chat_history, ""

    if session_id not in active_indices:
        chat_history.append(
            (user_query, "Session expired. Please process the profile again.")
        )
        return chat_history, ""

    try:
        index = active_indices[session_id]
        response=answer_user_query(index,user_query)
        chat_history.append((user_query, str(response)))

        return chat_history, ""
    except Exception:
        logger.exception("Error answering profile question")
        chat_history.append(
            (user_query, "Sorry, something went wrong while generating the answer.")
        )

        return chat_history, ""

def create_gradio_interface():
    """Build the Gradio application."""

    with gr.Blocks(title="LinkedIn AI Icebreakers") as demo:

        # Session state
        session_id=gr.State(value=None)

        gr.Markdown(
            """
            # LinkedIn AI Icebreakers

            Generate personalized conversation starters and ask
            questions about a LinkedIn profile using AI.
            """
        )


        with gr.Tab("Process Profile"):

            linkedin_url=gr.Textbox(
                label="LinkedIn Profile URL",
                placeholder="https://www.linkedin.com/in/username/",
            )
            use_mock=gr.Checkbox(
                label="Use mock profile data",
                value=False,
            )

            process_btn = gr.Button(
                "Process Profile",
                variant="primary",
            )

            result_text = gr.Markdown()

            process_btn.click(
                fn=process_profile,
                inputs=[linkedin_url,use_mock],
                outputs=[result_text,session_id,chatbot],
            )

        with gr.Tab("Chat"):

            gr.Markdown("Ask questions about the processed LinkedIn profile.")

            chatbot = gr.Chatbot(
                height=500,
                label="Profile Assistant",
            )

            chat_input=gr.Textbox(
                label="Your question",
                placeholder="What companies has this person worked for?",
            )

            chat_btn = gr.Button("Send", variant="primary")

            chat_btn.click(
                fn=chat_with_profile,
                inputs=[session_id, chat_input, chatbot],
                outputs=[chatbot, chat_input],
            )

            chat_input.submit(
                fn=chat_with_profile,
                inputs=[session_id, chat_input, chatbot],
                outputs=[chatbot, chat_input],
            )

    return demo

if __name__=="__main__":
    demo = create_gradio_interface()

    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=7860,
    )


