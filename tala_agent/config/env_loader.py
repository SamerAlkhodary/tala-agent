import logging
import os
import sys

from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def _load_env_variables():
    load_dotenv()


def _get_env_variable(env_name: str, var_type=str, default=None, required=False):
    label = "env_loader/get_env_variable"
    val = os.getenv(env_name)
    # env variable not set
    if val is None:
        # env variable not set but required
        if required:
            # default is not set: error
            if default is None:
                logger.error(
                    msg=f"Required env variable not set {env_name}",
                    extra={"label": label},
                )
                sys.exit(1)
            else:
                # default is set but type is not correct: error
                if not isinstance(default, var_type):
                    logger.error(
                        msg=f"Default env value {default} expected of type {var_type} but found of {default.__class__.__name__}",
                        extra={"label": label},
                    )
                    sys.exit(1)
        return default

    # If the env variable is set, handle conversion based on `var_type`
    result = default
    try:
        if var_type is str:
            result = val
        elif var_type is int:
            result = int(val)
        elif var_type is float:
            result = float(val)
        elif var_type is bool:
            # Convert to boolean using a standard approach
            result = val.lower() in ("true", "1", "t", "y", "yes")
        else:
            logger.error(
                msg=f"Unsupported type '{var_type}' for env variable '{env_name}'.",
                extra={"label": label},
            )
            sys.exit(1)
    except ValueError as e:
        logger.error(
            msg=f"Error converting env variable '{env_name}' to {var_type.__name__}. Using default value: {default}",
            extra={"label": label, "error": str(e)},
        )
    except Exception as e:
        logger.error(
            msg=f"Unexpected error reading env variable '{env_name}'",
            extra={"label": label, "error": str(e)},
        )
        sys.exit(1)
    return result
