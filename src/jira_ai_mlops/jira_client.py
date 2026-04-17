from jira import JIRA

from .config import JiraConfig


def build_client(config: JiraConfig) -> JIRA:
    return JIRA(server=config.server_url, basic_auth=(config.email, config.api_token))
