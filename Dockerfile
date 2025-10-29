# Imagem base com Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos de requisitos e instala dependências
COPY requeriments.txt .

RUN pip install --no-cache-dir -r requeriments.txt

# Copia o restante do projeto para dentro do container
COPY . .

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando padrão para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

