# Get latest Python3
FROM python:latest

# Workdirectory and File
WORKDIR /usr/app/src
COPY main.py ./

# Install Python Modules
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy Config File
COPY config.yaml ./

# Execute Program
CMD ["python3", "./main.py"]
