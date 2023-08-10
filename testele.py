# import telegram

# # Token bot Telegram Anda
# bot_token = '6318000053:AAHq9JdNN2s190po_6zHPuveM87K23ZIzkI'

# # ID obrolan (chat) tempat Anda ingin mengirim pesan notifikasi
# chat_id = 'MyDeviceNotif'

# # Pesan notifikasi yang ingin Anda kirim
# notification_message = 'Ini adalah pesan notifikasi.'

# def send_notification(token, chat_id, message):
#     bot = telegram.Bot(token=token)
#     bot.send_message(chat_id=chat_id, text=message)

# send_notification(bot_token, chat_id, notification_message)

import requests

x = requests.get('https://api.telegram.org/bot6318000053:AAHq9JdNN2s190po_6zHPuveM87K23ZIzkI/sendMessage?chat_id=1350618150&text=tesDuluBRO')


print(x.text)