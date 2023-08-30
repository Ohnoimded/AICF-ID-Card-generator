from flask import Flask, render_template, Response, request, flash, redirect, url_for
from AicfCardGenerator.ProfileScraper import ProfileScraper
from AicfCardGenerator.CardGenerator import CardGenerator

app = Flask(__name__)

# Disable caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.errorhandler(500)
def internal_error(error):
    error_message = "Failed to generate ID card for the given AICF ID. Please check your AICF ID and try again."
    return render_template('error.html', error_message=error_message)

@app.errorhandler(404)
def not_found(error):
    error_message = "The requested page was not found."
    return render_template('error.html', error_message=error_message)

@app.route('/')
def index():
    message_attr = "none"
    return render_template('index.html', message_attr=message_attr)

@app.route('/open_image', methods=['POST'])
def open_image():
    aicf_id = request.form['aicf_id']
    return redirect(url_for('download', aicf_id=aicf_id))

@app.route('/download/<aicf_id>')
def download(aicf_id):
    profile = ProfileScraper().scrape_profile(aicf_id)
    card = CardGenerator().generate_card(profile)
    response = Response(card, content_type='image/png')
    response.headers['Content-Disposition'] = 'inline; filename=image.png'
    return response

if __name__ == "__main__":
    app.run(debug=True)
