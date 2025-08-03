import React, { useState } from 'react';
import './TaskList.css';

const TaskList = ({ tasks, onUpdateTask, onCompleteTask, onDeleteTask }) => {
  const [editingTask, setEditingTask] = useState(null);
  const [editData, setEditData] = useState({});

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

  // Ordenar tarefas: pendentes primeiro, depois concluídas
  const sortedTasks = [...tasks].sort((a, b) => {
    if (a.status === 'pendente' && b.status === 'concluída') return -1;
    if (a.status === 'concluída' && b.status === 'pendente') return 1;
    return 0;
  });

  const formatDate = (dateString) => {
    if (!dateString) return 'Sem data definida';
    
    const date = new Date(dateString);
    return date.toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const isOverdue = (task) => {
    if (!task.due_date || task.status === 'concluída') return false;
    return new Date(task.due_date) < new Date();
  };

  const handleEdit = (task) => {
    setEditingTask(task.id);
    setEditData({
      title: task.title,
      description: task.description,
      due_date: task.due_date ? task.due_date.slice(0, 16) : '',
      status: task.status
    });
  };

  const handleSave = async (taskId) => {
    try {
      const result = await onUpdateTask(taskId, editData);
      if (result.success) {
        setEditingTask(null);
        setEditData({});
      }
    } catch (error) {
      console.error('Erro ao atualizar tarefa:', error);
    }
  };

  const handleCancel = () => {
    setEditingTask(null);
    setEditData({});
  };

  const renderTaskRow = (task) => {
    const isEditing = editingTask === task.id;

    return (
      <tr key={task.id} className="task-row">
        <td className="task-title-cell">
          {isEditing ? (
            <input
              type="text"
              value={editData.title}
              onChange={(e) => setEditData({...editData, title: e.target.value})}
              className="edit-input"
            />
          ) : (
            <strong>{task.title}</strong>
          )}
        </td>
        <td className="task-description-cell">
          {isEditing ? (
            <textarea
              value={editData.description}
              onChange={(e) => setEditData({...editData, description: e.target.value})}
              className="edit-textarea"
              rows="2"
            />
          ) : (
            <span title={task.description || '-'}>
              {task.description || '-'}
            </span>
          )}
        </td>
        <td className="task-status-cell">
          {isEditing ? (
            <select
              value={editData.status}
              onChange={(e) => setEditData({...editData, status: e.target.value})}
              className="edit-select"
            >
              <option value="pendente">Pendente</option>
              <option value="concluída">Concluída</option>
            </select>
          ) : (
            <span className={`task-status ${task.status}`}>
              {task.status === 'pendente' ? 'Pendente' : 'Concluída'}
            </span>
          )}
        </td>
        <td className="task-date-cell">
          {formatDate(task.created_at)}
        </td>
        <td className="task-due-date-cell">
          {isEditing ? (
            <input
              type="datetime-local"
              value={editData.due_date}
              onChange={(e) => setEditData({...editData, due_date: e.target.value})}
              className="edit-input"
            />
          ) : (
            task.due_date ? formatDate(task.due_date) : '-'
          )}
        </td>
        <td className="task-actions-cell">
          <div className="task-actions">
            {isEditing ? (
              <>
                <button 
                  onClick={() => handleSave(task.id)}
                  className="save-btn"
                  title="Salvar"
                >
                  ✓
                </button>
                <button 
                  onClick={handleCancel}
                  className="cancel-btn"
                  title="Cancelar"
                >
                  ✕
                </button>
              </>
            ) : (
              <>
                {task.status === 'pendente' && (
                  <button 
                    onClick={() => onCompleteTask(task.id)}
                    className="complete-btn"
                    title="Marcar como concluída"
                  >
                    ✓
                  </button>
                )}
                <button 
                  onClick={() => handleEdit(task)}
                  className="edit-btn"
                  title="Editar"
                >
                  ✎
                </button>
                <button 
                  onClick={() => onDeleteTask(task.id)}
                  className="delete-btn"
                  title="Excluir"
                >
                  ✕
                </button>
              </>
            )}
          </div>
        </td>
      </tr>
    );
  };

  return (
    <div className="task-list-container">
      <h2>Lista de Tarefas</h2>
      
      <div className="task-section">
        <div className="task-table-container">
          <table className="task-table">
            <thead>
              <tr>
                <th>Título</th>
                <th>Descrição</th>
                <th>Status</th>
                <th>Criada em</th>
                <th>Vence em</th>
                <th>Ações</th>
              </tr>
            </thead>
            <tbody>
              {sortedTasks.map(renderTaskRow)}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default TaskList; 