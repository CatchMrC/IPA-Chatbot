import React, { useState } from "react";
import { fetchProductRecommendation } from "../services/api";

const ProductRecommendation = () => {
  const [query, setQuery] = useState("");
  const [recommendation, setRecommendation] = useState(null);

  const handleRecommendation = async () => {
    if (!query.trim()) return;

    try {
      const response = await fetchProductRecommendation(query);
      setRecommendation(response);
    } catch (error) {
      console.error("Fehler bei der Produktempfehlung:", error);
    }
  };

  return (
    <div className="product-recommendation-container">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Produktempfehlung anfordern..."
      />
      <button onClick={handleRecommendation}>Empfehlung anfordern</button>
      {recommendation && (
        <div className="recommendation-result">
          <h3>Empfohlene Produkte:</h3>
          {recommendation.products.map((product, index) => (
            <div key={index} className="product-card">
              <h4>{product.header.name}</h4>
              <p>Preis: {product.header.price}</p>
              <p>Typ: {product.header.type}</p>
            </div>
          ))}
          <p>{recommendation.message}</p>
        </div>
      )}
    </div>
  );
};

export default ProductRecommendation;