# wedding-be

## Setup (local)

Create and activate a virtualenv (Linux/macOS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Configure environment:

```bash
cp .env.example .env
```

Run API:

```bash
uvicorn app.main:app --reload
```

## Common issue: `ModuleNotFoundError: No module named 'fastapi'`

This means you started `uvicorn` outside the virtualenv. Re-run with the venv activated:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```