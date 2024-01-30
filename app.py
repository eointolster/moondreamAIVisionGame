# pip install simplejson
# pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
#https://github.com/vikhyat/moondream
# fix
# https://github.com/vikhyat/moondream/issues/10?fbclid=IwAR0MkxjZR780_YmJtiq-F3w9Q6j0e9MioM6z0KwxO1C3I5_I7QWzqD1M6VE
from flask import Flask, render_template, request,session
import torch
import os
from PIL import Image
from moondream import VisionEncoder, TextModel, detect_device
from huggingface_hub import snapshot_download
# import gradio as gr
import jsonify
import random
from flask import Flask, render_template, request, jsonify, send_from_directory
import os

app = Flask(__name__)

model_path = snapshot_download("vikhyatk/moondream1")
vision_encoder = VisionEncoder(model_path).to("cuda" if torch.cuda.is_available() else "cpu")
text_model = TextModel(model_path).to("cuda" if torch.cuda.is_available() else "cpu")

def moondream(img, prompt):
    image = Image.fromarray(img)
    image_embeds = vision_encoder(image)
    response = text_model.answer_question(image_embeds, "describe this picture")
    return response

# iface = gr.Interface(fn=moondream, inputs="image", outputs="text")
# iface.launch(share=True)

assets_folder = os.path.join(app.root_path, 'static/images')

# Route to serve images
@app.route('/static/images/<path:filename>')
def serve_static(filename):
    return send_from_directory('static/images', filename)

@app.route('/')
def index():
    # return "Hello, this is the index page!"
    # return render_template('index.html', images=available_images)
    return render_template('index.html')

# Route to get available images
@app.route('/get_images')
def get_images():
    # Get a list of available images in the "assets" folder
    assets_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    available_images = [f for f in os.listdir(assets_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return jsonify(available_images)

@app.route('/predict_random', methods=['GET'])
def predict_random():
    available_images = [f for f in os.listdir(assets_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    # Select a random image from the available images
    random_filename = random.choice(available_images)
    image_path = os.path.join(assets_folder, random_filename)
    image = Image.open(image_path)

    # Process the image as before
    image_embeds = vision_encoder(image)
    prediction = text_model.answer_question(image_embeds, "describe this picture")
    
    return jsonify({'prediction': prediction, 'filename': random_filename})


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return redirect('/')
    
    image_file = request.files['image']
    if image_file.filename == '':
        return redirect('/')
    
    # Process the image
    image = Image.open(image_file)
    image_embeds = vision_encoder(image)
    prediction = text_model.answer_question(image_embeds, "describe this picture")
    
    # return render_template('index.html', images=available_images, prediction=prediction)
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
