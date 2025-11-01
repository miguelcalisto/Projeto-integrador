# 🤖 Projeto Integrador

Trabalho com [Django](https://www.djangoproject.com/) 🐍

---

## 🚀 Como Usar

1. **Crie e ative o [ambiente virtual](https://docs.python.org/pt-br/3/library/venv.html)** 

🐧  **Linux/WSL**:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

🖥️ **Windows**:

```bash
python -m venv .venv
.\.venv\Scripts\Activate
```

---

2. **Instale as dependências** 📦

```bash
pip install -r requirements.txt 
```

---

3. **Execute as migrações e inicie o servidor** 🛠️

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

4. **Criar superuser/admin** 👤

```bash
python manage.py createsuperuser
```

---

## 🐳 Como Rodar com [Docker](https://www.docker.com/)

Baixar a imagem do Docker Hub

```bash
docker pull miguelcalisto/projeto-integrador:latest
docker run -p 8000:8000 --name projeto_integrador_container miguelcalisto/projeto-integrador
```
Rodar as migrations e createsuperuser no docker
```bash
docker exec -it projeto_integrador_container python manage.py makemigrations
docker exec -it projeto_integrador_container python manage.py migrate
docker exec -it projeto_integrador_container python manage.py createsuperuser
```
acessar em https://localhost:8000

---

![print](assets/print01.png)

