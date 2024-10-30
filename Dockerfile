# First Stage: Dependency Installation
FROM python:3.8-slim as builder

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Second Stage: Build the Final Image
FROM python:3.8-slim

# Create a non-root user and switch to it
RUN useradd -m nonrootuser
USER nonrootuser

# Set the working directory and copy from the builder stage
WORKDIR /app
COPY --from=builder /app /app

# Copy application code
COPY . .

# Expose the Streamlit port
EXPOSE 8501

# Run the app with Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
