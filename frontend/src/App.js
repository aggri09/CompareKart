import React, { useState } from 'react';
import axios from 'axios';
import './style.css';

const App = () => {
  // State for handling product name input and displaying the results
  const [productName, setProductName] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  // Handle input change
  const handleProductNameChange = (event) => {
    setProductName(event.target.value);
  };

  // Handle the Compare Prices button click
  const handleComparePrices = async () => {
    // Clear any previous error
    setError(null);
    
    // Only make request if product name is provided
    if (!productName) {
      setError('Product name is required');
      return;
    }

    try {
      // Sending POST request to Flask backend
      const response = await axios.post('http://127.0.0.1:5000/compare-price', {
        product_name: productName
      });

      // Set the result from the backend response
      setResult(response.data);
    } catch (error) {
      // Handle errors if any occur during the API call
      setError('Error fetching data. Please try again.');
      console.error('Error fetching data', error);
    }
  };

  return (
    <div className="App">
      <h1>Price Comparator</h1>
      
      {/* Input for entering the product name */}
      <input
        type="text"
        value={productName}
        onChange={handleProductNameChange}
        placeholder="Enter product name"
      />

      {/* Button to trigger price comparison */}
      <button onClick={handleComparePrices}>Compare Prices</button>

      {/* Display results if available */}
      {result && (
        <div>
          <h2>Prices</h2>
          <div>
            <h3>Flipkart</h3>
            <p>Price: {result.flipkart.price}</p>
            <a href={result.flipkart.url} target="_blank" rel="noopener noreferrer">View on Flipkart</a>
          </div>
          <div>
            <h3>Amazon</h3>
            <p>Price: {result.amazon.price}</p>
            <a href={result.amazon.url} target="_blank" rel="noopener noreferrer">View on Amazon</a>
          </div>
        </div>
      )}

      {/* Display error message if any */}
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default App;
