import json
import requests


def fetch_data(request, database):
    try:
        params = {'request': request, 'database': database}
        response = requests.get('http://localhost:3000/admin/get', params=params)
        return json.loads(response.text)
    except json.decoder.JSONDecodeError:
        print("Error 404")


def post_data(request, database, data):
    try :
        data = {'request': request, 'database': database, 'data': data}
        response = requests.post('http://localhost:3000/admin/post', json=data)
    except json.decoder.JSONDecodeError:
        print("Error 404")


def node(update, context):
    chat_id = update.message.chat.id

    data = fetch_data(request="ALL", database="waypoints")

    data_text = "<code>-----------------------------</code>\n" \
                "<code>   Node.js Waypoints Data    </code>\n" \
                "<code>-----------------------------</code>\n" \
                "<code>  Name   :    (Lat, Long)    </code>\n" \
                "<code>-----------------------------</code>\n"

    for datum in data:
        name = datum["Name"]
        latitude = datum["Latitude"]
        longitude = datum["Longitude"]

        data_text += f"<code>{name:<8} : ({latitude:.4f}, {longitude:.4f})</code>\n"

    context.bot.send_message(text=data_text, chat_id=chat_id, parse_mode="HTML")