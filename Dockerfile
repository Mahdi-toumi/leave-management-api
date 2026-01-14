# 1. Base Image: Use a lightweight Python version
FROM python:3.10-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy dependencies file first (for better caching)
COPY requirements.txt .

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the rest of the application code
COPY app/ ./app/

# 6. Security: Create a non-root user and switch to it
# (Running as root is a security risk)
RUN useradd -m appuser
USER appuser

# 7. Expose the port the app runs on
EXPOSE 8000

# 8. Command to run the application
# We use 'app.main:app' because our code is inside the 'app' folder
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]