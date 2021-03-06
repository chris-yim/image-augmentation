import io

import requests
from flask import Flask, request, render_template
from PIL import Image

# Imports for augmenting the input image from the URL
from image_augmentations import random_augmentation

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# 4MB Max image size limit
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024


# Default route to handle showing the default, URL and error pages
@app.route('/', methods=['GET'])
def index():
    image_url = request.args.get('url')
    if not image_url:
        return render_template("index.html")
    try:
        image_response = requests.get(image_url)
        image = Image.open(io.BytesIO(image_response.content))
        augmented_image = random_augmentation(image)
        augmented_image.convert('RGB').save("static/augmented_image.jpg")
        return render_template("image_augment.html")
    except Exception as message:
        return render_template("error_handling.html", message=message)


if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=8000, debug=True)
