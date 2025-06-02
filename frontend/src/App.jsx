import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import GanPage from './pages/GanPage';
import DiffusionPage from './pages/DiffusionPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/gan" element={<GanPage />} />
        <Route path="/diffusion" element={<DiffusionPage />} />
      </Routes>
    </Router>
  );
}

export default App;
