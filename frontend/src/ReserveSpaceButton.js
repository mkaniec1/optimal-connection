const ReserveSpaceButton = ({ onClick }) => {

  return <button onClick={onClick}
    style={{
    background: 'linear-gradient(90deg, #4CAF50, #81C784)', // Green gradient
    color: 'white',
    fontWeight: 'bold',
    fontSize: '16px',
    borderRadius: '8px',
    padding: '10px 20px',
    border: 'none',
    cursor: 'pointer',
    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
    transition: 'all 0.3s ease',
  }}
  onMouseOver={(e) => (e.target.style.boxShadow = '0px 6px 8px rgba(0, 0, 0, 0.2)')}
  onMouseOut={(e) => (e.target.style.boxShadow = '0px 4px 6px rgba(0, 0, 0, 0.1)')}>reserve space</button> ;
};

export default ReserveSpaceButton;
