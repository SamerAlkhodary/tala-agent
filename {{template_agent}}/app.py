from typing import Final

import dotenv
import uvicorn
from agent_sdk.application import ServiceConfig, setup_service
from agent_sdk.context.extract_context import get_jwt
from agent_sdk.messaging.tenant_purge import create_tenant_purge_handler
from langchain_qlik.jwt import set_jwt_fetcher

from {{template_agent}}.agent import get_analytics

SERVICE_NAME: Final = "{{template-agent}}"
EVENT_SUBJECT: Final = "system-events.{{template-agent}}"
EVENT_SOURCE: Final = "com.qlik/{{template-agent}}"

dotenv.load_dotenv()


def main():
    """
    The side car is disabled in build env but we still need the database name
    to enable persistence
    """

    config = ServiceConfig(
        prefix="/v1/{{template-agent}}",
        service_name=SERVICE_NAME,
        database_name=SERVICE_NAME,
        is_remote_agent=True,
        feature_name=["CLOUD_ASSISTANT"],
        handle_tenant_purge=create_tenant_purge_handler(
            subject=EVENT_SUBJECT,
            source=EVENT_SOURCE,
            context=SERVICE_NAME,
            resource_type=SERVICE_NAME,
            event_handler=None,
        ),
    )
    set_jwt_fetcher(jwt_fetcher=get_jwt)
    app = setup_service(config, get_analytics)

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
