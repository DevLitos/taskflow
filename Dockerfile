FROM python:3.12

# Copiar ejecutables de uv desde su imagen oficial
COPY --from=ghcr.io/astral-sh/uv:0.13.1 /uv /uvx /bin/

WORKDIR /app

# Copiar solo la configuración del proyecto primero para aprovechar
# la caché de capas de Docker al instalar dependencias.
COPY pyproject.toml uv.lock ./
# Instalar dependencias respetando el lockfile (sin instalar el proyecto aún)
RUN uv sync --locked --no-install-project

# Copiar el código fuente del proyecto
COPY src/ ./src/

# Añadir el entorno virtual de uv al PATH para que los ejecutables
# instalados (como uvicorn) estén disponibles directamente.
ENV PATH="/app/.venv/bin:$PATH"
# Incluir src/ en el path de Python para que el paquete taskflow sea importable.
ENV PYTHONPATH="/app/src"

# Puerto en el que escucha la API
EXPOSE 8000

# Arrancar la aplicación con Uvicorn en modo producción
CMD ["uvicorn", "taskflow.main:app", "--host", "0.0.0.0", "--port", "8000"]