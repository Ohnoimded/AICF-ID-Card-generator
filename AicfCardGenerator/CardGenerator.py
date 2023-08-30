from PIL import Image, ImageDraw, ImageFont
import qrcode
import requests
import io

class CardGenerator:
    def generate_qr(self, url):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=4,
            border=1,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black")
        return qr_img

    def generate_card(self, profile_data):
        max_profile_width = 400  # Fixed width for the profile image

        # Import background template
        background = Image.open('static/images/template.png')

        # Import profile picture
        try:
            profile = requests.get(profile_data['Image']).content
            profile_image = Image.open(io.BytesIO(profile))
            # Resize profile image while maintaining aspect ratio and fixed width
            # width, height = profile_image.size
            new_height = int(max_profile_width / 0.95)
            profile_image = profile_image.resize((max_profile_width, new_height))
            # Most images are not png. That's why I added this exception handling
            try:
                background.paste(profile_image, (2100, 650), mask=profile_image)
            except:
                background.paste(profile_image, (2100, 650))
        except:
            profile_image=""


        # Make QR code
        qr_url = profile_data['url']
        qr_image = self.generate_qr(qr_url)
        qr_image = qr_image.resize((400, 400))

        # Add QR 
        background.paste(qr_image, (2100, 1450))

        # Fonts and textual data initialisation
        user_data_font = ImageFont.truetype(font='static/fonts/OpenSans-Semibold.ttf', size=65)
        draw = ImageDraw.Draw(background)

        # Add textual data
        text_y_start = 620 # Starting position in the y-axis for profile information
        for i in dict(list(profile_data.items())[4:]):
            draw.text((150, text_y_start), i, fill="black", font=user_data_font)
            draw.text((800, text_y_start), " : ", fill="black", font=user_data_font)
            draw.text((950, text_y_start), profile_data[i], fill="black", font=user_data_font)
            text_y_start += 160

        # AICF ID will be placed at the bottom
        draw.text((50, text_y_start - 40), profile_data['AICF ID'], fill="Red", font=ImageFont.truetype(font='static/fonts/OpenSans-Semibold.ttf', size=275))
        
        # Saving to buffer to avoid storage issues. Had issues here for the longest time. I'm dumb ¯\_( ͡° ͜ʖ ͡°)_/¯
        output_buffer=io.BytesIO() 
        background.save(output_buffer,dpi=(600, 600), format="PNG")
        output_buffer.seek(0)
        return output_buffer

card_generator=CardGenerator()
print(card_generator.generate_card({'url': 'https://prs.aicf.in/players/205997KL2023', 'Image': 'https://assets.aicf.in/contacts/large/6f73f8c3-c166-4861-97f1-cd822fe50b9a.png', 'AICF ID': '205997KL2023', 'FIDE ID': '', 'Name': 'Nived Krishna Prakash', 'Gender': 'M', 'Age': '23', 'State': 'Kerala', 'Registration Type': 'Player', 'Valid Upto': '2024-03-31'}))