from {{template_agent}}.config.config_handler import _AgentConfig
from {{template_agent}}.config.env_loader import (
    _load_env_variables,
)

_load_env_variables()

agent_config = _AgentConfig()
__all__ = [
    "agent_config",
]
