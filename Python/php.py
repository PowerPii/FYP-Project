import pandas as pd
import json

def fetch_data():
    try:
        waypoints_data = pd.read_html("http://localhost:8080/server.php")[0]
        return json.loads(waypoints_data.to_json(orient="records"))
    except:
        return None


def php(update, context):
    chat_id = update.message.chat.id

    data = fetch_data()

    data_text = "<code>-----------------------------</code>\n" \
                "<code>     PHP Waypoints Data      </code>\n" \
                "<code>-----------------------------</code>\n" \
                "<code>  Name   :    (Lat, Long)    </code>\n" \
                "<code>-----------------------------</code>\n"

    for datum in data:
        name = datum["Name"]
        latitude = float(datum["Latitude"])
        longitude = float(datum["Longitude"])

        data_text += f"<code>{name:<8} : ({latitude:.4f}, {longitude:.4f})</code>\n"

    context.bot.send_message(text=data_text, chat_id=chat_id, parse_mode="HTML")



