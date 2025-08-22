import os
from aiohttp import web
from botbuilder.core import TurnContext, CloudAdapter
from botbuilder.core.integration import ConfigurationBotFrameworkAuthentication
from botbuilder.schema import Activity
from bot_logic import EchoBot

# Credenciais vindas das App Settings do App Service
APP_ID = os.getenv("MicrosoftAppId")
APP_PASSWORD = os.getenv("MicrosoftAppPassword")

# Autenticação recomendada para canais (Teams)
bot_auth = ConfigurationBotFrameworkAuthentication(
    microsoft_app_id=APP_ID,
    microsoft_app_password=APP_PASSWORD,
    # Os demais argumentos podem ficar None para o padrão (SingleTenant está OK)
    # Veja: https://github.com/microsoft/botbuilder-python
)

adapter = CloudAdapter(bot_auth)
bot = EchoBot()

async def messages(request: web.Request) -> web.Response:
    try:
        body = await request.json()
    except Exception:
        return web.Response(status=400, text="invalid json")

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    async def logic(turn_context: TurnContext):
        await bot.on_turn(turn_context)

    try:
        await adapter.process_activity(auth_header, activity, logic)
        return web.Response(text="OK", status=201)
    except Exception as e:
        # log simples
        print(f"[ERROR] process_activity: {e}")
        return web.Response(text="ERR", status=500)

app = web.Application()
app.router.add_post("/api/messages", messages)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
