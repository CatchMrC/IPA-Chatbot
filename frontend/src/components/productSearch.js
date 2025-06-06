import React, { useState } from "react";
import "../styles/global.css";
import "../styles/components.css";

// Komponente für die Produkt- und Chatsuche am unteren Rand des Chatfensters
const ProductSearch = ({
  onSubmit,
  disabled,
  selectedProduct,
  placeholder,
}) => {
  // Zustand für den Suchbegriff
  const [query, setQuery] = useState("");

  // Absenden des Formulars
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!query.trim() || disabled) return;

    // Anfrage an übergeordnete Komponente weitergeben
    onSubmit({ query: query.trim() });
    // Eingabefeld zurücksetzen
    setQuery("");
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      {/* Eingabefeld für die Suche */}
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder={placeholder || "Search for products..."}
        className="search-input"
        disabled={disabled}
      />
      {/* Submit-Button nur mit Icon */}
      <button
        type="submit"
        className="search-button icon-only"
        title={selectedProduct ? "Ask about product" : "Search for products"}
        disabled={disabled || !query.trim()}
      >
        {/* Icon basierend auf Kontext */}
        {selectedProduct ? (
          <svg className="button-icon" viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
          </svg>
        ) : (
          <svg className="button-icon" viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z" />
          </svg>
        )}
      </button>
    </form>
  );
};

export default ProductSearch;