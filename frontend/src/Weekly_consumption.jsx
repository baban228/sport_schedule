import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Link } from 'react-router-dom';

const Weekly_consumption = () => {
  const [weeklyData, setWeeklyData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadWeekData = async () => {
      try {
        const res = await fetch('/api/nutrition/nutrition-stats/week/');
        if (res.ok) {
          const data = await res.json();
          // Преобразуем даты в читаемый формат: "21 апр"
          const formatted = data.map(item => ({
            ...item,
            dateLabel: new Date(item.date).toLocaleDateString('ru-RU', {
              day: '2-digit',
              month: 'short'
            })
          }));
          setWeeklyData(formatted);
        }
      } catch (err) {
        console.error('Ошибка загрузки недельных данных:', err);
      } finally {
        setLoading(false);
      }
    };

    loadWeekData();
  }, []);

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <div>
          <Link 
            to="/diet/" 
            style={{ 
              marginRight: '12px',
              padding: '6px 12px',
              backgroundColor: '#e3f2fd',
              borderRadius: '4px',
              textDecoration: 'none',
              color: '#1976d2',
              fontWeight: 'bold',
              border: '1px solid #bbdefb'
            }}
          >
            ↩️ Назад к дневнику
          </Link>
          <a href="/" style={{ textDecoration: 'none', color: '#1976d2' }}>
            🏠 На главную
          </a>
        </div>
      </div>

      {loading ? (
        <p>Загрузка...</p>
      ) : weeklyData.length === 0 ? (
        <p>Нет данных за последнюю неделю.</p>
      ) : (
        <div>
          <h3>Калории по дням</h3>
          <div style={{ height: 300, width: '100%' }}>
            <ResponsiveContainer>
              <LineChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="dateLabel" />
                <YAxis />
                <Tooltip 
                  formatter={(value) => `${value} ккал`}
                  labelFormatter={(label) => `Дата: ${label}`}
                />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="calories" 
                  name="Калории" 
                  stroke="#8884d8" 
                  activeDot={{ r: 8 }} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <h3 style={{ marginTop: '40px' }}>Белки, Жиры, Углеводы (граммы)</h3>
          <div style={{ height: 300, width: '100%' }}>
            <ResponsiveContainer>
              <LineChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="dateLabel" />
                <YAxis />
                <Tooltip formatter={(value) => `${value} г`} />
                <Legend />
                <Line type="monotone" dataKey="protein" name="Белки" stroke="#4CAF50" />
                <Line type="monotone" dataKey="fat" name="Жиры" stroke="#FF9800" />
                <Line type="monotone" dataKey="carbs" name="Углеводы" stroke="#2196F3" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
};

export default Weekly_consumption;