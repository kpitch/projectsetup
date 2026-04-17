import json

import click

from src.jira_ai_mlops.config import get_config, validate_config
from src.jira_ai_mlops.jira_client import build_client
from src.jira_ai_mlops.ticket_service import (
    create_ticket,
    get_ticket_status,
    transition_ticket,
)


def _build_ready_client():
    config = get_config()
    validate_config(config)
    client = build_client(config)
    return client, config


@click.group()
def cli():
    """Jira Python SDK + AI/MLOps automation CLI."""


@cli.command("create-ticket")
@click.option("--summary", required=True, help="Ticket summary/title")
@click.option("--description", required=True, help="Ticket description/body")
@click.option("--issue-type", default="Task", show_default=True, help="Issue type")
@click.option(
    "--labels",
    default="",
    help="Comma-separated labels (example: mlops,prod,urgent)",
)
def create_ticket_cmd(summary: str, description: str, issue_type: str, labels: str):
    """Create a Jira ticket with basic MLOps scoring."""
    client, config = _build_ready_client()
    labels_list = [x.strip() for x in labels.split(",") if x.strip()]
    result = create_ticket(
        client=client,
        project_key=config.project_key,
        summary=summary,
        description=description,
        issue_type=issue_type,
        labels=labels_list,
    )
    click.echo(json.dumps(result, indent=2))


@cli.command("check-status")
@click.option("--ticket-key", required=True, help="Ticket key, e.g. ENG-123")
def check_status_cmd(ticket_key: str):
    """Check current status of a Jira ticket."""
    client, _ = _build_ready_client()
    result = get_ticket_status(client=client, ticket_key=ticket_key)
    click.echo(json.dumps(result, indent=2))


@cli.command("move-ticket")
@click.option("--ticket-key", required=True, help="Ticket key, e.g. ENG-123")
@click.option("--transition", required=True, help="Transition name, e.g. Done")
def move_ticket_cmd(ticket_key: str, transition: str):
    """Move ticket to another Jira workflow state."""
    client, _ = _build_ready_client()
    transition_ticket(client=client, ticket_key=ticket_key, transition_name=transition)
    click.echo(
        json.dumps(
            {"ticket_key": ticket_key, "transition": transition, "status": "updated"},
            indent=2,
        )
    )


if __name__ == "__main__":
    cli()
