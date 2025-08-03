#!/usr/bin/env python3
"""
Script de Setup para Agenda de Tarefas
Automatiza a configuração inicial do projeto
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_banner():
    """Imprime o banner do projeto"""
    print("=" * 60)
    print("AGENDA DE TAREFAS - SETUP")
    print("=" * 60)
    print("Configurando o projeto FullStack...")
    print()

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    print("Verificando versão do Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Python 3.8+ é necessário!")
        print(f"Versão atual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_node():
    """Verifica se o Node.js está instalado"""
    print("Verificando Node.js...")
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Node.js {result.stdout.strip()} - OK")
            return True
        else:
            print("Node.js não encontrado!")
            return False
    except FileNotFoundError:
        print("Node.js não está instalado!")
        print("Baixe em: https://nodejs.org/")
        return False

def check_npm():
    """Verifica se o NPM está instalado e acessível"""
    print("Verificando NPM...")
    npm_command = "npm.cmd" if platform.system() == "Windows" else "npm"
    try:
        result = subprocess.run([npm_command, '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"NPM {result.stdout.strip()} - OK")
            return True
        else:
            print("NPM não encontrado!")
            return False
    except FileNotFoundError:
        print("NPM não está instalado ou não está no PATH.")
        print("Baixe em: https://nodejs.org/")
        return False


def install_backend_dependencies():
    """Instala as dependências do backend"""
    print("Instalando dependências do backend...")
    try:
        os.chdir('backend')
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("Dependências do backend instaladas!")
        
        # Criar arquivo .env se não existir
        env_file = Path('.env')
        if not env_file.exists():
            print("Criando arquivo .env...")
            subprocess.run([sys.executable, 'create_env.py'], check=True)
        
        os.chdir('..')
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar dependências: {e}")
        os.chdir('..')
        return False

def install_frontend_dependencies():
    """Instala as dependências do frontend"""
    print("Instalando dependências do frontend...")
    npm_command = "npm.cmd" if platform.system() == "Windows" else "npm"
    try:
        os.chdir('frontend')
        subprocess.run([npm_command, 'install'], check=True)
        print("Dependências do frontend instaladas!")
        os.chdir('..')
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao instalar dependências: {e}")
        os.chdir('..')
        return False
    except FileNotFoundError:
        print("Erro: comando 'npm' não encontrado. Verifique se o Node.js/NPM está instalado e no PATH.")
        os.chdir('..')
        return False


def create_start_scripts():
    """Cria scripts de inicialização"""
    print("Criando scripts de inicialização...")
    
    # Script para Windows
    if platform.system() == 'Windows':
        with open('start_backend.bat', 'w') as f:
            f.write('@echo off\n')
            f.write('echo Iniciando backend...\n')
            f.write('cd backend\n')
            f.write('python server.py\n')
            f.write('pause\n')
        
        with open('start_frontend.bat', 'w') as f:
            f.write('@echo off\n')
            f.write('echo Iniciando frontend...\n')
            f.write('cd frontend\n')
            f.write('npm start\n')
            f.write('pause\n')
        
        print("Scripts .bat criados!")
    
    # Script para Unix/Linux/Mac
    else:
        with open('start_backend.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Iniciando backend..."\n')
            f.write('cd backend\n')
            f.write('python3 server.py\n')
        
        with open('start_frontend.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write('echo "Iniciando frontend..."\n')
            f.write('cd frontend\n')
            f.write('npm start\n')
        
        # Tornar executáveis
        os.chmod('start_backend.sh', 0o755)
        os.chmod('start_frontend.sh', 0o755)
        
        print("Scripts .sh criados!")

def print_next_steps():
    """Imprime os próximos passos"""
    print("\n" + "=" * 60)
    print("SETUP CONCLUÍDO!")
    print("=" * 60)
    print("\nPRÓXIMOS PASSOS:")
    print("1. Configure o banco MySQL:")
    print("   - Execute: mysql -u root -p")
    print("   - Importe: source schema.sql")
    print("\n2. Inicie o backend:")
    if platform.system() == 'Windows':
        print("   - Execute: start_backend.bat")
    else:
        print("   - Execute: ./start_backend.sh")
    print("\n3. Inicie o frontend:")
    if platform.system() == 'Windows':
        print("   - Execute: start_frontend.bat")
    else:
        print("   - Execute: ./start_frontend.sh")
    print("\n4. Acesse a aplicação:")
    print("   - Frontend: http://localhost:3000")
    print("   - Backend API: http://localhost:8000")
    print("\nPara mais informações, consulte o README.md")

def main():
    """Função principal"""
    print_banner()
    
    # Verificações
    if not check_python_version():
        return
    
    if not check_node():
        return
    
    if not check_npm():
        return
    
    print()
    
    # Instalação de dependências
    if not install_backend_dependencies():
        return
    
    if not install_frontend_dependencies():
        return
    
    # Criação de scripts
    create_start_scripts()
    
    print_next_steps()

if __name__ == '__main__':
    main()
