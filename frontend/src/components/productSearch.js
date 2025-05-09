import React, { useState } from "react";
import { searchProducts } from "../services/api";
import "../styles/productSearch.css";

const ProductSearch = () => {
  const [query, setQuery] = useState("");
  const [products, setProducts] = useState([]);

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const response = await searchProducts(query);
      setProducts(response.products);
    } catch (error) {
      console.error("Fehler bei der Produktsuche:", error);
    }
  };

  return (
    <div className="container product-search-container">
      <div className="row mb-3">
        <div className="col-10">
          <input
            type="text"
            className="form-control"
            placeholder="Produkt suchen..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </div>
        <div className="col-2">
          <button className="btn btn-primary w-100" onClick={handleSearch}>
            Suchen
          </button>
        </div>
      </div>
      <div className="row">
        {products.map((product, index) => (
          <div key={index} className="col-12 col-md-6 col-lg-4 mb-3">
            <div className="card">
              <div className="card-body">
                <h5 className="card-title">{product.header.name}</h5>
                <p className="card-text">Preis: {product.header.price}</p>
                <p className="card-text">Typ: {product.header.type}</p>
                <a href={product.header.link} className="btn btn-secondary">
                  Details
                </a>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ProductSearch;