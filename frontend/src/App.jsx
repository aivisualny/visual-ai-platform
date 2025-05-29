import { useState } from 'react';

function App() {
  const zDim = 100; // 노이즈 차원
  const [noise, setNoise] = useState(Array(zDim).fill(0)); // 초기 노이즈
  const [imageUrl, setImageUrl] = useState(null);

  // 슬라이더 값 변경 시 노이즈 배열 업데이트
  const handleSliderChange = (index, value) => {
    const updatedNoise = [...noise];
    updatedNoise[index] = parseFloat(value);
    setNoise(updatedNoise);
  };

  // 이미지 생성 요청
  const handleGenerate = async () => {
    const response = await fetch('http://localhost:8000/generate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ noise }),  // noise 배열 전달
    });

    const data = await response.json();
    setImageUrl(`http://localhost:8000${data.image_path}`);
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h1>DCGAN 이미지 생성기</h1>

      <div style={{ marginBottom: '20px' }}>
        <h3>노이즈 벡터 조절 (z)</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(10, 1fr)', gap: '4px', padding: '0 10%' }}>
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

      <button onClick={handleGenerate}>이미지 생성</button>

      {imageUrl && (
        <div style={{ marginTop: '30px' }}>
          <h3>생성된 이미지</h3>
          <img src={imageUrl} alt="Generated" width="256" />
        </div>
      )}
    </div>
  );
}

export default App;
