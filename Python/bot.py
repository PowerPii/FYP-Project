from credentials import API_KEY
from telegram.ext import *

import backend, job

import buses as buses
import risks as risks
import sql as _sql
import php as _php
import node as _node


def start(update, context):
    chat_id = update.message.chat.id
    username = update.message.from_user.username

    start_text = f"<code>Hi {username}! Welcome to MooVita Bot</code>"

    context.bot.send_message(text=start_text, chat_id=chat_id, parse_mode="HTML")


def error(update, context):
    print(f"Update {update} caused error.\n {context.error}")


def telegram_setup():
    print("Bot started...")

    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    dp.add_handler(CommandHandler("info", backend.info))
    dp.add_handler(CommandHandler("ping", backend.ping))

    dp.add_handler(CommandHandler("sql", _sql.sql))
    dp.add_handler(CommandHandler("php", _php.php))
    dp.add_handler(CommandHandler("node", _node.node))

    dp.add_handler(CommandHandler("bus", buses.buses))
    dp.add_handler(CommandHandler("risk", risks.risks))

    dp.add_error_handler(error)

    jq = JobQueue()
    jq.set_dispatcher(dp)

    jq.run_repeating(callback=job.heartbeat, interval=60)
    jq.run_repeating(callback=buses.update_bus, interval=60)
    jq.run_repeating(callback=risks.update_risk, interval=5)

    jq.start()

    updater.start_polling()
    updater.idle()
