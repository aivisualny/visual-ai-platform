import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  return (
    <div style={{ textAlign: 'center', marginTop: '100px' }}>
      <h1>🔍 생성 모델 선택</h1>
      <button onClick={() => navigate('/gan')} style={{ margin: '10px', padding: '10px 20px' }}>GAN</button>
      <button onClick={() => navigate('/diffusion')} style={{ margin: '10px', padding: '10px 20px' }}>Diffusion</button>
    </div>
  );
}

export default Home;
