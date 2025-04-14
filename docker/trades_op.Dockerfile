FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PATH="/app/.venv/bin:$PATH"

# Copy just the lockfiles first for better caching
COPY pyproject.toml uv.lock ./
COPY services /app/services

# Install dependencies (cached on lockfile changes)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev

# Copy source code
COPY . .

# Install project code
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENTRYPOINT []

CMD ["uv", "run", "/app/services/trades/src/trades/main.py"]