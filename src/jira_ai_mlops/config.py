import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class JiraConfig:
    server_url: str
    email: str
    api_token: str
    project_key: str


def get_config() -> JiraConfig:
    load_dotenv()
    return JiraConfig(
        server_url=os.getenv("JIRA_SERVER_URL", "").strip(),
        email=os.getenv("JIRA_EMAIL", "").strip(),
        api_token=os.getenv("JIRA_API_TOKEN", "").strip(),
        project_key=os.getenv("JIRA_PROJECT_KEY", "").strip(),
    )


def validate_config(config: JiraConfig) -> None:
    missing = []
    if not config.server_url:
        missing.append("JIRA_SERVER_URL")
    if not config.email:
        missing.append("JIRA_EMAIL")
    if not config.api_token:
        missing.append("JIRA_API_TOKEN")
    if not config.project_key:
        missing.append("JIRA_PROJECT_KEY")

    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}"
        )
