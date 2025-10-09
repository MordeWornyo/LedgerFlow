FROM python:3.11-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt requirements-dev.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt -r requirements-dev.txt

# Copy project code
COPY . .

CMD ["pytest", "-v", "--cov=.", "--cov-report=term-missing", "--disable-warnings"]