import React, { useState, useEffect } from 'react';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import './App.css';

function App() {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Buscar tarefas da API
  const fetchTasks = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/tasks');
      const data = await response.json();
      
      if (data.success) {
        setTasks(data.data);
      } else {
        setError(data.message);
      }
    } catch (err) {
      setError('Erro ao carregar tarefas. Verifique se o backend está rodando.');
    } finally {
      setLoading(false);
    }
  };

  // Carregar tarefas ao montar o componente
  useEffect(() => {
    fetchTasks();
  }, []);

  // Adicionar nova tarefa
  const addTask = async (taskData) => {
    try {
      const response = await fetch('http://localhost:8000/tasks', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      const data = await response.json();
      
      if (data.success) {
        setTasks([data.data, ...tasks]);
        return { success: true, message: 'Tarefa criada com sucesso!' };
      } else {
        return { success: false, message: data.message };
      }
    } catch (err) {
      return { success: false, message: 'Erro ao criar tarefa.' };
    }
  };

  // Atualizar tarefa
  const updateTask = async (taskId, taskData) => {
    try {
      const response = await fetch(`http://localhost:8000/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(taskData),
      });

      const data = await response.json();
      
      if (data.success) {
        setTasks(tasks.map(task => 
          task.id === taskId ? data.data : task
        ));
        return { success: true, message: 'Tarefa atualizada com sucesso!' };
      } else {
        return { success: false, message: data.message };
      }
    } catch (err) {
      return { success: false, message: 'Erro ao atualizar tarefa.' };
    }
  };

  // Marcar tarefa como concluída
  const completeTask = async (taskId) => {
    try {
      const response = await fetch(`http://localhost:8000/tasks/${taskId}/complete`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      
      if (data.success) {
        setTasks(tasks.map(task => 
          task.id === taskId ? data.data : task
        ));
        return { success: true, message: 'Tarefa marcada como concluída!' };
      } else {
        return { success: false, message: data.message };
      }
    } catch (err) {
      return { success: false, message: 'Erro ao marcar tarefa como concluída.' };
    }
  };

  // Deletar tarefa
  const deleteTask = async (taskId) => {
    try {
      const response = await fetch(`http://localhost:8000/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      const data = await response.json();
      
      if (data.success) {
        setTasks(tasks.filter(task => task.id !== taskId));
        return { success: true, message: 'Tarefa removida com sucesso!' };
      } else {
        return { success: false, message: data.message };
      }
    } catch (err) {
      return { success: false, message: 'Erro ao remover tarefa.' };
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Agenda de Tarefas</h1>
        <p>Gerencie suas tarefas de forma simples e eficiente</p>
      </header>

      <main className="App-main">
        <div className="container">
          <TaskForm onAddTask={addTask} />
          
          {loading && (
            <div className="loading">
              <div className="spinner"></div>
              <p>Carregando tarefas...</p>
            </div>
          )}
          
          {error && (
            <div className="error">
              <p>{error}</p>
              <button onClick={fetchTasks} className="retry-btn">
                Tentar novamente
              </button>
            </div>
          )}
          
          {!loading && !error && (
            <TaskList 
              tasks={tasks}
              onUpdateTask={updateTask}
              onCompleteTask={completeTask}
              onDeleteTask={deleteTask}
            />
          )}
        </div>
      </main>

      <footer className="App-footer">
        <p>© 2024 Agenda de Tarefas - Projeto FullStack</p>
      </footer>
    </div>
  );
}

export default App; 