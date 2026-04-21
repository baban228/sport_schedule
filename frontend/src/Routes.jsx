import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Diet from './Diet';
import Weekly_consumption from './Weekly_consumption';

const RoutesConfig = () => {
  return (
    <Routes>
      <Route path="/diet" element={<Diet />} />
      <Route path="/weekly" element={<Weekly_consumption />} />
    </Routes>
  );
};

export default RoutesConfig;