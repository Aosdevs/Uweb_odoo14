FROM odoo:14
# Copy entrypoint script and Odoo configuration file
USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    libxmlsec1-dev \
    libxml2-dev \
    libxslt1-dev \
    libxml2 \
    libxmlsec1 \
    python3-dev \
    pkg-config \
    wget \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    zlib1g-dev

COPY ./extra-addons /usr/lib/python3/dist-packages/odoo/extra-addons

WORKDIR /usr/lib/python3/dist-packages/odoo/extra-addons
RUN pip3 install --upgrade pip wheel setuptools \
    && pip3 install -r ./pip-requirements.txt

COPY ./odoo.conf /etc/odoo/odoo.conf