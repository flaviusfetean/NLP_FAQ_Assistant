# Stage 1: Base stage with ollama image
#FROM ollama_orca:0.1 as ollama_base

#EXPOSE 11434

# Stage 2: Final stage with Python application
FROM python:3.12.2

# Set environment variables, if needed
ENV PYTHONUNBUFFERED=1

# Install any necessary dependencies for your Python application
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # Add any necessary packages here \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#COPY --from=ollama_base /bin/ollama /bin/ollama

#RUN /bin/ollama ollama serve

# Copy your application code to the container
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port that your FastAPI application will run on
EXPOSE 8000

# Command to run your FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
