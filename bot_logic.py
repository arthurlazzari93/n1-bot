from botbuilder.core import ActivityHandler, TurnContext
from botbuilder.schema import ChannelAccount

class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                await turn_context.send_activity(
                    "Olá! 👋 Sou o N1 Suporte. Me envie uma mensagem para eu responder."
                )

    async def on_message_activity(self, turn_context: TurnContext):
        text = turn_context.activity.text or ""
        await turn_context.send_activity(
            f"Recebi sua mensagem: **{text}**\n\nEstou online e funcionando ✅"
        )
