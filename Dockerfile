# 1. Base Image
FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Create the user FIRST (so we can assign permissions)
RUN useradd -m appuser

# 4. Copy requirements
COPY requirements.txt .

# 5. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy application code AND change ownership to appuser
#    (This is the critical fix!)
COPY --chown=appuser:appuser . .

# 7. Switch to non-root user
USER appuser

# 8. Expose port
EXPOSE 8000

# 9. Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]