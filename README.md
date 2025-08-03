# 📋 Agenda de Tarefas

Aplicação simples de gerenciamento de tarefas com **React** (Frontend) e **Python** (Backend) + **MySQL**.

## 🚀 Funcionalidades

- ✅ Criar, editar, excluir tarefas
- ✅ Marcar tarefas como concluídas
- ✅ Interface responsiva e moderna
- ✅ Lista organizada por status

## 🛠️ Tecnologias

- **Frontend**: React 18 + CSS3
- **Backend**: Python + HTTP Server
- **Banco**: MySQL

## 📦 Instalação

### 1. Backend
```bash
cd backend
pip install -r requirements.txt
```

### 2. Banco de Dados
```bash
# Criar banco
mysql -u root -p -e "CREATE DATABASE agenda_tarefas;"

# Executar schema
mysql -u root -p agenda_tarefas < schema.sql
```

### 3. Configurar .env
```bash
cd backend
cp env_example.txt .env
# Editar .env com suas configurações
```

### 4. Frontend
```bash
cd frontend
npm install
```

## 🚀 Executar

### Backend
```bash
cd backend
python server.py
# http://localhost:8000
```

### Frontend
```bash
cd frontend
npm start
# http://localhost:3000
```

## 📡 API

- `GET /tasks` - Listar tarefas
- `POST /tasks` - Criar tarefa
- `PUT /tasks/:id` - Editar tarefa
- `PATCH /tasks/:id/complete` - Concluir tarefa
- `DELETE /tasks/:id` - Excluir tarefa

## 👨‍💻 Autor

**Marco Giacomini**
- LinkedIn: [Marco Giacomini](https://www.linkedin.com/in/marco-giacomini/)