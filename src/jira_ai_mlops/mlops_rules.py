from dataclasses import dataclass


@dataclass
class MLOpsScoringResult:
    score: int
    priority: str
    recommendation: str


def score_ticket_for_mlops(
    summary: str,
    description: str,
    labels: list[str] | None = None,
) -> MLOpsScoringResult:
    labels = labels or []
    text = f"{summary} {description}".lower()
    score = 0

    critical_signals = ["incident", "outage", "production", "failed pipeline", "p0"]
    model_signals = ["drift", "retrain", "model", "ml", "accuracy drop"]
    data_signals = ["dataset", "schema", "feature", "etl", "data quality"]

    for signal in critical_signals:
        if signal in text:
            score += 4
    for signal in model_signals:
        if signal in text:
            score += 3
    for signal in data_signals:
        if signal in text:
            score += 2

    if any(label.lower() in {"urgent", "prod", "mlops"} for label in labels):
        score += 3

    if score >= 10:
        return MLOpsScoringResult(
            score=score,
            priority="Highest",
            recommendation="Escalate immediately and notify on-call MLOps.",
        )
    if score >= 6:
        return MLOpsScoringResult(
            score=score,
            priority="High",
            recommendation="Address in current sprint and monitor model health.",
        )
    return MLOpsScoringResult(
        score=score,
        priority="Medium",
        recommendation="Add to backlog and review in weekly triage.",
    )
