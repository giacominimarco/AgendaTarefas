#!/usr/bin/env python3
"""
Script para testar a conexão com o banco de dados MySQL
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.connection import db

def test_connection():
    """Testa a conexão com o banco de dados"""
    try:
        print("🔍 Testando conexão com o banco de dados...")
        
        # Testar conexão básica
        connection = db.get_connection()
        print("✅ Conexão estabelecida com sucesso!")
        
        # Verificar se a tabela tasks existe
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES LIKE 'tasks'")
        tables = cursor.fetchall()
        
        if tables:
            print("✅ Tabela 'tasks' encontrada!")
            
            # Contar registros
            cursor.execute("SELECT COUNT(*) as count FROM tasks")
            result = cursor.fetchone()
            print(f"📊 Total de tarefas no banco: {result['count']}")
            
            # Listar algumas tarefas
            cursor.execute("SELECT id, title, status FROM tasks LIMIT 5")
            tasks = cursor.fetchall()
            
            if tasks:
                print("📋 Tarefas encontradas:")
                for task in tasks:
                    print(f"   - ID: {task['id']}, Título: {task['title']}, Status: {task['status']}")
            else:
                print("⚠️  Nenhuma tarefa encontrada no banco")
                
        else:
            print("❌ Tabela 'tasks' não encontrada!")
            print("💡 Execute o script schema.sql para criar a tabela")
            
        cursor.close()
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("\n🔧 Possíveis soluções:")
        print("1. Verifique se o MySQL está rodando")
        print("2. Verifique as configurações no arquivo .env")
        print("3. Execute o script schema.sql para criar o banco e tabelas")
        print("4. Verifique se o usuário tem permissões no banco")

if __name__ == "__main__":
    test_connection() 