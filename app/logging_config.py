import logging
import os

import boto3
import watchtower


LOG_GROUP = "/ai-support-specialist-lab/application"
AWS_REGION = "eu-central-1"


def configure_logger():
    logger = logging.getLogger("ai-support-lab")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return logger

    # Console logging is always available
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console_handler)

    cloudwatch_enabled = (
        os.getenv("ENABLE_CLOUDWATCH_LOGGING", "false").lower() == "true"
    )

    if not cloudwatch_enabled:
        logger.info(
            '{"event":"cloudwatch_disabled","logging":"console_only"}'
        )
        return logger

    try:
        cloudwatch_client = boto3.client(
            "logs",
            region_name=AWS_REGION
        )

        cloudwatch_handler = watchtower.CloudWatchLogHandler(
            log_group_name=LOG_GROUP,
            stream_name="local-development",
            boto3_client=cloudwatch_client,
            create_log_group=False
        )

        cloudwatch_handler.setFormatter(
            logging.Formatter("%(message)s")
        )

        logger.addHandler(cloudwatch_handler)

        logger.info(
            '{"event":"cloudwatch_enabled","logging":"console_and_cloudwatch"}'
        )

    except Exception as error:
        logger.warning(
            '{"event":"cloudwatch_unavailable",'
            f'"error_type":"{type(error).__name__}",'
            '"logging":"console_only"}'
        )

    return logger
