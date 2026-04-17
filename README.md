# Jira Python SDK + AI/MLOps Ticket Automation

This project is a Python CLI app using Jira SDK to:

- Create Jira tickets
- Check ticket status
- Move tickets between workflow states
- Auto-score tickets using a simple AI/MLOps triage rule

## Project Structure

- `main.py`: CLI entry point
- `src/jira_ai_mlops/config.py`: environment config loader and validator
- `src/jira_ai_mlops/jira_client.py`: Jira SDK client builder
- `src/jira_ai_mlops/ticket_service.py`: ticket create/status/transition service
- `src/jira_ai_mlops/mlops_rules.py`: AI/MLOps scoring and priority mapping

## Prerequisites

- Python 3.10+ (recommended)
- Jira Cloud account
- Jira API token
- Access to a Jira project key (for example: `ENG`)

## Step-by-Step Setup

### 1) Clone and enter project

```bash
git clone <your-repo-url>
cd projectsetup
```

### 2) Create virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

### 4) Create your environment file

```bash
cp .env.example .env
```

### 5) Generate Jira API token

1. Open [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click **Create API token**
3. Copy the token value

### 6) Fill `.env`

Update values in `.env`:

```env
JIRA_SERVER_URL=https://your-company.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-generated-token
JIRA_PROJECT_KEY=ENG
```

## Run the Application

### Create a ticket

```bash
python main.py create-ticket \
  --summary "Model drift alert in production" \
  --description "Prediction accuracy dropped by 12% in EU region." \
  --issue-type "Task" \
  --labels "mlops,prod,urgent"
```

### Check ticket status

```bash
python main.py check-status --ticket-key "ENG-101"
```

### Move ticket to another status

```bash
python main.py move-ticket --ticket-key "ENG-101" --transition "Done"
```

## AI/MLOps Triage Logic

The scoring logic in `src/jira_ai_mlops/mlops_rules.py`:

- Detects incident/model/data-related keywords
- Uses labels such as `urgent`, `prod`, and `mlops`
- Sets priority to `Highest`, `High`, or `Medium`
- Appends recommendation text into ticket description

You can later replace this with:

- A trained model endpoint
- LLM-based triage
- A custom MLOps policy service
