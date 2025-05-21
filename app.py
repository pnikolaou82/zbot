from flask import Flask, request, Response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    BotFrameworkAdapter,
    TurnContext,
)
from botbuilder.schema import Activity
from config import DefaultConfig
from bot import EchoBot
import asyncio

app = Flask(__name__)

CONFIG = DefaultConfig()
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)
BOT = EchoBot()

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers.get("Content-Type", ""):
        json_message = request.json
    else:
        return Response(status=415)

    activity = Activity().deserialize(json_message)
    auth_header = request.headers.get("Authorization", "")

    async def call_bot():
        await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)

    try:
        asyncio.run(call_bot())
        return Response(status=200)
    except Exception as e:
        print(f"Exception: {e}")
        return Response(status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

