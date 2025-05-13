import React from "react";
import "../styles/global.css";
import "../styles/components.css";

// Produktkarten-Komponente zum Anzeigen von Produktdetails
const ProductCard = ({ product, isSelected, onSelect, onDeselect }) => {
  // Handler für Klick-Events auf der Karte
  const handleClick = (e) => {
    e.preventDefault();
    e.stopPropagation();
    console.log(
      "Produkt angeklickt:",
      product.id,
      "Aktuell ausgewählt:",
      isSelected
    ); // Logging für Debugging

    // Toggle-Logik: Produkt abwählen wenn bereits ausgewählt, sonst auswählen
    if (isSelected) {
      onDeselect();
    } else {
      onSelect();
    }
  };

  return (
    <div className={`product-card ${isSelected ? "selected" : ""}`}>
      {/* Produktkopf mit Namen und Preis */}
      <div className="product-header">
        <h3>{product.name}</h3>
        <p className="price">${product.price}</p>
      </div>

      {/* Produktspezifikationen */}
      <div className="product-specs">
        {/* Kopfbereich */}
        <div className="card-section header">
          <div className="product-type">{product.header.type}</div>
          <h2 className="product-title">{product.header.name}</h2>
          <div className="product-price">{product.header.price}</div>
        </div>

        {/* Zielgruppen-Bereich */}
        <div className="card-section">
          <h3 className="section-title">Target Users</h3>
          <div className="user-groups">
            {product.target_audience.users.map((user, index) => (
              <div key={index} className="user-group">
                {user.trim()}
              </div>
            ))}
          </div>
          {/* Qualifikationsanforderung anzeigen, wenn vorhanden */}
          {product.target_audience.qualification !== "N/A" && (
            <div className="qualification-tag">
              Required: {product.target_audience.qualification}
            </div>
          )}
        </div>

        {/* Systemspezifikationen */}
        {Object.values(product.specifications.system).some(
          (value) => value !== "N/A"
        ) && (
          <div className="card-section">
            <h3 className="section-title">System Specifications</h3>
            <div className="specs-grid">
              {/* Nur relevante Spezifikationen anzeigen (nicht "N/A") */}
              {Object.entries(product.specifications.system)
                .filter(([_, value]) => value !== "N/A")
                .map(([key, value]) => (
                  <div key={key} className="spec-item">
                    <span className="spec-label">{key.toUpperCase()}</span>
                    <span className="spec-value">{value}</span>
                  </div>
                ))}
            </div>
          </div>
        )}
      </div>

      {/* Aktions-Button: Produkt auswählen oder Auswahl aufheben */}
      <button
        className={`action-button ${isSelected ? "deselect" : "select"}`}
        onClick={handleClick}
      >
        {isSelected ? "Deselect product" : "Select product"}
      </button>
    </div>
  );
};

export default ProductCard;