import React, { useState, useEffect } from 'react';
import './TaskForm.css';

const TaskForm = ({ onAddTask }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    due_date: ''
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // Timer para desaparecer mensagem
  useEffect(() => {
    if (message) {
      const timer = setTimeout(() => {
        setMessage('');
      }, 3000); // 3 segundos

      return () => clearTimeout(timer);
    }
  }, [message]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.title.trim()) {
      setMessage({ type: 'error', text: 'Título é obrigatório!' });
      return;
    }

    setLoading(true);
    setMessage('');

    try {
      const result = await onAddTask(formData);
      
      if (result.success) {
        setFormData({
          title: '',
          description: '',
          due_date: ''
        });
        setMessage({ type: 'success', text: result.message });
      } else {
        setMessage({ type: 'error', text: result.message });
      }
    } catch (error) {
      setMessage({ type: 'error', text: 'Erro ao criar tarefa.' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="task-form-container">
      <h2>Nova Tarefa</h2>
      
      <form onSubmit={handleSubmit} className="task-form">
        <div className="form-group">
          <label htmlFor="title">Título *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            placeholder="Digite o título da tarefa"
            required
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="description">Descrição</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Digite a descrição da tarefa (opcional)"
            rows="3"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="due_date">Data de Vencimento</label>
          <input
            type="datetime-local"
            id="due_date"
            name="due_date"
            value={formData.due_date}
            onChange={handleChange}
            disabled={loading}
          />
        </div>

        <button 
          type="submit" 
          className="submit-btn"
          disabled={loading || !formData.title.trim()}
        >
          {loading ? 'Criando...' : 'Criar Tarefa'}
        </button>
      </form>

      {message && (
        <div className={`message ${message.type}`}>
          {message.text}
        </div>
      )}
    </div>
  );
};

export default TaskForm; 