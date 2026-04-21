import React from 'react';
import { Link } from 'react-router-dom';

const Weekly_consumption = () => {
  return (
    <div className="page">
      <h1>Страница 2</h1>
      <p>Это вторая страница.</p>
      <Link to="/diet" className="btn">← Назад</Link>
    </div>
  );
};

export default Weekly_consumption;