import json
import time
import requests
import base64
from PIL import Image
from io import BytesIO
import telebot
import os

class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']
            attempts -= 1
            time.sleep(delay)

    def decode_base64(self, base64_string, img_name):
        decoded_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(decoded_data))
        image.save(os.path.join('images', img_name))


api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '5A80D4969512A685021A8D044F228AB7', '685B956365CD051B2714A6D1B0B52E6D')
model_id = api.get_model()


if not os.path.exists('images'):
    os.makedirs('images')


bot = telebot.TeleBot("")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет Напишите мне и я сгенерирую для вас изображение.")

@bot.message_handler(func=lambda message: True)
def generate_image(message):
    chat_id = message.chat.id
    text = message.text

    # Simulate typing
    bot.send_chat_action(chat_id, 'typing')


    uuid = api.generate(text, model_id)
    images = api.check_generation(uuid)[0]
    api.decode_base64(images, "123.jpg")
    photo = open(os.path.join('images', "123.jpg"), "rb")
    bot.send_photo(chat_id, photo)

    # Delete the image after sending
    os.remove(os.path.join('images', "123.jpg"))


bot.polling()
