from flask import Flask, request, jsonify
from lwcc import LWCC
# from flask_cors import CORS
import base64
import os
import random
import string


app = Flask(__name__)
# CORS(app) 
csrnet_model_a = LWCC.load_model(model_name = "CSRNet", model_weights="SHA")
bay_model_a = LWCC.load_model(model_name= "Bay", model_weights="SHA")
dmcount_model_a = LWCC.load_model(model_name= "DM-Count", model_weights="SHA")
csrnet_model_b = LWCC.load_model(model_name = "CSRNet", model_weights="SHB")
bay_model_b = LWCC.load_model(model_name= "Bay", model_weights="SHB")
dmcount_model_b = LWCC.load_model(model_name= "DM-Count", model_weights="SHB")
sfanet_model = LWCC.load_model(model_name= "SFANet", model_weights="SHB")

@app.route("/")
def home():
    return "Hello World!"

@app.route("/countingService", methods=['POST'])
def countingService():
    if 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400
    
    event_id = request.json['event_id']
    image_data = request.json['image']
    
    # Remove the base64 prefix if it exists
    if image_data.startswith('data:image/jpeg;base64,'):
        image_data = image_data.replace('data:image/jpeg;base64,', '')
    
    # Convert base64 to bytes
    image_bytes = base64.b64decode(image_data)
    
    # Generate a event directory and a random filename
    if not os.path.exists(event_id):
        os.makedirs(event_id)
    filename = event_id + '/' + generate_random_string(15) + '.jpg'
    
    # Write the image data to a file
    with open(filename, 'wb') as f:
        f.write(image_bytes)
    
    # Run algorithm (you would replace this with your actual image processing code)
    count = LWCC.get_count(filename, model = sfanet_model, resize_img = True)

    # For demonstration purposes, let's just print the filename
    print(f"Image processed: {filename}")
    
    return jsonify({'message': 'success', 'count': int(count)}), 200

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)