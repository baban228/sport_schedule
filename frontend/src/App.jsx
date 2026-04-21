import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import RoutesConfig from './Routes';

function App() {
  return (
    <Router>
      <div className="app">
        <RoutesConfig />
      </div>
    </Router>
  );
}

export default App;