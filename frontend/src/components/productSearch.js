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
      {/* Submit-Button mit unterschiedlichem Text je nach Kontext */}
      <button
        type="submit"
        className="search-button"
        title="Send message"
        disabled={disabled || !query.trim()}
      >
        {selectedProduct ? "Ask" : "Search"}
      </button>
    </form>
  );
};

export default ProductSearch;