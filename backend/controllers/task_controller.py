import json
from datetime import datetime
from models.task import Task

class TaskController:
    @staticmethod
    def get_all_tasks():
        """
        Retorna todas as tarefas em formato JSON
        Returns:
            tuple: (status_code, response_body, headers)
        """
        try:
            tasks = Task.get_all()
            tasks_data = [task.to_dict() for task in tasks]
            
            response = {
                'success': True,
                'data': tasks_data,
                'message': f'Encontradas {len(tasks_data)} tarefas'
            }
            
            return 200, json.dumps(response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            }
            
        except Exception as e:
            error_response = {
                'success': False,
                'message': f'Erro ao buscar tarefas: {str(e)}'
            }
            return 500, json.dumps(error_response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            }
    
    @staticmethod
    def get_task_by_id(task_id):
        """
        Returns:
            tuple: (status_code, response_body, headers)
        """
        try:
            task = Task.get_by_id(task_id)
            
            if not task:
                error_response = {
                    'success': False,
                    'message': f'Tarefa com ID {task_id} não encontrada'
                }
                return 404, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            
            response = {
                'success': True,
                'data': task.to_dict(),
                'message': 'Tarefa encontrada com sucesso'
            }
            
            return 200, json.dumps(response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            }
            
        except Exception as e:
            error_response = {
                'success': False,
                'message': f'Erro ao buscar tarefa: {str(e)}'
            }
            return 500, json.dumps(error_response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            }
    
    @staticmethod
    def create_task(request_data):
        """
        Args:
            request_data (dict): Dados da requisição
        
        Returns:
            tuple: (status_code, response_body, headers)
        """
        try:
            # Validar dados obrigatórios
            if not request_data.get('title'):
                error_response = {
                    'success': False,
                    'message': 'Título é obrigatório'
                }
                return 400, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            
            # Converter due_date se fornecido
            due_date = None
            if request_data.get('due_date'):
                try:
                    due_date = datetime.fromisoformat(request_data['due_date'].replace('Z', '+00:00'))
                except ValueError:
                    error_response = {
                        'success': False,
                        'message': 'Formato de data inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)'
                    }
                    return 400, json.dumps(error_response, ensure_ascii=False), {
                        'Content-Type': 'application/json'
                    }
            
            # Criar nova tarefa
            task = Task(
                title=request_data.get('title', ''),
                description=request_data.get('description', ''),
                status=request_data.get('status', 'pendente'),
                due_date=due_date
            )
            
            if task.save():
                response = {
                    'success': True,
                    'data': task.to_dict(),
                    'message': 'Tarefa criada com sucesso'
                }
                return 201, json.dumps(response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            else:
                error_response = {
                    'success': False,
                    'message': 'Erro ao salvar tarefa no banco de dados'
                }
                return 500, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
                
        except Exception as e:
            error_response = {
                'success': False,
                'message': f'Erro ao criar tarefa: {str(e)}'
            }
            return 500, json.dumps(error_response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            }
    
    @staticmethod
    def update_task(task_id, request_data):
        """
        Returns:
            tuple: (status_code, response_body, headers)
        """
        try:
            # Buscar tarefa existente
            task = Task.get_by_id(task_id)
            
            if not task:
                error_response = {
                    'success': False,
                    'message': f'Tarefa com ID {task_id} não encontrada'
                }
                return 404, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            
            # Atualizar campos fornecidos
            if 'title' in request_data:
                task.title = request_data['title']
            if 'description' in request_data:
                task.description = request_data['description']
            if 'status' in request_data:
                task.status = request_data['status']
            if 'due_date' in request_data:
                if request_data['due_date']:
                    try:
                        task.due_date = datetime.fromisoformat(request_data['due_date'].replace('Z', '+00:00'))
                    except ValueError:
                        error_response = {
                            'success': False,
                            'message': 'Formato de data inválido. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)'
                        }
                        return 400, json.dumps(error_response, ensure_ascii=False), {
                            'Content-Type': 'application/json'
                        }
                else:
                    task.due_date = None
            
            if task.save():
                response = {
                    'success': True,
                    'data': task.to_dict(),
                    'message': 'Tarefa atualizada com sucesso'
                }
                return 200, json.dumps(response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            else:
                error_response = {
                    'success': False,
                    'message': 'Erro ao atualizar tarefa no banco de dados'
                }
                return 500, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
                
        except Exception as e:
            error_response = {
                'success': False,
                'message': f'Erro ao atualizar tarefa: {str(e)}'
            }
            return 500, json.dumps(error_response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            }
    
    @staticmethod
    def mark_task_as_completed(task_id):
        """
        Returns:
            tuple: (status_code, response_body, headers)
        """
        try:
            task = Task.get_by_id(task_id)
            
            if not task:
                error_response = {
                    'success': False,
                    'message': f'Tarefa com ID {task_id} não encontrada'
                }
                return 404, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            
            if task.mark_as_completed():
                response = {
                    'success': True,
                    'data': task.to_dict(),
                    'message': 'Tarefa marcada como concluída com sucesso'
                }
                return 200, json.dumps(response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            else:
                error_response = {
                    'success': False,
                    'message': 'Erro ao marcar tarefa como concluída'
                }
                return 500, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
                
        except Exception as e:
            error_response = {
                'success': False,
                'message': f'Erro ao marcar tarefa como concluída: {str(e)}'
            }
            return 500, json.dumps(error_response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            }
    
    @staticmethod
    def delete_task(task_id):
        """
        Returns:
            tuple: (status_code, response_body, headers)
        """
        try:
            task = Task.get_by_id(task_id)
            
            if not task:
                error_response = {
                    'success': False,
                    'message': f'Tarefa com ID {task_id} não encontrada'
                }
                return 404, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            
            if task.delete():
                response = {
                    'success': True,
                    'message': 'Tarefa removida com sucesso'
                }
                return 200, json.dumps(response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
            else:
                error_response = {
                    'success': False,
                    'message': 'Erro ao remover tarefa do banco de dados'
                }
                return 500, json.dumps(error_response, ensure_ascii=False), {
                    'Content-Type': 'application/json'
                }
                
        except Exception as e:
            error_response = {
                'success': False,
                'message': f'Erro ao remover tarefa: {str(e)}'
            }
            return 500, json.dumps(error_response, ensure_ascii=False), {
                'Content-Type': 'application/json'
            } 