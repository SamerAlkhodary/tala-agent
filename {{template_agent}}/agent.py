from contextual_agents_sdk.hydrator import Hydrator

from {{template_agent}}.config import agent_config
from {{template_agent}}.tools import greater_tool


def get_analytics(checkpointer=None):
    hydrator = Hydrator.create(
        swarm_file=agent_config.SWARM_FILE_PATH,
        local_tools=[greater_tool],
        checkpointer=checkpointer,
    )
    hive = hydrator.build()
    return hive.get_graph()
