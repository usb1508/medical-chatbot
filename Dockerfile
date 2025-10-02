FROM python:3.12-slim

# Install curl + build essentials (slim images are barebones)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH (installer puts it in ~/.cargo/bin)
ENV PATH="/root/.cargo/bin:$PATH"

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install dependencies with uv
RUN uv sync --frozen

# Copy the rest of the source code
COPY . .

# Run your app using uv
CMD ["uv", "run", "python", "app.py"]
