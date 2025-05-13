import React from "react";
// Importiere ProductCard Komponente
import { ProductCard } from "./productCard"; 
import "../styles/global.css";
import "../styles/components.css";

// MessageItem Komponente für die Darstellung von Chat-Nachrichten
// Parameter:
// - message: Die anzuzeigende Nachricht
// - onProductSelect: Callback für Produktauswahl
// - onProductDeselect: Callback für Aufhebung der Produktauswahl
// - selectedProduct: Aktuell ausgewähltes Produkt
const MessageItem = ({
  message,
  onProductSelect,
  onProductDeselect,
  selectedProduct,
}) => {
  return (
    <div className={`message ${message.type}`}>
      <div className="message-content">{message.content}</div>

      {/* Zeige Produktempfehlungen an, falls vorhanden */}
      {message.products?.length > 0 && (
        <div className="product-recommendations">
          <div className="product-list">
            {/* Erstelle für jedes Produkt eine ProductCard Komponente */}
            {message.products.map((product, idx) => (
              <ProductCard
                key={idx}
                product={product}
                onSelect={() => onProductSelect(product)}
                onDeselect={onProductDeselect}
                isSelected={selectedProduct?.product === product.product}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default MessageItem;