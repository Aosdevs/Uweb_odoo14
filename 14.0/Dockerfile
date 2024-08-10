# Use a imagem base com Python 3.8
FROM python:3.8

# Instale dependências básicas e o Odoo
RUN apt-get update && apt-get install -y \
    wget \
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
    git

# Instale o Odoo 14
RUN wget https://github.com/odoo/odoo/archive/refs/tags/14.0.tar.gz && \
    tar -xzf 14.0.tar.gz && \
    mv odoo-14.0 /opt/odoo && \
    pip install --upgrade pip wheel setuptools && \
    pip install -r /opt/odoo/requirements.txt

# Adicione os addons extras
COPY ./extra-addons /opt/odoo/extra-addons

# Copie o arquivo de configuração do Odoo
COPY ./odoo.conf /etc/odoo/

# Defina o diretório de trabalho e o ponto de entrada
WORKDIR /opt/odoo
ENTRYPOINT ["odoo"]
CMD ["-c", "/etc/odoo/odoo.conf"]

# Exponha a porta padrão do Odoo
EXPOSE 8069
