from credentials import admin_id

import sql as _sql
import php as _php
import node as _node

from risks import Risk
from buses import Bus


def get_status():
    mysql_status = True if _sql.fetch_data() else False
    php_status = True if _php.fetch_data() else False
    node_js_status = True if _node.fetch_data() else False

    return mysql_status, php_status, node_js_status


def heartbeat(context):
    mysql_status, php_status, node_js_status = get_status()

    heartbeat_text = "<code>-----------------------------</code>\n" \
                     "<code>       Hearbeat Update       </code>\n" \
                     "<code>-----------------------------</code>\n" 

    heartbeat_text += "<code>MySQL   : Online</code>\n" if mysql_status else  "<code>MySQL   : Offline</code>\n" 
    heartbeat_text += "<code>PHP     : Online</code>\n" if php_status else  "<code>PHP     : Offline</code>\n" 
    heartbeat_text += "<code>Node.js : Online</code>\n" if node_js_status else "<code>Node.js : Offline</code>\n"  

    context.bot.send_message(text=heartbeat_text, chat_id=admin_id, parse_mode="HTML")


def update_risk(context):
    risk = Risk()
    risk.update_database()

def update_bus(context):
    bus = Bus()
    bus.update_database()
