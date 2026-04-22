// src/pages/Diet.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { PieChart, Pie, Cell, Tooltip, ResponsiveContainer } from 'recharts';

// Получить CSRF-токен из cookie
function getCSRFToken() {
  const name = 'csrftoken=';
  const decodedCookie = decodeURIComponent(document.cookie);
  const ca = decodedCookie.split(';');
  for (let i = 0; i < ca.length; i++) {
    let c = ca[i];
    while (c.charAt(0) === ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) === 0) {
      return c.substring(name.length, c.length);
    }
  }
  return '';
}

const Diet = () => {
  const [formData, setFormData] = useState({
    name: '',
    weight: '',
    calories_per_100: '',
    protein_per_100: '',
    fat_per_100: '',
    carbs_per_100: '',
    meal_type: 'breakfast'
  });

  const [totals, setTotals] = useState({
    calories: 0,
    protein: 0,
    fat: 0,
    carbs: 0
  });

  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  // Цвета для графика
  const COLORS = ['#4CAF50', '#FF9800', '#2196F3']; // Белки, Жиры, Углеводы
  const MACRO_LABELS = ['Белки', 'Жиры', 'Углеводы'];

  // Загрузить сегодняшнюю статистику
  const loadStats = async () => {
    try {
      const res = await fetch('/api/nutrition/nutrition-stats/today/');
      if (res.ok) {
        const data = await res.json();
        setTotals(data);
      }
    } catch (err) {
      console.error('Не удалось загрузить статистику', err);
    }
  };

  useEffect(() => {
    loadStats();
  }, []);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    const {
      name, weight, calories_per_100,
      protein_per_100, fat_per_100, carbs_per_100, meal_type
    } = formData;

    if (!name || !weight || !calories_per_100) {
      setMessage('⚠️ Заполните название, вес и калории');
      setLoading(false);
      return;
    }

    try {
      const today = new Date().toISOString().split('T')[0];
      const csrfToken = getCSRFToken();

      // 1. Создать продукт
      const productRes = await fetch('/api/nutrition/products/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          name: name.trim(),
          calories: parseFloat(calories_per_100),
          protein: parseFloat(protein_per_100 || 0),
          fat: parseFloat(fat_per_100 || 0),
          carbs: parseFloat(carbs_per_100 || 0)
        })
      });

      if (!productRes.ok) {
        const errorData = await productRes.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Не удалось создать продукт');
      }
      const product = await productRes.json();

      // 2. Создать приём пищи
      const mealRes = await fetch('/api/nutrition/meals/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          date: today,
          meal_type: meal_type
        })
      });

      if (!mealRes.ok) {
        const errorData = await mealRes.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Не удалось создать приём пищи');
      }
      const meal = await mealRes.json();

      // 3. Добавить элемент
      const itemRes = await fetch('/api/nutrition/meal-items/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          meal: meal.id,
          product: product.id,
          weight: parseFloat(weight)
        })
      });

      if (!itemRes.ok) {
        const errorData = await itemRes.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Не удалось добавить запись');
      }

      setMessage('✅ Успешно добавлено!');
      setFormData({
        name: '',
        weight: '',
        calories_per_100: '',
        protein_per_100: '',
        fat_per_100: '',
        carbs_per_100: '',
        meal_type: 'breakfast'
      });

      loadStats();
    } catch (err) {
      console.error('Ошибка:', err);
      setMessage(`❌ ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Подготовка данных для графика
  const totalMacros = totals.protein + totals.fat + totals.carbs;
  const pieData = totalMacros > 0 ? [
    { name: 'Белки', value: totals.protein },
    { name: 'Жиры', value: totals.fat },
    { name: 'Углеводы', value: totals.carbs },
  ] : [];

  return (
    <div style={{ padding: '20px', maxWidth: '700px', margin: '0 auto' }}>
      <h1>Добавить приём пищи</h1>

      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '20px' 
      }}>
        <a href="/" style={{ textDecoration: 'none', color: '#1976d2' }}>🏠 На главную</a>
        <Link 
          to="/weekly/" 
          style={{ 
            padding: '6px 12px',
            backgroundColor: '#e0e0e0',
            borderRadius: '4px',
            textDecoration: 'none',
            color: '#333',
            fontWeight: 'bold'
          }}
        >
          📅 Неделя
        </Link>
      </div>

      {/* Круговая диаграмма */}
      <div style={{ marginBottom: '25px', textAlign: 'center' }}>
        <h3>Сегодняшнее соотношение БЖУ</h3>
        {totalMacros > 0 ? (
          <div style={{ height: 300, margin: '0 auto' }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip formatter={(value) => `${value.toFixed(1)} г`} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <p>Пока ничего не записано.</p>
        )}

        {/* Общие калории */}
        <div style={{ marginTop: '15px', fontSize: '18px' }}>
          🔥 <strong>{totals.calories.toFixed(1)}</strong> ккал
        </div>
      </div>

      {/* Сообщение */}
      {message && (
        <div style={{
          marginBottom: '20px',
          padding: '10px',
          backgroundColor: message.includes('✅') ? '#e8f5e9' : '#ffebee',
          color: message.includes('✅') ? '#2e7d32' : '#c62828',
          borderRadius: '4px'
        }}>
          {message}
        </div>
      )}

      {/* Форма */}
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '15px' }}>
          <label>Название блюда или продукта:</label>
          <input
            type="text"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label>Вес (в граммах):</label>
          <input
            type="number"
            name="weight"
            value={formData.weight}
            onChange={handleChange}
            required
            min="1"
            step="1"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ marginBottom: '15px' }}>
          <label>Калории на 100г:</label>
          <input
            type="number"
            name="calories_per_100"
            value={formData.calories_per_100}
            onChange={handleChange}
            required
            min="0"
            step="0.1"
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
          <div>
            <label>Белки на 100г:</label>
            <input
              type="number"
              name="protein_per_100"
              value={formData.protein_per_100}
              onChange={handleChange}
              min="0"
              step="0.1"
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>
          <div>
            <label>Жиры на 100г:</label>
            <input
              type="number"
              name="fat_per_100"
              value={formData.fat_per_100}
              onChange={handleChange}
              min="0"
              step="0.1"
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>
          <div>
            <label>Углеводы на 100г:</label>
            <input
              type="number"
              name="carbs_per_100"
              value={formData.carbs_per_100}
              onChange={handleChange}
              min="0"
              step="0.1"
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            />
          </div>
          <div>
            <label>Приём пищи:</label>
            <select
              name="meal_type"
              value={formData.meal_type}
              onChange={handleChange}
              style={{ width: '100%', padding: '8px', marginTop: '5px' }}
            >
              <option value="breakfast">Завтрак</option>
              <option value="lunch">Обед</option>
              <option value="dinner">Ужин</option>
              <option value="snack">Перекус</option>
            </select>
          </div>
        </div>

        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '10px 20px',
            fontSize: '16px',
            backgroundColor: loading ? '#ccc' : '#2196f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer'
          }}
        >
          {loading ? 'Отправка...' : 'Добавить'}
        </button>
      </form>
    </div>
  );
};

export default Diet;