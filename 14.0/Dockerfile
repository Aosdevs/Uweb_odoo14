FROM odoo:14

# Instale dependências necessárias para o Python 3.8
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
    zlib1g-dev \
    && apt-get clean

# Baixe, compile e instale o Python 3.8
RUN wget https://www.python.org/ftp/python/3.8.9/Python-3.8.9.tgz \
    && tar -xzf Python-3.8.9.tgz \
    && cd Python-3.8.9 \
    && ./configure --enable-optimizations \
    && make -j$(nproc) \
    && make altinstall \
    && cd .. \
    && rm -rf Python-3.8.9 Python-3.8.9.tgz

# Crie um link simbólico para o python3.8
RUN ln -s /usr/local/bin/python3.8 /usr/bin/python3.8 \
    && ln -s /usr/local/bin/pip3.8 /usr/bin/pip3.8

# Copie os addons extras
COPY ./extra-addons /usr/lib/python3/dist-packages/odoo/extra-addons

# Defina o diretório de trabalho
WORKDIR /usr/lib/python3/dist-packages/odoo/extra-addons

# Use pip3.8 para instalar as dependências
RUN pip3.8 install --upgrade pip wheel setuptools \
    && pip3.8 install -r ./pip-requirements.txt

# Copie o arquivo de configuração do Odoo
COPY ./odoo.conf /etc/odoo/
