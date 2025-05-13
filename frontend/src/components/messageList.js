import React from "react";
import ReactMarkdown from "react-markdown";
import "github-markdown-css/github-markdown.css";
import remarkGfm from "remark-gfm";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";
import ProductCard from "./productCard";
import "../styles/global.css";
import "../styles/components.css";

// Animierte Tippindikator-Komponente
const TypingIndicator = () => (
  <div className="typing-indicator">
    <span></span>
    <span></span>
    <span></span>
  </div>
);

// Hauptkomponente für die Nachrichtenliste im Chat
const MessageList = ({
  messages,
  loading,
  selectedProduct,
  onProductSelect,
  onProductDeselect,
  messagesEndRef,
  onExampleClick,
  onToggleProducts,
}) => {
  return (
    <div className="message-list">
      {/* Alle Nachrichten durchlaufen und entsprechend ihrem Typ rendern */}
      {messages.map((message, messageIndex) => (
        <div
          key={message.id || messageIndex}
          className={`message-container ${message.type}-container`}
        >
          {/* System-Nachrichten: Beinhaltet Willkommensnachrichten und Beispiele */}
          {message.type === "system" && (
            <div className="message system">
              <ReactMarkdown
                children={message.content}
                remarkPlugins={[remarkGfm]}
                components={{
                  // Syntax-Highlighting für Code-Blöcke
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={atomDark}
                        language={match[1]}
                        PreTag="div"
                        {...props}
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                  // Links spezielle Formatierung
                  a({ node, children, href, ...props }) {
                    return (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="chat-link"
                        {...props}
                      >
                        {children}
                      </a>
                    );
                  },
                }}
              />
              {/* Beispiel-Buttons anzeigen, wenn vorhanden */}
              {message.examples && (
                <div className="examples">
                  {message.examples.map((example, index) => (
                    <button
                      key={index}
                      className="example-button"
                      onClick={() => onExampleClick(example)}
                    >
                      {example}
                    </button>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Benutzer-Nachrichten: Eingaben des Anwenders */}
          {message.type === "user" && (
            <div className="message user">
              <div className="message-content">{message.content}</div>
            </div>
          )}

          {/* Assistenten-Nachrichten: Antworten des Chatbots */}
          {message.type === "assistant" && (
            <div className="message assistant markdown-body">
              <ReactMarkdown
                children={message.content}
                remarkPlugins={[remarkGfm]}
                components={{
                  // Gleiche Code-Formatierung wie bei System-Nachrichten
                  code({ node, inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");
                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={atomDark}
                        language={match[1]}
                        PreTag="div"
                        {...props}
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },
                  // Gleiche Link-Formatierung wie bei System-Nachrichten
                  a({ node, children, href, ...props }) {
                    return (
                      <a
                        href={href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="chat-link"
                        {...props}
                      >
                        {children}
                      </a>
                    );
                  },
                }}
              />

              {/* Produktempfehlungsbereich mit umschaltbarer Anzeige */}
              {message.products?.length > 0 && (
                <div className="product-recommendations">
                  <button
                    className={`toggle-products-button ${
                      message.showProducts ? "active" : ""
                    }`}
                    onClick={() => onToggleProducts(message.id)}
                  >
                    {message.showProducts
                      ? "Hide recommended products"
                      : "Show recommended products"}
                  </button>

                  {message.showProducts && (
                    <>
                      {" "}
                      {/* Raster für Produktkarten */}
                      <div className="products-grid">
                        {message.products.map((product, index) => (
                          <ProductCard
                            key={`product-${messageIndex}-${index}`}
                            product={product}
                            isSelected={selectedProduct?.id === product.id}
                            onSelect={() => onProductSelect(product)}
                            onDeselect={onProductDeselect}
                          />
                        ))}
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      ))}

      {/* Ladeindikator während der Antwortgenerierung */}
      {loading && <TypingIndicator />}

      {/* Referenz für automatisches Scrollen */}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;