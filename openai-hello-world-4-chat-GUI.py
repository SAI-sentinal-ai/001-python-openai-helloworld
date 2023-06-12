# pyhton -m pip install gradio
import os
import openai
import gradio as gr

openai.api_key = os.environ["OPENAI_API_KEY"]

messages = [{"role": "system", "content": "You are a friendly, smart, assistant."}]

def openai_create(prompt):
    global messages
    messages.append({"role": "user", "content": prompt})
    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo",
        messages = messages
    )
    ChatGPT_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

def chatgpt_clone(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = openai_create(inp)
    history.append((input, output))
    return history, history

block = gr.Blocks(theme=gr.themes.Default())

with block:
    gr.Markdown("""<h1><center>ChatGPT 🤖 with OpenAI API & Gradio 🚀 </center></h1>
    """)
    chatbot = gr.Chatbot(label='GPT')
    message = gr.Textbox(placeholder="Your message...",label='User')
    state = gr.State()
    submit = gr.Button("Send")
    clear = gr.Button("Clear")
    submit.click(chatgpt_clone, inputs=[message, state], outputs=[chatbot, state])
    clear.click(lambda: None, None, chatbot, queue=False)

block.launch(debug = True)
