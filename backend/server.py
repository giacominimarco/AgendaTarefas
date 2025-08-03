import json
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from controllers.task_controller import TaskController

class TaskAPIHandler(BaseHTTPRequestHandler):    
    def do_GET(self):
        """
        Gerencia requisições GET
        - GET /tasks → listar todas as tarefas
        - GET /tasks/:id → buscar tarefa específica
        """
        try:
            if self.path == '/favicon.ico':
                self.send_response(204)  # No Content
                self.end_headers()
                return
        
            # Parse da URL
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            
            # Rota para listar todas as tarefas
            if path == '/tasks':
                status_code, response_body, headers = TaskController.get_all_tasks()
                self._send_response(status_code, response_body, headers)
                return
            
            # Rota para buscar tarefa específica
            match = re.match(r'^/tasks/(\d+)$', path)
            if match:
                task_id = int(match.group(1))
                status_code, response_body, headers = TaskController.get_task_by_id(task_id)
                self._send_response(status_code, response_body, headers)
                return
            
            # Rota não encontrada
            self._send_404()
            
        except Exception as e:
            self._send_500(f"Erro interno do servidor: {str(e)}")
    
    def do_POST(self):
        """
        Gerencia requisições POST
        - POST /tasks → criar nova tarefa
        """
        try:
            if self.path == '/tasks':
                # Ler dados da requisição
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                
                # Parse do JSON
                try:
                    request_data = json.loads(post_data.decode('utf-8'))
                except json.JSONDecodeError:
                    self._send_400("JSON inválido")
                    return
                
                # Criar tarefa
                status_code, response_body, headers = TaskController.create_task(request_data)
                self._send_response(status_code, response_body, headers)
                return
            
            # Rota não encontrada
            self._send_404()
            
        except Exception as e:
            self._send_500(f"Erro interno do servidor: {str(e)}")
    
    def do_PUT(self):
        """
        Gerencia requisições PUT
        - PUT /tasks/:id → atualizar tarefa
        """
        try:
            # Parse da URL para extrair ID
            match = re.match(r'^/tasks/(\d+)$', self.path)
            if match:
                task_id = int(match.group(1))
                
                # Ler dados da requisição
                content_length = int(self.headers.get('Content-Length', 0))
                put_data = self.rfile.read(content_length)
                
                # Parse do JSON
                try:
                    request_data = json.loads(put_data.decode('utf-8'))
                except json.JSONDecodeError:
                    self._send_400("JSON inválido")
                    return
                
                # Atualizar tarefa
                status_code, response_body, headers = TaskController.update_task(task_id, request_data)
                self._send_response(status_code, response_body, headers)
                return
            
            # Rota não encontrada
            self._send_404()
            
        except Exception as e:
            self._send_500(f"Erro interno do servidor: {str(e)}")
    
    def do_PATCH(self):
        """
        Gerencia requisições PATCH
        - PATCH /tasks/:id/complete → marcar como concluída
        """
        try:
            # Parse da URL para extrair ID
            match = re.match(r'^/tasks/(\d+)/complete$', self.path)
            if match:
                task_id = int(match.group(1))
                
                # Marcar como concluída
                status_code, response_body, headers = TaskController.mark_task_as_completed(task_id)
                self._send_response(status_code, response_body, headers)
                return
            
            # Rota não encontrada
            self._send_404()
            
        except Exception as e:
            self._send_500(f"Erro interno do servidor: {str(e)}")
    
    def do_DELETE(self):
        """
        Gerencia requisições DELETE
        - DELETE /tasks/:id → deletar tarefa
        """
        try:
            # Parse da URL para extrair ID
            match = re.match(r'^/tasks/(\d+)$', self.path)
            if match:
                task_id = int(match.group(1))
                
                # Deletar tarefa
                status_code, response_body, headers = TaskController.delete_task(task_id)
                self._send_response(status_code, response_body, headers)
                return
            
            # Rota não encontrada
            self._send_404()
            
        except Exception as e:
            self._send_500(f"Erro interno do servidor: {str(e)}")
    
    def do_OPTIONS(self):
        """
        Gerencia requisições OPTIONS para CORS
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '86400')
        self.end_headers()
    
    def _send_response(self, status_code, response_body, headers):
        """
        Envia resposta HTTP com headers personalizados
        
        Args:
            status_code (int): Código de status HTTP
            response_body (str): Corpo da resposta
            headers (dict): Headers da resposta
        """
        self.send_response(status_code)
        
        # Adicionar headers CORS para todas as respostas
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        
        # Enviar headers
        for header, value in headers.items():
            self.send_header(header, value)
        
        self.end_headers()
        self.wfile.write(response_body.encode('utf-8'))
    
    def _send_404(self):
        """
        Envia resposta 404 - Rota não encontrada
        """
        error_response = {
            'success': False,
            'message': 'Rota não encontrada'
        }
        self._send_response(404, json.dumps(error_response, ensure_ascii=False), {
            'Content-Type': 'application/json'
        })
    
    def _send_400(self, message):
        """
        Envia resposta 400 - Bad Request
        
        Args:
            message (str): Mensagem de erro
        """
        error_response = {
            'success': False,
            'message': message
        }
        self._send_response(400, json.dumps(error_response, ensure_ascii=False), {
            'Content-Type': 'application/json'
        })
    
    def _send_500(self, message):
        """
        Envia resposta 500 - Internal Server Error
        
        Args:
            message (str): Mensagem de erro
        """
        error_response = {
            'success': False,
            'message': message
        }
        self._send_response(500, json.dumps(error_response, ensure_ascii=False), {
            'Content-Type': 'application/json'
        })
    
    def log_message(self, format, *args):
        """
        Personaliza o log de mensagens do servidor
        """
        print(f"{self.address_string()} - {format % args}")

def run_server(port=8000):
    """
    Inicia o servidor HTTP
    
    Args:
        port (int): Porta onde o servidor será executado
    """
    server_address = ('', port)
    httpd = HTTPServer(server_address, TaskAPIHandler)
    
    print(f"Servidor iniciado em http://localhost:{port}")
    print("Endpoints disponíveis:")
    print("   GET    /tasks              - Listar todas as tarefas")
    print("   GET    /tasks/:id          - Buscar tarefa específica")
    print("   POST   /tasks              - Criar nova tarefa")
    print("   PUT    /tasks/:id          - Atualizar tarefa")
    print("   PATCH  /tasks/:id/complete - Marcar como concluída")
    print("   DELETE /tasks/:id          - Deletar tarefa")
    print("\nPressione Ctrl+C para parar o servidor")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor parado!")
        httpd.server_close()

if __name__ == '__main__':
    run_server() 