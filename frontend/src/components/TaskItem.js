import React, { useState } from 'react';
import './TaskItem.css';

const TaskItem = ({ task, onUpdateTask, onCompleteTask, onDeleteTask }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState({
    title: task.title,
    description: task.description,
    due_date: task.due_date ? task.due_date.slice(0, 16) : ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleEdit = () => {
    setIsEditing(true);
    setMessage('');
  };

  const handleCancel = () => {
    setIsEditing(false);
    setEditData({
      title: task.title,
      description: task.description,
      due_date: task.due_date ? task.due_date.slice(0, 16) : ''
    });
    setMessage('');
  };

  const handleSave = async () => {
    if (!editData.title.trim()) {
      setMessage({ type: 'error', text: 'Título é obrigatório!' });
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const result = await onUpdateTask(task.id, editData);
      
      if (result.success) {
        setIsEditing(false);
        setMessage({ type: 'success', text: result.message });
      } else {
        setMessage({ type: 'error', text: result.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao atualizar tarefa.' });
    } finally {
      setLoading(false);
    }
  };

  const handleComplete = async () => {
    setLoading(true);
    setMessage('');

    try {
      const result = await onCompleteTask(task.id);
      setMessage({ type: 'success', text: result.message });
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao marcar como concluída.' });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const result = await onDeleteTask(task.id);
      setMessage({ type: 'success', text: result.message });
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao excluir tarefa.' });
    } finally {
      setLoading(false);
    }
  };

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

  const isOverdue = () => {
    if (!task.due_date || task.status === 'concluída') return false;
    return new Date(task.due_date) < new Date();
  };

  return (
    <div className={`task-item ${task.status} ${isOverdue() ? 'overdue' : ''}`}>
      {isEditing ? (
        /* Modo de edição */
        <div className="task-edit">
          <div className="form-group">
            <label>Título *</label>
            <input
              type="text"
              value={editData.title}
              onChange={(e) => setEditData({...editData, title: e.target.value})}
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label>Descrição</label>
            <textarea
              value={editData.description}
              onChange={(e) => setEditData({...editData, description: e.target.value})}
              rows="3"
              disabled={loading}
            />
          </div>
          
          <div className="form-group">
            <label>Data de Vencimento</label>
            <input
              type="datetime-local"
              value={editData.due_date}
              onChange={(e) => setEditData({...editData, due_date: e.target.value})}
              disabled={loading}
            />
          </div>
          
          <div className="edit-actions">
            <button 
              onClick={handleSave} 
              className="save-btn"
              disabled={loading}
            >
              {loading ? 'Salvando...' : 'Salvar'}
            </button>
            <button 
              onClick={handleCancel} 
              className="cancel-btn"
              disabled={loading}
            >
              Cancelar
            </button>
          </div>
        </div>
      ) : (
        /* Modo de visualização */
        <div className="task-content">
          <div className="task-header">
            <h3 className="task-title">{task.title}</h3>
            <span className={`task-status ${task.status}`}>
              {task.status === 'pendente' ? 'Pendente' : 'Concluída'}
            </span>
          </div>
          
          {task.description && (
            <p className="task-description">{task.description}</p>
          )}
          
          <div className="task-meta">
            <span className="task-date">
              Criada em: {formatDate(task.created_at)}
            </span>
            {task.due_date && (
              <span className={`task-due-date ${isOverdue() ? 'overdue' : ''}`}>
                Vence em: {formatDate(task.due_date)}
              </span>
            )}
          </div>
          
          <div className="task-actions">
            {task.status === 'pendente' && (
              <button 
                onClick={handleComplete}
                className="complete-btn"
                disabled={loading}
              >
                Concluir
              </button>
            )}
            <button 
              onClick={handleEdit}
              className="edit-btn"
              disabled={loading}
            >
              Editar
            </button>
            <button 
              onClick={handleDelete}
              className="delete-btn"
              disabled={loading}
            >
              Excluir
            </button>
          </div>
        </div>
      )}
      
      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default TaskItem; 