FROM python:3.13-slim-bookworm AS builder
ARG GITHUB_API_TOKEN

RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
RUN apt-get update && apt-get install -y git
RUN git config --global url."https://${GITHUB_API_TOKEN}:x-oauth-basic@github.com/qlik-trial".insteadOf "https://github.com/qlik-trial"
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_CACHE_DIR=/app/.cache/uv

RUN mkdir -p /app/.cache/uv

COPY {{template_agent}} /app/{{template_agent}}
COPY uv.lock /app
COPY pyproject.toml /app
COPY swarm_configs/ /app/swarm_configs

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN --mount=type=cache,target=/app/.cache/uv \
    UV_CACHE_DIR=/app/.cache/uv uv sync --frozen

RUN mkdir -p /app/.cache/uv && chown -R 64357:64357 /app

# prod image
FROM python:3.13-slim-bookworm AS prod
COPY --from=builder /root/.local /root/.local
COPY --from=builder /app /app
ENV PATH="/root/.local/bin:$PATH"
ENV UV_CACHE_DIR=/app/.cache/uv

ARG VERSION
ARG CREATED
ARG REVISION

ENV BUILD_INFO_VERSION=$VERSION
ENV BUILD_INFO_CREATED=$CREATED
ENV BUILD_INFO_REVISION=$REVISION

LABEL org.opencontainers.image.created=$CREATED
LABEL org.opencontainers.image.source="https://github.com/qlik-trial/{{template-agent}}"
LABEL org.opencontainers.image.version=$VERSION
LABEL org.opencontainers.image.revision=$REVISION

EXPOSE 8000

RUN chown -R 64357:64357 /app

USER 64357:64357

WORKDIR /app
CMD ["uv", "run", "python", "-m", "{{template_agent}}"]
