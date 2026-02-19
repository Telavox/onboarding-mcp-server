FROM python:3.11-slim

# Use uv for deterministic installs from uv.lock
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy

# Copy workspace manifests first
COPY pyproject.toml uv.lock ./

# Copy only this workspace member
COPY src/apps/onboarding-mcp ./src/apps/onboarding-mcp
COPY src/libs ./src/libs

# Install deps into a venv using the lockfile
RUN uv venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app/src/apps/onboarding-mcp
RUN uv sync --frozen --no-dev --project /app --active --package onboarding-mcp


ENV PORT=8000
EXPOSE 8000

CMD ["uv", "run", "--active", "--no-sync", "--script", "main.py"]
