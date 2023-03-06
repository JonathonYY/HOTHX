import './App.css';
import { BrowserRouter, Routes, Route, Link, Outlet, Switch } from 'react-router-dom';
import HomePage from './pages/homePage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage/>} />
      </Routes>
    </BrowserRouter>
    
  );
}

export default App;