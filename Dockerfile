# First Stage: Dependency Installation
FROM python:3.8-slim AS builder

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Second Stage: Build the Final Image
FROM python:3.8-slim

# Create a non-root user first
RUN useradd -m nonrootuser

# Set the working directory and copy from the builder stage
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Ensure the data/uploaded_pdfs directory exists and set ownership to nonrootuser
RUN mkdir -p data/uploaded_pdfs && chown -R nonrootuser:nonrootuser data

# Switch to nonrootuser
USER nonrootuser

# Expose the Streamlit port
EXPOSE 8501

# Run the app with Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
