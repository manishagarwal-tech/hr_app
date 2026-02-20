import importlib
import logging
import os
from django.conf import settings

logger = logging.getLogger(__name__)


def load_adk_agent_class():
    import_path = getattr(settings, "GOOGLE_ADK_AGENT_CLASS", os.getenv("GOOGLE_ADK_AGENT_CLASS", ""))
    if not import_path:
        return None
    try:
        module_path, class_name = import_path.rsplit(":", 1)
    except ValueError:
        logger.warning("Invalid GOOGLE_ADK_AGENT_CLASS format. Use module:ClassName")
        return None
    try:
        module = importlib.import_module(module_path)
    except ImportError:
        logger.warning("Unable to import ADK module: %s", module_path)
        return None
    return getattr(module, class_name, None)
