import { useState } from 'react';

function DiffusionPage() {
  const [imageUrl, setImageUrl] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    setImageUrl(null);
    try {
      const response = await fetch('http://localhost:8000/generate/diffusion', {
        method: 'POST',
      });

      const data = await response.json();
      if (response.ok) {
        setImageUrl(`http://localhost:8000${data.image_path}`);
      } else {
        setError(data.error || '생성 실패');
      }
    } catch (err) {
      setError('서버 연결 오류');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '100px' }}>
      <h1>🌫️ Diffusion 이미지 생성</h1>
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? '생성 중...' : '이미지 생성'}
      </button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {imageUrl && (
        <div style={{ marginTop: '30px' }}>
          <h3>🎨 생성된 이미지</h3>
          <img src={imageUrl} alt="Generated Diffusion" width="280" />
        </div>
      )}
    </div>
  );
}

export default DiffusionPage;
