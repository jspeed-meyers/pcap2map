## TODO: THIS DOCKERFILE DOES NOT WORK

# Use a python image since this is a python app
FROM python:3.7-slim

LABEL creator="John Speed Meyers"

# Set working directory
WORKDIR /src

# Copy over requirements.txt first to take 
# advantage of layer caching
COPY requirements.txt .

WORKDIR /
 
# Run apt-get update, install dependencies, and
# manage orca appimage
RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
  build-essential \
  desktop-file-utils \
  fuse \
  libgtk2.0-0 \
  libgconf-2-4 \
  libxtst6 \
  libxss1 \
  libgconf-2-4 \
  libnss3 \
  libasound2 \
  tshark \
  wget \
  xvfb

# orca, needed for plotly, has an online reputation
# for being hard to integrate into an external app
# An improved version of this app might use a 
# visualization and mapping library other than plotly
# https://stackoverflow.com/questions/53710227/locate-lib-orca-with-python

RUN mkdir -p /opt/orca
RUN cd /opt/orca
RUN wget https://github.com/plotly/orca/releases/tag/v1.3.1/orca-1.3.1-x86_64.AppImage
RUN chmod +x orca-1.3.1-x86_64.AppImage
# TODO: Something is wrong here
RUN orca-1.3.1-x86_64.AppImage --appimage-extract
RUN rm orca-1.3.1-x86_64.AppImage 

WORKDIR /src

# Install python dependencies
RUN pip install -r requirements.txt

# Copy over project files - only the necessary
# files; .dockerignore lists unnecessary files
COPY . /src

# Install pcap2map
RUN python setup.py install

# Going to need a volume to save the picture on the
# user computer

# And then run command line approach with -m
# CMD ["python", "-m", pcpcap2map", "tests/test.pcap"]
