FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

WORKDIR /opt/waveshop

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-dev --no-cache --compile-bytecode \
    && find .venv -type d -name "__pycache__" -exec rm -rf {} + \
    && rm -rf .venv/lib/python3.12/site-packages/pip* \
    && rm -rf .venv/lib/python3.12/site-packages/setuptools* \
    && rm -rf .venv/lib/python3.12/site-packages/wheel*

FROM python:3.12-alpine AS final

WORKDIR /opt/waveshop

COPY --from=builder /opt/waveshop/.venv /opt/waveshop/.venv

ENV PATH="/opt/waveshop/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/opt/waveshop

COPY ./src ./src
COPY ./assets /opt/waveshop/assets.default
COPY ./docker-entrypoint.sh ./docker-entrypoint.sh

RUN chmod +x ./docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
