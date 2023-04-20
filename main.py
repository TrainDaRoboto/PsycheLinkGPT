import openai
import gradio as gr
import random

def get_api_key():
    api_key = ""
    while not api_key:
        api_key = input("Please enter your OpenAI API key: ").strip()
    return api_key

def setup_openai():
    api_key = get_api_key()
    openai.api_key = api_key

setup_openai()

PROMPTS = [
    "What are some tips for managing anxiety?",
    "How can I improve my mood?",
]

def psyche_link_gpt(input_text):
    prompt = f"PsycheLinkGPT: {input_text}"
    prompt_index = random.randint(0, len(PROMPTS) - 1)
    guidelines = PROMPTS[prompt_index]
    
    prompt = f"{guidelines}\n{prompt}\nResponse:"

    response = openai.Completion.create(
        engine="davinci",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=["PsycheLinkGPT:"],
        temperature=0.5,
    )

    return response.choices[0].text.strip()

input_text = gr.inputs.Textbox(lines=5, label="Input Text")
output_text = gr.outputs.Textbox(label="Output Text")

app = gr.Interface(psyche_link_gpt, inputs=input_text, outputs=output_text, title="PsycheLinkGPT")

if __name__ == "__main__":
    app.launch()
