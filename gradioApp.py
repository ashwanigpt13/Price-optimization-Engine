import gradio as gr
import subprocess
import time

with gr.Blocks() as ui:
    with gr.Column():
        with gr.Column():
            with gr.Row():
                Delta = gr.Textbox(label="Delta",value="10")
                inventory = gr.Textbox(label="inventory",value = "100")
            with gr.Row():
                result = gr.Textbox(label="price_you_should_set_today",value="0")
        generate_btn = gr.Button("Get Suggested Price")

    def generate(Delta,inventory):
        print("in Generation")
        print(Delta)
        print(inventory)
        currTime = time.time()
        command = f"python3 predict.py --Delta {Delta} --inventory {inventory} --ctime {currTime} "
        subprocess.call(command,shell=True)
        with open(f'output.txt','r') as f:
            price = f.readline()
        return str(price)
    
    generate_btn.click(
    generate,
    [Delta,inventory],
    result)

ui.launch(share=True)