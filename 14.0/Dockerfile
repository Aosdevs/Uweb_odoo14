# Use a imagem base com Python 3.8
FROM python:3.8

# Instale dependências básicas e o Odoo
RUN apt-get update && apt-get install -y \
    git \
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
    && rm -rf /var/lib/apt/lists/*

# Crie o diretório para o Odoo
RUN mkdir -p /opt/odoo

# Clone o repositório do Odoo na branch 14
RUN git clone -b 14.0 --single-branch https://github.com/odoo/odoo.git /opt/odoo

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
