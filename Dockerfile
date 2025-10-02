# Start from a base image with Python
FROM python:3.12-slim

# Install uv (they provide a standalone binary installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add uv to PATH (installer puts it in ~/.cargo/bin by default)
ENV PATH="/root/.cargo/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy only dependency files first (for caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen

# Now copy the rest of the source code
COPY . .

# Run your app
CMD ["uv", "run", "python", "app.py"]
