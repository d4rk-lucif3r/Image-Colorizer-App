import os 
os.chdir('./DeOldify')
import sys
sys.path.append('.')

import warnings
from deoldify.visualize import *
import gradio as gr
import torch
from deoldify import device
from deoldify.device_id import DeviceId
import logging
logging.basicConfig(level=logging.INFO)
device.set(device=DeviceId.CPU)
warnings.filterwarnings("ignore", category=UserWarning,
                        message=".*?Your .*? set is empty.*?")
colorizer = get_image_colorizer(artistic=True)

filepath = 'test_images/image.png'
demo = gr.Blocks(title='B/W Image Colorizer')  # Create a gradio block


def colorize(image_path):
    '''Colorize a single image'''
    render_factor = 35
    image_path = colorizer.plot_transformed_image(
        path=image_path, render_factor=render_factor, compare=False, watermarked=False)
    logging.info(f'Image saved to {image_path}')
    return image_path


with demo:
    gr.Markdown("# B/W Image Colorizer")
    with gr.Tabs():
        with gr.TabItem("Examples"):  # If the user wants to use the examples
            with gr.Row():
                rad1 = gr.components.Radio(
                    ['Image 1', 'Image 2'], label='Select Image and wait till it appears!')  # Radio button to select the image
                img1 = gr.Image(label="Image 1", shape=(300, 300))
            submit1 = gr.Button('Submit')
        with gr.TabItem("Do it yourself!"):  # If the user wants to add their own image
            with gr.Row():
                img3 = gr.Image(label="Image 1", shape=(300, 300))
            submit2 = gr.Button('Submit')

        def action1(choice):  # Function to show the article when the user selects the article
            global filepath
            if choice == 'Image 1':
                filepath = 'test_images/image.png'
                return 'test_images/image.png'
            elif choice == 'Image 2':
                filepath = 'test_images/image2.jpg'
                return 'test_images/image2.jpg'

        # Change the image when the user selects the image name
        rad1.change(action1, rad1, img1)

        # Output for the Highlighted text
        op = gr.Image(label="Colorized Image", shape=(300, 300))

        gr.Markdown(
            "### Made with ❤️ by Arsh using TrueFoundry's Gradio Deployment")
        gr.Markdown(
            "### [Github Repo](https://github.com/d4rk-lucif3r/Image-Colorizer-App)")
        gr.Markdown(
            '### [Blog]()')

        def fn(img1):  # Main function
            global filepath
            result = colorize(filepath)
            logging.info(f'CWD is {os.getcwd()}')
            logging.info(f'Result saved to {result}')
            logging.info(os.path.exists(result))
            return str(result)
        
        try:
            submit1.click(fn=fn, outputs=[
                      op], inputs=[img1])  # Submit button for the examples
        except Exception as e:
            logging.info('Error in submit1 ', e)
            pass
        # Submit button for the user input
        submit2.click(fn=fn, outputs=[op], inputs=[img1])
demo.queue()  # Queue the block
demo.launch(server_port=8080, server_name='0.0.0.0', show_error=True)  # Launch the gradio block
