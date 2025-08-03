import os
from pathlib import Path

def create_env_file():
    env_content = """# Configurações do Banco de Dados
# Copie este arquivo para .env e ajuste conforme necessário

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=
DB_NAME=agenda_tarefas
DB_CHARSET=utf8mb4
DB_COLLATION=utf8mb4_unicode_ci
"""
    
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        print("Arquivo .env já existe!")
        response = input("Deseja sobrescrever? (y/N): ")
        if response.lower() != 'y':
            print("Operação cancelada.")
            return False
    
    try:
        with open(env_path, 'w') as f:
            f.write(env_content)
        print("Arquivo .env criado com sucesso!")
        print(f"Localização: {env_path}")
        print("\nPara alterar as configurações, edite o arquivo .env")
        return True
    except Exception as e:
        print(f"Erro ao criar arquivo .env: {e}")
        return False

def show_env_help():
    print("\nComo usar o arquivo .env:")
    print("=" * 40)
    print("1. Execute: python create_env.py")
    print("2. Edite o arquivo .env gerado")
    print("3. Ajuste as configurações conforme necessário")
    print("\nExemplo de configuração:")
    print("DB_HOST=localhost")
    print("DB_USER=root")
    print("DB_PASSWORD=sua_senha")
    print("DB_NAME=agenda_tarefas")

if __name__ == '__main__':
    print("Criando arquivo .env")
    print("=" * 30)
    
    if create_env_file():
        show_env_help()
    else:
        print("\nFalha ao criar arquivo .env") 