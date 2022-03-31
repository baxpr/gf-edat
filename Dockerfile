FROM ubuntu:20.04

RUN apt-get -y update && \
    DEBIAN_FRONTEND=noninteractive apt-get -y install wget unzip xvfb openjdk-8-jre python3-pip && \
    apt-get clean

RUN pip3 install pandas fpdf

# Copy the pipeline code
COPY src /opt/gf-edat/src
COPY README.md /opt/gf-edat/README.md

# Add pipeline to system path
ENV PATH /opt/gf-edat/src:${PATH}

# Entrypoint
ENTRYPOINT ["gf-edat.sh"]
