import React from 'react';
import TaskItem from './TaskItem';
import './TaskList.css';

const TaskList = ({ tasks, onUpdateTask, onCompleteTask, onDeleteTask }) => {
  if (tasks.length === 0) {
    return (
      <div className="task-list-container">
        <div className="empty-state">
          <h3>Nenhuma tarefa encontrada</h3>
          <p>Comece criando sua primeira tarefa usando o formulário acima!</p>
        </div>
      </div>
    );
  }

  // Separar tarefas por status
  const pendingTasks = tasks.filter(task => task.status === 'pendente');
  const completedTasks = tasks.filter(task => task.status === 'concluída');

  return (
    <div className="task-list-container">
              <h2>Lista de Tarefas</h2>
      
      {/* Tarefas Pendentes */}
      {pendingTasks.length > 0 && (
        <div className="task-section">
                      <h3 className="section-title pending">
              Pendentes ({pendingTasks.length})
            </h3>
          <div className="task-grid">
            {pendingTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdateTask={onUpdateTask}
                onCompleteTask={onCompleteTask}
                onDeleteTask={onDeleteTask}
              />
            ))}
          </div>
        </div>
      )}

      {/* Tarefas Concluídas */}
      {completedTasks.length > 0 && (
        <div className="task-section">
                      <h3 className="section-title completed">
              Concluídas ({completedTasks.length})
            </h3>
          <div className="task-grid">
            {completedTasks.map(task => (
              <TaskItem
                key={task.id}
                task={task}
                onUpdateTask={onUpdateTask}
                onCompleteTask={onCompleteTask}
                onDeleteTask={onDeleteTask}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

 export default TaskList; 