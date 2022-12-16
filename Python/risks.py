from datetime import datetime
import random
import json

from node import fetch_data, post_data

class Risk:
    def __init__(self):
        self.date = str(datetime.now().date())
        self.time = str(datetime.now().time().replace(microsecond=0))
        self.risks = {"Blk 51": random.randint(1, 3), 
                      "Blk 72": random.randint(1, 3),
                      "Blk 73": random.randint(1, 3),
                      "Blk 23": random.randint(1, 3),
                      "Blk 8" : random.randint(1, 3),
                      "SIT"   : random.randint(1, 3)}

    def update_database(self):
        data = {"date": self.date, "time": self.time, "risks": self.risks}
        post_data(request="APPEND", database="risks", data=data)


def get_risks():
    data = fetch_data(request="ALL", database="risks")[-1]

    date = data["Date"]
    time = data["Time"]
    risks = json.loads(data["Risks"].replace("'", "\""))

    return date, time, risks


def update_risk(context):
    risk = Risk()
    risk.update_database()


def risks(update, context):
    chat_id = update.message.chat.id

    date, time, risks = get_risks()

    risk_text = "<code>------------------------------</code>\n" \
                "<code>        Risk Database         </code>\n" \
                "<code>------------------------------</code>\n" \
                f"<code>     {date} {time}           </code>\n" \
                "<code>------------------------------</code>\n" \
                f'<code> Blk 51      : {risks["Blk 51"]:>8}</code>\n' \
                f'<code> Blk 72      : {risks["Blk 72"]:>8}</code>\n' \
                f'<code> Blk 73      : {risks["Blk 73"]:>8}</code>\n' \
                f'<code> Blk 23      : {risks["Blk 23"]:>8}</code>\n' \
                f'<code> Blk 8       : {risks["Blk 8"]:>8}</code>\n' \
                f'<code> SIT         : {risks["SIT"]:>8}</code>\n' 


    context.bot.send_message(text=risk_text, chat_id=chat_id, parse_mode="HTML")





    



