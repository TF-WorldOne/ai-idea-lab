FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Cloud Run uses PORT environment variable
ENV PORT=8080

# Expose the port
EXPOSE 8080

# Streamlit configuration for Cloud Run
RUN mkdir -p ~/.streamlit && \
    echo "[server]" > ~/.streamlit/config.toml && \
    echo "headless = true" >> ~/.streamlit/config.toml && \
    echo "enableCORS = false" >> ~/.streamlit/config.toml && \
    echo "enableXsrfProtection = false" >> ~/.streamlit/config.toml && \
    echo "port = 8080" >> ~/.streamlit/config.toml

# Run the application
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
