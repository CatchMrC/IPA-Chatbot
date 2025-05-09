import React from "react";
import "../styles/productCard.css";

const ProductCard = ({ name, price, type, link }) => {
  return (
    <div className="card product-card">
      <div className="card-body">
        <h5 className="card-title">{name}</h5>
        <p className="card-text">Preis: {price}</p>
        <p className="card-text">Typ: {type}</p>
        <a href={link} className="btn btn-secondary">
          Mehr Infos
        </a>
      </div>
    </div>
  );
};

export default ProductCard;