-- Script SQL para criar o banco de dados e tabela de tarefas
-- Execute este script no MySQL para configurar o banco de dados

-- Criar o banco de dados
CREATE DATABASE IF NOT EXISTS agenda_tarefas;
USE agenda_tarefas;

-- Criar a tabela de tarefas
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status ENUM('pendente', 'concluída') DEFAULT 'pendente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Inserir alguns dados de exemplo
INSERT INTO tasks (title, description, status, due_date) VALUES
('Estudar React', 'Aprender os conceitos básicos do React JS', 'pendente', '2024-01-15 18:00:00'),
('Fazer exercícios', 'Treino de musculação na academia', 'concluída', '2024-01-10 07:00:00'),
('Ler livro técnico', 'Ler capítulos 5 e 6 do livro de Python', 'pendente', '2024-01-20 22:00:00'),
('Reunião com cliente', 'Apresentar proposta de projeto', 'pendente', '2024-01-12 14:00:00'),
('Organizar workspace', 'Limpar arquivos desnecessários do computador', 'pendente', '2024-01-08 16:00:00');

-- Verificar se os dados foram inseridos
SELECT * FROM tasks; 