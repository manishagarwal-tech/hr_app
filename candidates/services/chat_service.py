import logging
from django.conf import settings
from langchain_core.messages import AIMessage, HumanMessage
from .llm_factory import LLMFactory
from .prompts import build_chat_prompt, CHAT_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.memory_turns = settings.CHAT_MEMORY_TURNS

    def process(self, user_question, chat_history=None, profile=None):
        if not user_question:
            return {"error": "No input provided."}

        system_prompt = self._build_system_prompt(profile)
        messages_history = self._build_messages_history(chat_history)

        prompt = build_chat_prompt()
        llm = LLMFactory.get_chat_model(settings.CHAT_MODEL_NAME, temperature=0)
        chain = prompt | llm
        response = chain.invoke({
            "system_prompt": system_prompt,
            "chat_history": messages_history,
            "human_input": user_question,
        })

        updated_history = (chat_history or []).copy()
        updated_history.append({"role": "human", "content": user_question})
        updated_history.append({"role": "ai", "content": response.content})
        updated_history = self._trim_history(updated_history)

        return {
            "system_prompt": system_prompt,
            "human": user_question,
            "ai": response.content,
            "chat_history": updated_history,
        }

    def _build_system_prompt(self, profile):
        if not profile:
            return CHAT_SYSTEM_PROMPT
        context = (
            "Candidate profile context: "
            f"Name: {profile.get('name', 'Unknown')}; "
            f"Primary skills: {', '.join(profile.get('primary_skills') or [])}; "
            f"Secondary skills: {', '.join(profile.get('secondary_skills') or [])}; "
            f"Experience: {profile.get('experience', 'Unknown')} years. "
            "Answer only using this profile context when applicable."
        )
        return f"{CHAT_SYSTEM_PROMPT} {context}"

    def _build_messages_history(self, chat_history):
        messages = []
        for item in chat_history or []:
            role = (item or {}).get("role")
            content = (item or {}).get("content")
            if not content:
                continue
            if role == "human":
                messages.append(HumanMessage(content=content))
            elif role == "ai":
                messages.append(AIMessage(content=content))
        return self._trim_messages(messages)

    def _trim_messages(self, messages):
        max_messages = self.memory_turns * 2
        if len(messages) > max_messages:
            return messages[-max_messages:]
        return messages

    def _trim_history(self, history):
        max_messages = self.memory_turns * 2
        if len(history) > max_messages:
            return history[-max_messages:]
        return history
