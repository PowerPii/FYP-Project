import psutil
from ping3 import ping

 
def info(update, context):
    chat_id = update.message.chat.id

    rom_used = psutil.disk_usage('/').used / (1024 ** 3)
    total_rom = psutil.disk_usage('/').total / (1024 ** 3)
    rom_percentage = rom_used / total_rom * 100

    ram_used = psutil.virtual_memory().used / (1024 ** 3)
    total_ram = psutil.virtual_memory().total / (1024 ** 3)
    ram_percentage = ram_used / total_ram * 100

    info_text = "<code>-----------------------------</code>\n" \
                "<code>    Backend Information      </code>\n" \
                "<code>-----------------------------</code>\n" \
                f"<code>ROM : {rom_used:.1f}/{total_rom:.1f} GB ({rom_percentage:.1f}%)</code>\n" \
                f"<code>RAM : {ram_used:.1f}/{total_ram:.1f} GB ({ram_percentage:.1f}%)</code>\n"

    context.bot.send_message(text=info_text, chat_id=chat_id, parse_mode="HTML")


def pings(update, context):
    chat_id = update.message.chat.id

    ping_location = "127.0.0.1"
    ping_delay = ping(ping_location) * 1000

    ping_text = "<code>-----------------------------</code>\n" \
                "<code>      Ping Information       </code>\n" \
                "<code>-----------------------------</code>\n" \
                f"<code>Ping Location : {ping_location}</code>\n" \
                f"<code>Timing        : {ping_delay:.2f} ms </code>\n"

    context.bot.send_message(text=ping_text, chat_id=chat_id, parse_mode="HTML")











