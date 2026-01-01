# Stage 1: Build
FROM python:3.12-slim AS builder

# Install uv binary directly
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Copy dependency files only to cache layers
COPY pyproject.toml uv.lock ./

# Install dependencies into a standalone virtual environment
# --frozen ensures the lockfile is respected
RUN uv sync --frozen --no-install-project --no-dev

# Copy the rest of the source code
COPY app/ .

# Stage 2: Runtime
FROM python:3.12-slim AS runtime

WORKDIR /app

# Copy the pre-built virtual environment and source code
COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/ .

# Ensure the virtual environment's binaries are used
ENV PATH="/app/.venv/bin:$PATH"
# Optimize Python for production
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


EXPOSE 8080

# The ADK api_server command
# Syntax: adk api_server <source_directory_of_agents>
CMD ["adk", "api_server", "agents", "--host", "0.0.0.0", "--port", "8080"]