# Use a python image since this is a python app
FROM python:3.7-slim

LABEL creator="John Speed Meyers"

# Create new directory and make working directory
WORKDIR /src

# Copy over requirements first to take advantage of
# layer caching
COPY requirements.txt .

# Run apt-get update and then install tshark
RUN  apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  tshark \
  build-essential

# Install dependencies
# TODO: Can I combine this with commands above?
RUN pip install -r requirements.txt

# Copy over project files - only the necessary
# files; .dockerignore lists unnecessary files
COPY . /src

# What about setup.py build?

# RUN setup.py build

# And setup.py install?

# Going to need a volume to save the picture on the
# user computer

# And then run command line approach with -m
# CMD ["python", "pcpcap2map.py", "tests/test.pcap"]