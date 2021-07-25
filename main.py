from flask import Flask, render_template, request
from colorthief import ColorThief
from urllib.request import urlopen
from flask_cache_buster import CacheBuster
from colormap import rgb2hex
import io
import os


# App configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)


# Use of flask_cache_buster to update CSS files
config = {
     'extensions': ['.js', '.css', '.csv'],
     'hash_size': 10
}
cache_buster = CacheBuster(config=config)
cache_buster.register_cache_buster(app)


# Main page
@app.route('/', methods=['GET', 'POST'])
def colorpicker():
    if request.method == "POST":
        image = request.form['image_url']
        fd = urlopen(image)
        f = io.BytesIO(fd.read())
        color_thief = ColorThief(f)
        dominant = color_thief.get_color(quality=100)
        dominant_hex = rgb2hex(dominant[0], dominant[1], dominant[2])
        palette = color_thief.get_palette(quality=100)
        palette_hex = []
        for i in palette:
            color = rgb2hex(i[0], i[1], i[2])
            palette_hex.append(color)
        return render_template('index.html', dominant=dominant, palette=palette, image=image, dominant_hex=dominant_hex, palette_hex=palette_hex)
    return render_template('index.html', dominant="", palette="", image="", dominant_hex="", palette_hex="")


# Run app
if __name__ == "__main__":
    app.run(debug=True)
