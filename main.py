import requests
import openai
import os
import gradio as gr



CONFIG_FILE = "config.ini"
history = ""

def get_api_key_from_file():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return file.readline().strip()
    return None

def save_api_key_to_file(api_key):
    with open(CONFIG_FILE, "w") as file:
        file.write(api_key)
import json

def moderate_response(api_key, response):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    data = {
        "input": response
    }

    response = requests.post(
        "https://api.openai.com/v1/moderations",
        headers=headers,
        data=json.dumps(data),
    )

    if response.status_code == 200:
        moderation_result = response.json()
        flagged = moderation_result["results"][0]["flagged"]
        return not flagged
    else:
        return False
def generate_text(api_key, prompt, input_text):
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"{prompt}\nUser: {input_text}\nAI:",
            max_tokens=100,
            n=1,
            stop=["\nUser:", "\nAI:"],
            temperature=0.5,
        )
        generated_text = response.choices[0].text.strip()
        if moderate_response(api_key, generated_text):
            return generated_text
        else:
            return "The generated response was not appropriate. Please try again."
    except openai.error.AuthenticationError as e:
        return f"The API key is invalid or an error occurred. Error message: {str(e)}"

def chatbot(input, prompt):
    api_key = get_api_key_from_file()
    if not api_key:
        return "No API key found. Please provide an API key."
    return generate_text(api_key, prompt, input)

prompt_input = gr.inputs.Dropdown(choices=[
    "I want you to act as my friend and assistant when getting through a hard time. This may mean giving me helpful tips, assurances, and redirecting from poor thought cycles. You are to calmly analyze the situations as I give them and also try and give open, respectful but alternative point of views too. You are to assist the user in building up their empathy so that they can build themselves up.",
    "I want you to act as a limited therapist (understanding your own shortcomings) to assist individuals through major life issues and decisions. These concepts are necessary for the individual to heal and live their life happily."
], label="Select a Prompt")
input_text = gr.inputs.Textbox(lines=7, label="Chat with AI")
output_text = gr.outputs.Textbox(label="Reply")

iface = gr.Interface(
    fn=chatbot,
    inputs=[input_text, prompt_input],
    outputs=output_text,
    allow_flagging="never",
    title="PycheLinkGPT",
    description="Talk it out with a non-judgemental bot!",
    theme="compact"
)

iface.launch(share=True)