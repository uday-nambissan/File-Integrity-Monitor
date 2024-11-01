# Use the official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /FIM

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose ports as needed (e.g., 80 for web servers)
EXPOSE 80

# Command to run the FIM script
CMD ["python", "file_integrity_monitor.py"]
