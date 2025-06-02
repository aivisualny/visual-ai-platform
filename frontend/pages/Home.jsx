// src/pages/Home.jsx
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: 'center', marginTop: '100px' }}>
      <h1>모델 선택</h1>
      <button onClick={() => navigate('/gan')} style={{ marginRight: '20px' }}>GAN</button>
      <button onClick={() => navigate('/diffusion')}>Diffusion</button>
    </div>
  );
}

export default Home;
