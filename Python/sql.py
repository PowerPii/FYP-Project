import mysql.connector

from credentials import HOST, USER, PASSWORD, DATABASE, PORT

server_url = 'http://localhost:3000'


def fetch_data():
    try:
        db = mysql.connector.connect(host=HOST, user=USER, password=PASSWORD, database=DATABASE, port=PORT)
        cursor = db.cursor()
        cursor.execute('SELECT * FROM application.waypoints')
        return cursor.fetchall()
    except:
        return None


def sql(update, context):
    chat_id = update.message.chat.id

    data = fetch_data()

    data_text = "<code>-----------------------------</code>\n" \
                "<code>    MySQL Waypoints Data     </code>\n" \
                "<code>-----------------------------</code>\n" \
                "<code>  Name   :    (Lat, Long)    </code>\n" \
                "<code>-----------------------------</code>\n"

    for datum in data:
        name = list(datum)[0]
        latitude = list(datum)[1]
        longitude = list(datum)[2]

        data_text += f"<code>{name:<8} : ({latitude:.4f}, {longitude:.4f})</code>\n"

    context.bot.send_message(text=data_text, chat_id=chat_id, parse_mode="HTML")






