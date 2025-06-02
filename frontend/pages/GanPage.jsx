// src/pages/GanPage.jsx
import { useState } from 'react';

function GanPage() {
  const zDim = 100;
  const [noise, setNoise] = useState(Array(zDim).fill(0));
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSliderChange = (index, value) => {
    const updatedNoise = [...noise];
    updatedNoise[index] = parseFloat(value);
    setNoise(updatedNoise);
  };

  const handleGenerate = async () => {
    setLoading(true);
    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ noise }),
    });

    const data = await response.json();
    setImageUrl(`http://localhost:8000${data.image_path}`);
    setLoading(false);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>GAN 이미지 생성기</h1>
      <div style={{ marginBottom: '20px' }}>
        <h3>노이즈 벡터 조절 (z)</h3>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(10, 1fr)',
          gap: '4px',
          padding: '0 10%'
        }}>
          {noise.map((val, i) => (
            <input
              key={i}
              type="range"
              min={-1}
              max={1}
              step={0.1}
              value={val}
              onChange={(e) => handleSliderChange(i, e.target.value)}
            />
          ))}
        </div>
      </div>

      <button onClick={handleGenerate} disabled={loading}>
        {loading ? '생성 중...' : '이미지 생성'}
      </button>

      {imageUrl && (
        <div style={{ marginTop: '30px' }}>
          <h3>생성된 이미지</h3>
          <img src={imageUrl} alt="Generated" width="280" />
        </div>
      )}
    </div>
  );
}

export default GanPage;
