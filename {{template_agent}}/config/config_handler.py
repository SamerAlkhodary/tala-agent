from {{template_agent}}.config.env_loader import (
    _get_env_variable,
)


class _AgentConfig:
    SERVICE_NAME = _get_env_variable(
        env_name="AGENT_SERVICE_NAME",
        var_type=str,
        default="{{template-agent}}",
        required=False,
    )
    SWARM_FILE_PATH = _get_env_variable(
        env_name="AGENT_SWARM_FILE_PATH",
        var_type=str,
        default="./swarm_configs/swarm.yaml",
        required=False,
    )
