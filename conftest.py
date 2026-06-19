import sys
from unittest.mock import MagicMock

# Stub out agno and APScheduler before any test module imports them.
# agno: avoids needing an OpenAI key for module-level Agent instantiation.
# apscheduler: prevents real background threads from spinning up during tests.
for mod in (
    "agno", "agno.agent", "agno.models", "agno.models.openai",
    "apscheduler", "apscheduler.schedulers", "apscheduler.schedulers.background",
):
    sys.modules.setdefault(mod, MagicMock())
