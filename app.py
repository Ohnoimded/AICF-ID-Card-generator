from flask import Flask, render_template, Response, send_file, request, flash,redirect,url_for
from AicfCardGenerator.ProfileScraper import ProfileScraper
from AicfCardGenerator.CardGenerator import CardGenerator
import os

# class AICFRegistrationError(Exception):
#     pass

app = Flask(__name__)


# disable caching
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

global message_attr

@app.route('/')
def index():
    message_attr = "none"
    return render_template('index.html', message_attr=message_attr)

@app.route('/download', methods=['POST'])
def download_output_image():
    aicf_id = request.form['aicf_id']
    try:
        profile = ProfileScraper().scrape_profile(aicf_id)
        card = CardGenerator().generate_card(profile)
        return send_file(card, download_name="AICF_ID_CARD_{}.png".format(aicf_id), as_attachment=True)
    except:
        message_attr = 'failure'
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
