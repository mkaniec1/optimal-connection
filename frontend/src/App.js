import React, {useState, useEffect} from 'react';
import PolandMap from './PolandMap';
import CityLine from './CityLine';

function App() {
  const backend_address = 'http://localhost:8000';
  const [cities, setCities] = useState({});
  const [connections, setConnections] = useState([]);

  useEffect(() => {
    const fetchConnectionsData = async () => {
      try {
        const response = await fetch(backend_address + '/api/connections');
        const data = await response.json();
        const cityData = {}
        data.cities.forEach(city => {
          cityData[city[0]] = [city[1], city[2]]
        });
        setCities(cityData);
        setConnections(
          data.connections.map(conn => ({
            id: conn[0],
            starting_node_id: conn[1],
            ending_node_id: conn[2],
            total_capacity: conn[3],
            provisioned_capacity: conn[4]
          })));
      } catch (error) {
        console.error('Error fetching city coordinates', error);
      }
    };
    fetchConnectionsData();
  }, []); // use only once

  const handleLineClick = (conn) => {
    alert(`Conn busy in ${conn.provisioned_capacity}%`);
  };

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h1>Map of Poland</h1>
      <PolandMap>
        {connections.map((conn) => (
          <CityLine
            key={conn.id}
            positions={[cities[conn.starting_node_id], cities[conn.ending_node_id]]}
            onClick={() => handleLineClick(conn)}
          />
        ))}
      </PolandMap>
    </div>
  );
}

export default App;
