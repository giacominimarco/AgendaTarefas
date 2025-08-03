"""
Módulo de conexão com o banco de dados MySQL
Responsável por gerenciar a conexão e operações básicas do banco
"""

import mysql.connector
from mysql.connector import Error
import json
import os
from datetime import datetime
from pathlib import Path

def load_env_file():
    env_path = Path(__file__).parent.parent / '.env'
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if '\x00' in line: # ignora linhas com caractere nulo
                    continue 
                # Ignora linhas vazias, comentários ou mal formatadas
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                os.environ[key] = value


def get_database_config():
    load_env_file()
    
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASSWORD', ''),
        'database': os.getenv('DB_NAME', 'agenda_tarefas'),
        'charset': os.getenv('DB_CHARSET', 'utf8mb4'),
        'collation': os.getenv('DB_COLLATION', 'utf8mb4_unicode_ci')
    }

class DatabaseConnection:
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._connection:
            self._connect()
    
    def _connect(self):
        try:
            config = get_database_config()
            
            self._connection = mysql.connector.connect(**config)
            print("Conexão com o banco de dados estabelecida com sucesso!")
            
        except Error as e:
            print(f"Erro ao conectar com o banco de dados: {e}")
            raise
    
    def get_connection(self):
        if not self._connection or not self._connection.is_connected():
            self._connect()
        return self._connection
    
    def execute_query(self, query, params=None):
        try:
            connection = self.get_connection()
            cursor = connection.cursor(dictionary=True)
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Para SELECT, retorna os resultados
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                cursor.close()
                return results
            
            # Para INSERT, UPDATE, DELETE, faz commit
            connection.commit()
            cursor.close()
            return True
            
        except Error as e:
            print(f"❌ Erro ao executar query: {e}")
            if connection:
                connection.rollback()
            raise
    
    def close_connection(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("Conexão com o banco de dados fechada!")

db = DatabaseConnection() 