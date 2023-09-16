import requests
import io
import cv2
# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = '6553866779:AAHJzhYrKV5rhXePN_wupU23YKUxGvND_-U'

# Replace 'CHAT_ID' with the chat ID of the user or group
chat_id = '5559085957'

# URL for sending messages with images
url = f'https://api.telegram.org/bot{bot_token}/sendPhoto'

def send_img_telegram(img):
        _, img_encoded = cv2.imencode('.jpg', img)
        img_io = io.BytesIO(img_encoded)
        img_io = io.BytesIO(img_encoded)
        files = {'photo': img_io}
        data = {'chat_id': chat_id}

        # Send the image
        response = requests.post(url, data=data, files=files)


        
