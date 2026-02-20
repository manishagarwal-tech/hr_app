from langchain_groq import ChatGroq
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import os
import logging
logger = logging.getLogger(__name__)


class ChatLLM:
    def __init__(self):
        # Initialize the ChatGroq model
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name=os.getenv("CHAT_MODEL_NAME")
        )
        # Keep a short rolling window of messages (per session/request)
        self.conversational_memory_length = 5

    def process_text(self, user_question, chat_history=None):
        system_prompt = (
            "You are a knowledgeable and helpful AI assistant. "
            "Provide clear, direct, and concise answers. "
            "Avoid unnecessary details or lengthy explanations. "
            "Respond in 2–4 sentences maximum unless the user explicitly asks for more detail. "
            "If the user asks a question related to code generation, format your response inside Markdown-style code blocks "
            "so it can be rendered within a <pre><code> container on the frontend."
        )
        if not user_question:
            return {"error": "No input provided."}

        # Convert stored history (list[dict]) to LangChain messages
        messages_history = []
        if chat_history:
            for item in chat_history:
                role = (item or {}).get("role")
                content = (item or {}).get("content")
                if not content:
                    continue
                if role == "human":
                    messages_history.append(HumanMessage(content=content))
                elif role == "ai":
                    messages_history.append(AIMessage(content=content))

        # Trim to last N turns (human+ai => 2 messages per turn)
        max_messages = self.conversational_memory_length * 2
        if len(messages_history) > max_messages:
            messages_history = messages_history[-max_messages:]

        # Construct prompt
        prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ])

        # Modern pipeline (RunnableSequence)
        chain = prompt | self.llm
        logger.info(f"getting chain -> {chain}")
        response = chain.invoke({
            "chat_history": messages_history,
            "human_input": user_question
        })

        # Return updated history for persistence (e.g., Django session)
        updated_history = (chat_history or []).copy()
        updated_history.append({"role": "human", "content": user_question})
        updated_history.append({"role": "ai", "content": response.content})
        if len(updated_history) > max_messages:
            updated_history = updated_history[-max_messages:]

        return {
            "system_prompt": system_prompt,
            "human": user_question,
            "ai": response.content,
            "chat_history": updated_history,
        }