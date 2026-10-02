import logging

import boto3
import watchtower


LOG_GROUP = "/ai-support-specialist-lab/application"
AWS_REGION = "eu-central-1"


def configure_logger():
    logger = logging.getLogger("ai-support-lab")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))

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

    logger.addHandler(console_handler)
    logger.addHandler(cloudwatch_handler)

    return logger