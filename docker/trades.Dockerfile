# stage 1 : build application
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# enable bytecode complication and set uv to use system interpreter
ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY services /app/services

# Install dependencies (cached on lockfile changes)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Add project files and sync full dependencies
ADD . /app
# Install project code
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

#### stage 2 : Build application without uv 
FROM python:3.12-slim-bookworm

# set working directory 
WORKDIR /app

# add service name as an argument
# ARG SERVICE_NAME
# ENV SERVICE_NAME=${SERVICE_NAME}

# Create non root user for security
RUN groupadd -r app && useradd -r -g app app

# Create state directory with proper permissions
RUN mkdir -p /app/state && chown -R app:app /app/state

# copy application files from builder stage with correct permissions
COPY --from=builder --chown=app:app /app /app 

# set environment path to virtual environment
ENV PATH="/app/.venv/bin:$PATH"

# switch to non-root user
USER app

# ENTRYPOINT ["sh", "-c", "exec python /app/services/${SERVICE_NAME}/src/${SERVICE_NAME}/main.py"]
ENTRYPOINT ["sh", "-c", "exec python /app/services/trades/src/trades/main.py"]
CMD []
# CMD ["uv", "run", "/app/services/trades/src/trades/main.py"]