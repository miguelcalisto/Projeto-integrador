# Imagem base do Python
FROM python:3.12-slim


# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências
COPY requeriments.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requeriments.txt

# Copia todo o restante do código
COPY . .

# Expõe a porta padrão do Django
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
