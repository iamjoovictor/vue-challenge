# imagem de referência para o container backend: baseada na imagem de python 3.10
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# cria um diretório chamadao 'backend' dentro no container criado
WORKDIR /backend

# copia o arquivo requirements.txt para o diretório requirements.txt
COPY ./requirements.txt /backend/requirements.txt

# instalada todas as dependências dentro da imagem
RUN pip install --no-cache-dir -r /backend/requirements.txt

# copia o diretório atual para diretório backend dentro do container
COPY ./ /backend
