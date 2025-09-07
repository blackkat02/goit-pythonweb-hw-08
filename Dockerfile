FROM python:3.12-slim

WORKDIR /app

# Встановлюємо curl і uv
RUN apt-get update \
    && apt-get install -y curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh

# Додаємо uv у PATH
ENV PATH="/root/.local/bin:${PATH}"

# Спочатку копіюємо тільки requirements.txt (для кешування)
COPY requirements.txt .

# Встановлюємо залежності
RUN uv pip install --system -r requirements.txt \
    && mkdir -p /app/storage

# Копіюємо весь код
COPY . .

VOLUME ["/app/storage"]

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

