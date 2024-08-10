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
    git \
    && rm -rf /var/lib/apt/lists/*

# Crie o diretório para o Odoo
RUN mkdir -p /opt/odoo

# Baixe o Odoo 14
RUN wget https://github.com/odoo/odoo/archive/refs/tags/14.0.tar.gz

# Extraia o Odoo 14
RUN tar -xzf 14.0.tar.gz

# Mova os arquivos para o diretório de trabalho
RUN mv odoo-14.0/* /opt/odoo/ \
    && rm -rf odoo-14.0 14.0.tar.gz

# Instale os requisitos do Odoo
WORKDIR /opt/odoo
RUN pip install --upgrade pip wheel setuptools \
    && pip install -r requirements.txt

# Adicione os addons extras
COPY ./extra-addons /opt/odoo/addons

# Copie o arquivo de configuração do Odoo
COPY ./odoo.conf /etc/odoo/

# Defina o diretório de trabalho e o ponto de entrada
ENTRYPOINT ["odoo"]
CMD ["-c", "/etc/odoo/odoo.conf"]

# Exponha a porta padrão do Odoo
EXPOSE 8069
