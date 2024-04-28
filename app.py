from flask import Flask, request, jsonify
from lwcc import LWCC
import base64
import os
import random
import string

app = Flask(__name__)
dmcount_model_a = LWCC.load_model(model_name= "DM-Count", model_weights="SHA")
dmcount_model_b = LWCC.load_model(model_name= "DM-Count", model_weights="SHB")
#csrnet_model_a = LWCC.load_model(model_name = "CSRNet", model_weights="SHA")
#bay_model_a = LWCC.load_model(model_name= "Bay", model_weights="SHA")
#csrnet_model_b = LWCC.load_model(model_name = "CSRNet", model_weights="SHB")
#bay_model_b = LWCC.load_model(model_name= "Bay", model_weights="SHB")
#sfanet_model = LWCC.load_model(model_name= "SFANet", model_weights="SHB")

'''
Dummy route
'''
@app.route("/")
def home():
    return "Hello World!"

'''
Counts the number of people in an image.

Also, performs image conversion from base64 and storage for the use in ML model.

@return {number} number of people in an image.
'''
@app.route("/countingService", methods=['POST'])
def countingService():
    if 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400
    
    event_id = request.json['event_id']
    image_data = request.json['image']
    modelToUse = request.json['model']
    
    # Decode the image
    image_type = ''
    if image_data.startswith('data:image/jpeg;base64,'):
        image_data = image_data.replace('data:image/jpeg;base64,', '')
        image_type = 'jpg'
    elif image_data.startswith('data:image/png;base64,'):
        image_data = image_data.replace('data:image/png;base64,', '')
        image_type = 'png'
    image_bytes = base64.b64decode(image_data)
    
    # Store the image
    if not os.path.exists(event_id):
        os.makedirs(event_id)
    filename = ''
    if image_type == 'jpg':
        filename = event_id + '/' + generate_random_string(15) + '.jpg'
    elif image_type == 'png':
        filename = event_id + '/' + generate_random_string(15) + '.png'
    with open(filename, 'wb') as f:
        f.write(image_bytes)
    
    # Model selection and counting
    if modelToUse == 'dense':
        modelToUse = dmcount_model_a
    elif modelToUse == 'sparse':
        modelToUse = dmcount_model_b
    count = LWCC.get_count(filename, model = modelToUse)

    print(f"Image processed: {filename}")
    
    return jsonify({'message': 'success', 'count': int(count)}), 200

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

if __name__ == "__main__":
    app.run(debug=True, threaded=True)