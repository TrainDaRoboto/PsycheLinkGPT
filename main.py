import openai
import gradio as gr
import random

# Define your OpenAI API key
def get_api_key():
    api_key = ""
    while not api_key:
        api_key = input("Please enter your OpenAI API key: ").strip()
    return api_key

# Set up the OpenAI API client
def setup_openai():
    api_key = get_api_key()
    openai.api_key = api_key

# Set up the OpenAI API client
setup_openai()

# Define your prompts
PROMPTS = [
    "What are some tips for managing anxiety?",
    "How can I improve my mood?",
]

# Define the PsycheLinkGPT chatbot function
def psyche_link_gpt(input_text):
    # Define the prompt for the GPT-3 model
    prompt = f"{input_text}\nPsycheLinkGPT:"

    # Choose a random prompt to use
    prompt_index = random.randint(0, len(PROMPTS) - 1)
    prompt = PROMPTS[prompt_index] + " " + prompt

    # Generate a response using the GPT-3 model
    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Return the generated response
    return response.choices[0].text.strip()

# Define the Gradio user interface
input_text = gr.inputs.Textbox(lines=5, label="Input Text")
output_text = gr.outputs.Textbox(label="Output Text")

app = gr.Interface(psyche_link_gpt, inputs=input_text, outputs=output_text, title="PsycheLinkGPT")

# Launch the Gradio interface
if __name__ == "__main__":
    app.launch()