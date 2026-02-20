from .base import BaseAgent
from candidates.services.chat_service import ChatService


class ChatAgent(BaseAgent):
    def __init__(self):
        super().__init__("chat")
        self.chat = ChatService()

    def run(self, context):
        response = self.chat.process(
            context["user_question"],
            chat_history=context.get("chat_history"),
            profile=context.get("profile"),
        )
        context["chat_response"] = response
        return context
