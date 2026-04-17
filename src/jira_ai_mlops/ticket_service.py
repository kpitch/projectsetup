from jira import JIRA

from .mlops_rules import score_ticket_for_mlops


def create_ticket(
    client: JIRA,
    project_key: str,
    summary: str,
    description: str,
    issue_type: str = "Task",
    labels: list[str] | None = None,
) -> dict:
    labels = labels or []
    score = score_ticket_for_mlops(summary=summary, description=description, labels=labels)

    issue = client.create_issue(
        fields={
            "project": {"key": project_key},
            "summary": summary,
            "description": f"{description}\n\n[MLOps Recommendation] {score.recommendation}",
            "issuetype": {"name": issue_type},
            "labels": labels,
            "priority": {"name": score.priority},
        }
    )
    return {
        "key": issue.key,
        "id": issue.id,
        "priority": score.priority,
        "score": score.score,
    }


def get_ticket_status(client: JIRA, ticket_key: str) -> dict:
    issue = client.issue(ticket_key)
    return {
        "key": issue.key,
        "summary": issue.fields.summary,
        "status": issue.fields.status.name,
        "priority": issue.fields.priority.name if issue.fields.priority else None,
        "assignee": issue.fields.assignee.displayName if issue.fields.assignee else None,
    }


def transition_ticket(client: JIRA, ticket_key: str, transition_name: str) -> None:
    transitions = client.transitions(ticket_key)
    transition_id = None
    for transition in transitions:
        if transition["name"].lower() == transition_name.lower():
            transition_id = transition["id"]
            break

    if not transition_id:
        available = ", ".join(t["name"] for t in transitions)
        raise ValueError(
            f"Transition '{transition_name}' not found. Available transitions: {available}"
        )

    client.transition_issue(ticket_key, transition_id)
