from datetime import datetime
import json
from database.connection import db

class Task:
    def __init__(self, id=None, title="", description="", status="pendente", 
                 created_at=None, due_date=None):
        """
        Inicializa uma nova tarefa
        Args:
            id (int): ID único da tarefa
            title (str): Título da tarefa
            description (str): Descrição da tarefa
            status (str): Status da tarefa ('pendente' ou 'concluída')
            created_at (datetime): Data de criação
            due_date (datetime): Data de vencimento
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at or datetime.now()
        self.due_date = due_date
    
    def to_dict(self):
        """
        Converte a tarefa para um dicionário
        Returns:
            dict: Dicionário representando a tarefa
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'due_date': self.due_date.isoformat() if self.due_date else None
        }
    
    def to_json(self):
        """
        Converte a tarefa para JSON
        Returns:
            str: String JSON representando a tarefa
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, default=str)
    
    @staticmethod
    def from_dict(data):
        """
        Cria uma tarefa a partir de um dicionário
        Args:
            data (dict): Dicionário com os dados da tarefa
        Returns:
            Task: Nova instância de Task
        """
        # Converter strings de data para datetime
        created_at = None
        due_date = None
        
        if data.get('created_at'):
            if isinstance(data['created_at'], str):
                created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
            else:
                created_at = data['created_at']
        
        if data.get('due_date'):
            if isinstance(data['due_date'], str):
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            else:
                due_date = data['due_date']
        
        return Task(
            id=data.get('id'),
            title=data.get('title', ''),
            description=data.get('description', ''),
            status=data.get('status', 'pendente'),
            created_at=created_at,
            due_date=due_date
        )
    
    @staticmethod
    def get_all():
        try:
            query = """
                SELECT id, title, description, status, created_at, due_date
                FROM tasks
                ORDER BY created_at DESC
            """
            results = db.execute_query(query)
            
            tasks = []
            for row in results:
                task = Task.from_dict(row)
                tasks.append(task)
            
            return tasks
            
        except Exception as e:
            print(f"Erro ao buscar tarefas: {e}")
            return []
    
    @staticmethod
    def get_by_id(task_id):
        try:
            query = """
                SELECT id, title, description, status, created_at, due_date
                FROM tasks
                WHERE id = %s
            """
            results = db.execute_query(query, (task_id,))
            
            if results:
                return Task.from_dict(results[0])
            return None
            
        except Exception as e:
            print(f"Erro ao buscar tarefa {task_id}: {e}")
            return None
    
    def save(self):
        try:
            if self.id:
                # Atualizar tarefa existente
                query = """
                    UPDATE tasks 
                    SET title = %s, description = %s, status = %s, due_date = %s
                    WHERE id = %s
                """
                params = (self.title, self.description, self.status, self.due_date, self.id)
            else:
                # Criar nova tarefa
                query = """
                    INSERT INTO tasks (title, description, status, due_date)
                    VALUES (%s, %s, %s, %s)
                """
                params = (self.title, self.description, self.status, self.due_date)
            
            db.execute_query(query, params)
            
            # Se é uma nova tarefa, buscar o ID gerado
            if not self.id:
                query = "SELECT LAST_INSERT_ID() as id"
                result = db.execute_query(query)
                if result:
                    self.id = result[0]['id']
            
            return True
            
        except Exception as e:
            print(f"Erro ao salvar tarefa: {e}")
            return False
    
    def delete(self):
        try:
            if not self.id:
                return False
            
            query = "DELETE FROM tasks WHERE id = %s"
            db.execute_query(query, (self.id,))
            return True
            
        except Exception as e:
            print(f"Erro ao deletar tarefa {self.id}: {e}")
            return False
    
    def mark_as_completed(self):
        try:
            self.status = 'concluída'
            return self.save()
            
        except Exception as e:
            print(f"Erro ao marcar tarefa como concluída: {e}")
            return False 