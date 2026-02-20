from .adk_adapter import load_adk_agent_class


class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.adk_agent_class = load_adk_agent_class()

    def run(self, context):
        raise NotImplementedError("Agent must implement run().")
