from langchain_groq import ChatGroq
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
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
        self.conversational_memory_length = 5
        self.memory = ConversationBufferWindowMemory(k=self.conversational_memory_length, memory_key="chat_history",
                                                return_messages=True)

    def process_text(self, user_question):
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
            "chat_history": self.memory.chat_memory.messages,
            "human_input": user_question
        })

        # Save to memory if needed
        self.memory.chat_memory.add_user_message(user_question)
        self.memory.chat_memory.add_ai_message(response.content)

        return {
            "system_prompt": system_prompt,
            "human": user_question,
            "ai": response.content
        }