FROM python:3.12

# Copiar ejecutables de uv desde imagen oficial
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

WORKDIR /app

# Copiar la configuracion del proyecto 
COPY pyproject.toml uv.lock ./
# Instalar dependencias respetando el lockfile
RUN uv sync --locked --no-install-project

COPY src/ ./src/


# Añade el entorno virtual de uv al PATH del sistema
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/src"

EXPOSE 8000

CMD ["uvicorn", "taskflow.main:app", "--host", "0.0.0.0", "--port", "8000"]