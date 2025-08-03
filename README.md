# 📋 Agenda de Tarefas - FullStack

Uma aplicação completa de gerenciamento de tarefas desenvolvida com **React** (Frontend) e **Python** (Backend), utilizando **MySQL** como banco de dados.

## 🚀 Funcionalidades

### ✅ Gerenciamento de Tarefas
- **Criar** novas tarefas com título, descrição e data de vencimento
- **Visualizar** lista de tarefas organizadas por status (Pendentes/Concluídas)
- **Editar** informações das tarefas existentes
- **Marcar** tarefas como concluídas
- **Excluir** tarefas desnecessárias

### 🎨 Interface Moderna
- Design responsivo e intuitivo
- Separação visual entre tarefas pendentes e concluídas
- Indicadores visuais para tarefas vencidas
- Animações suaves e feedback visual

### 🔧 Tecnologias Utilizadas

#### Frontend
- **React 18** - Biblioteca JavaScript para interface
- **CSS3** - Estilização moderna com flexbox e grid
- **Fetch API** - Comunicação com o backend

#### Backend
- **Python 3** - Linguagem principal
- **HTTP Server** - Servidor HTTP nativo do Python
- **MySQL** - Banco de dados relacional
- **MySQL Connector** - Driver para conexão com MySQL

## 📁 Estrutura do Projeto

```
AgendaTarefas/
├── backend/
│   ├── controllers/
│   │   └── task_controller.py
│   ├── database/
│   │   └── connection.py
│   ├── models/
│   │   └── task.py
│   ├── server.py
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── TaskForm.js
│   │   │   ├── TaskList.js
│   │   │   └── TaskItem.js
│   │   ├── App.js
│   │   └── App.css
│   ├── package.json
│   └── public/
├── schema.sql
└── README.md
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- **Node.js** (versão 14 ou superior)
- **Python** (versão 3.8 ou superior)
- **MySQL** (versão 5.7 ou superior)
- **Git**

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd AgendaTarefas
```

### 2. Configurar o Backend

#### Instalar Dependências Python
```bash
cd backend
pip install -r requirements.txt
```

#### Configurar Banco de Dados
1. **Criar banco de dados MySQL:**
```sql
CREATE DATABASE agenda_tarefas;
```

2. **Executar script de criação das tabelas:**
```bash
mysql -u root -p agenda_tarefas < schema.sql
```

3. **Configurar variáveis de ambiente:**
```bash
# Copiar arquivo de exemplo
cp env_example.txt .env

# Editar arquivo .env com suas configurações
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha
DB_NAME=agenda_tarefas
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci
```

#### Iniciar o Backend
```bash
python server.py
```
O servidor estará disponível em: `http://localhost:8000`

### 3. Configurar o Frontend

#### Instalar Dependências
```bash
cd frontend
npm install
```

#### Iniciar o Frontend
```bash
npm start
```
A aplicação estará disponível em: `http://localhost:3000`

## 📡 API Endpoints

### Tarefas
- `GET /tasks` - Listar todas as tarefas
- `GET /tasks/:id` - Buscar tarefa específica
- `POST /tasks` - Criar nova tarefa
- `PUT /tasks/:id` - Atualizar tarefa
- `PATCH /tasks/:id/complete` - Marcar como concluída
- `DELETE /tasks/:id` - Deletar tarefa

### Exemplo de Uso da API

#### Criar Tarefa
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Estudar React",
    "description": "Aprender conceitos básicos",
    "due_date": "2024-01-15T18:00:00"
  }'
```

#### Listar Tarefas
```bash
curl http://localhost:8000/tasks
```

## 🎯 Funcionalidades Principais

### Frontend
- ✅ **Interface responsiva** que funciona em desktop e mobile
- ✅ **Formulário de criação** com validação
- ✅ **Lista organizada** por status das tarefas
- ✅ **Edição inline** das tarefas
- ✅ **Indicadores visuais** para tarefas vencidas
- ✅ **Feedback visual** para todas as ações

### Backend
- ✅ **API RESTful** completa
- ✅ **Validação de dados** robusta
- ✅ **Tratamento de erros** abrangente
- ✅ **CORS configurado** para desenvolvimento
- ✅ **Conexão segura** com MySQL

## 🔧 Desenvolvimento

### Estrutura do Banco de Dados
```sql
CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('pendente', 'concluída') DEFAULT 'pendente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### Scripts Disponíveis

#### Backend
```bash
# Iniciar servidor de desenvolvimento
python server.py

# Testar conexão com banco
python test_db.py
```

#### Frontend
```bash
# Iniciar servidor de desenvolvimento
npm start

# Build para produção
npm run build

# Executar testes
npm test
```

## 🚀 Deploy

### Backend (Produção)
- Configurar servidor web (Apache/Nginx)
- Usar WSGI (Gunicorn/uWSGI)
- Configurar variáveis de ambiente de produção

### Frontend (Produção)
```bash
npm run build
```
- Servir arquivos estáticos
- Configurar proxy reverso para API

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👨‍💻 Autor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)

## 🙏 Agradecimentos

- Comunidade React
- Comunidade Python
- Stack Overflow
- Documentação oficial das tecnologias utilizadas

---

⭐ Se este projeto te ajudou, considere dar uma estrela no repositório!