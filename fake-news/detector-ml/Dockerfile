# Use official Python image
FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install dependencies
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# Copy app files
COPY . .

# Expose the FastAPI port
EXPOSE 8000

# Run the app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
