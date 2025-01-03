import React from 'react';
import PolandMap from './PolandMap';
import CityLine from './CityLine';

function App() {
  const cityCoordinates = {
    Warsaw: [52.2297, 21.0122],
    Krakow: [50.0647, 19.9450],
    Gdansk: [54.3520, 18.6466],
  };

  const lines = [
    { from: 'Warsaw', to: 'Krakow' },
    { from: 'Warsaw', to: 'Gdansk' },
  ];

  const handleLineClick = (line) => {
    alert(`Clicked line from ${line.from} to ${line.to}`);
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>Map of Poland</h1>
      <PolandMap>
        {lines.map((line, index) => (
          <CityLine
            key={index}
            positions={[cityCoordinates[line.from], cityCoordinates[line.to]]}
            onClick={() => handleLineClick(line)}
          />
        ))}
      </PolandMap>
    </div>
  );
}

export default App;
