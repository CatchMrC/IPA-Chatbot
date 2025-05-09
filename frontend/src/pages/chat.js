import React, { useState, useRef, useEffect } from "react";
import "../styles/chat.css";
import ProductCard from "../components/productCard";
import { sendChatMessage, searchProducts, fetchProductRecommendation } from "../services/api";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [chatMode, setChatMode] = useState("general"); // "general" oder "product-search"
  const [query, setQuery] = useState(""); // Für Produktsuche
  const [products, setProducts] = useState([]); // Ergebnisse der Produktsuche
  const messagesEndRef = useRef(null);

  // Scrollt automatisch zu den neuesten Nachrichten
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Lädt gespeicherte Nachrichten aus localStorage
  useEffect(() => {
    const savedMessages = JSON.parse(localStorage.getItem("messages")) || [];
    setMessages(savedMessages);
  }, []);

  // Speichert Nachrichten in localStorage
  useEffect(() => {
    localStorage.setItem("messages", JSON.stringify(messages));
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      if (chatMode === "general") {
        // Genereller Chat-Modus
        const response = await sendChatMessage(input, "general");
        const botMessage = { sender: "bot", text: response.response };
        setMessages((prev) => [...prev, botMessage]);
      } else if (chatMode === "product-search") {
        // Produktsuche und Empfehlung
        const searchResults = await searchProducts(input);
        console.log("Suchergebnisse:", searchResults);

        // Extrahiere relevante Informationen aus den Suchergebnissen
        const formattedResults = searchResults.products.map((product) => {
          const { manufacturer, model, name, price, link } = product.header;
          return `${name} (${manufacturer} - ${model}) - Preis: ${price} CHF - [Mehr Infos](${link})`;
        });

        const recommendation = await fetchProductRecommendation(input);
        console.log("Empfehlung:", recommendation);

        const botMessage = {
          sender: "bot",
          text: `Suchergebnisse:\n${formattedResults.join("\n")}\n\nEmpfehlung: ${recommendation.message}`,
        };
        setMessages((prev) => [...prev, botMessage]);
      }
    } catch (error) {
      console.error("Fehler beim Senden der Nachricht:", error);
      const errorMessage = {
        sender: "bot",
        text: error.response?.data?.message || "Es gab ein Problem mit der Anfrage. Bitte versuchen Sie es später erneut.",
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleProductSearch = async () => {
    if (!query) return;
    try {
      const response = await searchProducts(query);
      setProducts(response.products);
    } catch (error) {
      console.error("Fehler bei der Produktsuche:", error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !loading) {
      handleSendMessage();
    }
  };

  const switchMode = (mode) => {
    setChatMode(mode);
    const botMessage = {
      sender: "bot",
      text: `Modus gewechselt zu: ${mode === "general" ? "Genereller Chat" : "Produktsuche"}`,
    };
    setMessages((prev) => [...prev, botMessage]);
  };

  return (
    <div className="container chat-container">
      <div className="row">
        <div className="col-12 chat-messages">
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`chat-message ${
                msg.sender === "user" ? "user-message" : "bot-message"
              }`}
            >
              {msg.text}
            </div>
          ))}
          {loading && <div className="chat-message bot-message">Antwort wird geladen...</div>}
          <div ref={messagesEndRef}></div>
        </div>
      </div>
      <div className="row chat-input-container">
        <div className="col-10">
          <input
            type="text"
            className="form-control"
            placeholder="Nachricht eingeben..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
          />
        </div>
        <div className="col-2">
          <button
            className="btn btn-primary w-100"
            onClick={handleSendMessage}
            disabled={loading}
          >
            Senden
          </button>
        </div>
      </div>
      {chatMode === "product-search" && (
        <div className="row mt-3">
          <div className="col-12">
            <input
              type="text"
              className="form-control"
              placeholder="Produkt suchen..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
            <button className="btn btn-primary mt-2" onClick={handleProductSearch}>
              Suchen
            </button>
          </div>
          <div className="col-12 product-results mt-3">
            {products.map((product, index) => (
              <ProductCard
                key={index}
                name={product.header.name}
                price={product.header.price}
                type={product.header.type}
                link={product.header.link}
              />
            ))}
          </div>
        </div>
      )}
      <div className="row mt-3">
        <div className="col-6">
          <button
            className={`btn ${chatMode === "general" ? "btn-secondary" : "btn-outline-secondary"} w-100`}
            onClick={() => switchMode("general")}
            disabled={loading}
          >
            Genereller Chat
          </button>
        </div>
        <div className="col-6">
          <button
            className={`btn ${chatMode === "product-search" ? "btn-secondary" : "btn-outline-secondary"} w-100`}
            onClick={() => switchMode("product-search")}
            disabled={loading}
          >
            Produktsuche
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;