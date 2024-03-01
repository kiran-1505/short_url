from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import random
import string

app = Flask(__name__)

def load_urls():
    """Load URL mappings from JSON file."""
    if os.path.exists('urls.json'):
        with open('urls.json', 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # Handle the case where the JSON file is invalid or empty
                return {}
    else:
        return {}

def save_urls(urls):
    """Save URL mappings to JSON file."""
    try:
        with open('urls.json', 'w') as file:
            json.dump(urls, file)
    except Exception as e:
        # Handle the case where writing to the JSON file fails
        print(f"Error saving URLs to JSON file: {e}")

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('url')
    urls = load_urls()

    if long_url in urls:
        short_url = urls[long_url]
    else:
        short_url = generate_short_url()
        urls[long_url] = short_url
        save_urls(urls)

    return render_template('shorturl.html', short_url_display=short_url)

@app.route('/display/<short_url>')
def display_short_url(short_url):
    return render_template('shorturl.html', short_url_display=short_url)

def generate_short_url():
    """Generate a random short URL with 'https://' prefix."""
    short_url_length = 8
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(short_url_length))
    return f'https://{short_url}'

if __name__ == '__main__':
    app.run(port=5000, debug=True)