
// === Chat.js - Hauptkomponente für die Chat-Funktionalität ===
import React, { useState, useRef, useEffect, useCallback } from "react";
import ProductSearch from "../components/productSearch";
import MessageList from "../components/messageList";
import ChatSidebar from "../components/chatSidebar";
import {
  sendChatMessage,
  fetchProductRecommendation,
  saveChats,
  loadChats,
} from "../services/api";
import "../styles/global.css";
import "../styles/components.css";


// Chat-Modi für die verschiedenen Funktionsweisen
const CHAT_MODES = {
  GENERAL: "general", // Allgemeine Konversation
  PRODUCT_SEARCH: "product_search", // Produktsuche
  PRODUCT_SPECIFIC: "product_specific", // Produktspezifische Anfragen
};

// Beispielnachrichten für die verschiedenen Chat-Modi
const EXAMPLE_MESSAGES = {
  [CHAT_MODES.GENERAL]: [
    "What IT hardware is available for laboratories?",
    "What options do I have for BL2 and vivarium environments?",
    "Can you recommend hardware for scientific applications?",
  ],
  [CHAT_MODES.PRODUCT_SEARCH]: [
    "I need a mini PC for the lab under 1000 CHF",
    "Show me tablets suitable for BL2 environments",
    "What mobile carts are available for laboratory use?",
  ],
};

// Tooltips für die Modus-Buttons
const MODE_TOOLTIPS = {
  [CHAT_MODES.GENERAL]: "Ask general questions about IT hardware",
  [CHAT_MODES.PRODUCT_SEARCH]: "Search for specific products based on criteria",
  [CHAT_MODES.PRODUCT_SPECIFIC]:
    "Get detailed information about a selected product",
};

// Erstellt die initialen Begrüßungsnachrichten
const createInitialMessages = () => [
  {
    id: "welcome",
    type: "system",
    content:
      "Welcome! I'm your IT hardware assistant. Choose a mode and start chatting!",
    examples: EXAMPLE_MESSAGES[CHAT_MODES.GENERAL],
  },
];

const Chat = () => {
  // === ZUSTAND FÜR SIDEBAR ===
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);

  // === ZUSTAND FÜR CHAT-INHALTE ===
  const [chatStates, setChatStates] = useState({});
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Referenz für das Sidebar-Element
  const sidebarRef = useRef(null);

  // === EFFEKTE UND EVENT-HANDLER ===

  // Effekt zum Behandeln von Klicks außerhalb der Sidebar
  useEffect(() => {
    const handleClickOutside = (event) => {
      // Nur verarbeiten, wenn Sidebar geöffnet ist
      if (!sidebarOpen) return;

      // Wenn Sidebar-Ref existiert und der Klick außerhalb der Sidebar war
      if (sidebarRef.current && !sidebarRef.current.contains(event.target)) {
        setSidebarOpen(false);
      }
    };

    // Event-Listener hinzufügen
    document.addEventListener("mousedown", handleClickOutside);

    // Aufräumen
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [sidebarOpen]); // Nur neu ausführen, wenn sich sidebarOpen ändert

  // === SIDEBAR-HANDLER ===

  // Umschalter für Sidebar-Anzeige
  const handleToggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  // Erstellen eines neuen Chats
  const handleCreateChat = useCallback(() => {
    const newChatId = Date.now().toString();

    // Funktionsform von setState verwenden, um auf aktuellen Zustand zuzugreifen
    setChats((prevChats) => {
      const newChat = {
        id: newChatId,
        name: `Chat ${prevChats.length + 1}`,
      };

      // Neuen Chat am Anfang des Arrays hinzufügen
      return [newChat, ...prevChats];
    });

    // Chat-Zustand initialisieren
    setChatStates((prev) => ({
      ...prev,
      [newChatId]: {
        messages: createInitialMessages(),
        selectedProduct: null,
        chatMode: CHAT_MODES.GENERAL,
      },
    }));

    setActiveChat(newChatId);
  }, []); // Leeres Dependency-Array ist jetzt gültig

  // === CHATS LADEN UND SPEICHERN ===

  // Chats beim Komponenten-Mount laden
  useEffect(() => {
    const loadSavedChats = async () => {
      try {
        const savedChats = await loadChats();
        if (savedChats && savedChats.length > 0) {
          // Bestehende Chats laden
          setChats(savedChats);

          // Chat-Zustände initialisieren
          const states = {};
          savedChats.forEach((chat) => {
            states[chat.id] = {
              messages: chat.messages || createInitialMessages(),
              selectedProduct: chat.selectedProduct || null,
              chatMode: chat.chatMode || CHAT_MODES.GENERAL,
            };
          });
          setChatStates(states);

          // Immer einen neuen Chat beim Start erstellen
          handleCreateChat();
        } else {
          // Standard-Chat erstellen, wenn keiner existiert
          handleCreateChat();
        }
      } catch (error) {
        console.error("Fehler beim Laden der Chats:", error);
        handleCreateChat();
      }
    };

    loadSavedChats();
  }, [handleCreateChat]); // handleCreateChat zum Dependency-Array hinzufügen

  // Chats speichern, wenn sie sich ändern
  useEffect(() => {
    if (chats.length > 0) {
      // Chats ohne Benutzernachrichten vor dem Speichern herausfiltern
      const nonEmptyChats = chats.filter((chat) => {
        const messages = chatStates[chat.id]?.messages || [];
        // Prüfen, ob der Chat mindestens eine Benutzernachricht enthält
        return messages.some((msg) => msg.type === "user");
      });

      const chatsToSave = nonEmptyChats.map((chat) => ({
        ...chat,
        messages: chatStates[chat.id]?.messages || [],
        selectedProduct: chatStates[chat.id]?.selectedProduct || null,
        chatMode: chatStates[chat.id]?.chatMode || CHAT_MODES.GENERAL,
      }));

      saveChats(chatsToSave).catch((error) => {
        console.error("Fehler beim Speichern der Chats:", error);
      });
    }
  }, [chats, chatStates]);

  // Automatisches Scrollen zum Ende der Nachrichtenliste
  useEffect(() => {
    scrollToBottom();
  }, [activeChat, chatStates]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  // === HILFSFUNKTIONEN FÜR ZUSTANDSVERWALTUNG ===

  // Aktuellen Chat-Zustand abrufen
  const getCurrentState = () => {
    if (!activeChat || !chatStates[activeChat]) {
      return {
        messages: createInitialMessages(),
        selectedProduct: null,
        chatMode: CHAT_MODES.GENERAL,
      };
    }
    return chatStates[activeChat];
  };

  // Aktuellen Chat-Zustand aktualisieren
  const updateCurrentState = (updates) => {
    if (!activeChat) return;

    setChatStates((prevStates) => ({
      ...prevStates,
      [activeChat]: {
        ...prevStates[activeChat],
        ...updates,
      },
    }));
  };

  // === CHAT-VERWALTUNGSFUNKTIONEN ===

  // Chat auswählen
  const handleSelectChat = (chatId) => {
    setActiveChat(chatId);
  };

  // Chat umbenennen
  const handleRenameChat = (chatId, newName) => {
    // Namen bereinigen, indem Sonderzeichen entfernt werden
    const sanitizedName = newName.replace(/[^\w\s]/g, "").trim();

    // Falls der bereinigte Name leer ist, einen Standardnamen verwenden
    const finalName = sanitizedName || `Chat ${chats.length}`;

    setChats((prev) =>
      prev.map((chat) =>
        chat.id === chatId ? { ...chat, name: finalName } : chat
      )
    );
  };

  // Chat löschen
  const handleDeleteChat = (chatId) => {
    setChats((prev) => prev.filter((chat) => chat.id !== chatId));
    setChatStates((prev) => {
      const newStates = { ...prev };
      delete newStates[chatId];
      return newStates;
    });

    if (activeChat === chatId) {
      // Dieses Muster verwenden, um veraltete Closures zu vermeiden
      setChats((prevChats) => {
        const remainingChats = prevChats.filter((chat) => chat.id !== chatId);
        if (remainingChats.length > 0) {
          setActiveChat(remainingChats[0].id);
        } else {
          // handleCreateChat für den nächsten Render-Zyklus planen
          setTimeout(handleCreateChat, 0);
        }
        return prevChats;
      });
    }
  };

  // === CHAT-FUNKTIONALITÄT ===

  // Zwischen den Chat-Modi wechseln
  const switchMode = (mode) => {
    const { selectedProduct } = getCurrentState();
    if (mode === CHAT_MODES.PRODUCT_SPECIFIC && !selectedProduct) return;

    updateCurrentState({
      chatMode: mode,
      messages: [
        ...getCurrentState().messages,
        {
          id: Date.now(),
          type: "system",
          content: getModeMessage(mode, selectedProduct),
          examples: EXAMPLE_MESSAGES[mode],
        },
      ],
    });
  };

  // Nachricht für den jeweiligen Chat-Modus generieren
  const getModeMessage = (mode, product) => {
    switch (mode) {
      case CHAT_MODES.GENERAL:
        return "Switched to general conversation mode. Here are some examples of what you can ask:";
      case CHAT_MODES.PRODUCT_SEARCH:
        return "Switched to product search mode. Try asking something like:";
      case CHAT_MODES.PRODUCT_SPECIFIC:
        return product
          ? `Now discussing: ${product.manufacturer} ${product.model}. Ask specific questions about this product.`
          : "Please select a product first.";
      default:
        return "";
    }
  };

  // Produkt auswählen
  const handleProductSelect = (product) => {
    if (!product) return;

    // Formatieren des Produktnamens
    const productName = product.header
      ? `${product.header.manufacturer} ${product.header.model}`
      : `${product.manufacturer} ${product.model}`;

    updateCurrentState({
      selectedProduct: product,
      chatMode: CHAT_MODES.PRODUCT_SPECIFIC,
      messages: [
        ...getCurrentState().messages,
        {
          id: Date.now(),
          type: "system",
          content: `Selected Product: ${
            product.header?.type || product.type
          } - ${productName}`,
        },
      ],
    });
  };

  // Produktauswahl aufheben
  const handleProductDeselect = () => {
    const { selectedProduct } = getCurrentState();
    if (!selectedProduct) return;

    const prevProduct = selectedProduct;

    // Formatieren des Produktnamens
    const productName = prevProduct.header
      ? `${prevProduct.header.manufacturer} ${prevProduct.header.model}`
      : `${prevProduct.manufacturer} ${prevProduct.model}`;

    updateCurrentState({
      selectedProduct: null,
      chatMode: CHAT_MODES.PRODUCT_SEARCH,
      messages: [
        ...getCurrentState().messages,
        {
          id: Date.now(),
          type: "system",
          content: `Product deselected: ${
            prevProduct.header?.type || prevProduct.type
          } - ${productName}`,
        },
      ],
    });
  };

  // Produktanzeige umschalten
  const handleToggleProducts = (messageId) => {
    updateCurrentState({
      messages: getCurrentState().messages.map((msg) =>
        msg.id === messageId ? { ...msg, showProducts: !msg.showProducts } : msg
      ),
    });
  };

  // Chat-Namen aus der Benutzeranfrage generieren
  const generateChatName = (query) => {
    // Sonderzeichen entfernen und Länge begrenzen
    const sanitizedQuery = query.replace(/[^\w\s]/g, "").trim();

    // Erste 30 Zeichen oder weniger nehmen
    const shortQuery = sanitizedQuery.slice(0, 30);

    // Auslassungspunkte hinzufügen, wenn gekürzt
    return shortQuery.length < sanitizedQuery.length
      ? `${shortQuery}...`
      : shortQuery;
  };

  // === HAUPTCHAT-LOGIK ===

  // Chat-Nachrichtenverarbeitung
  const handleChat = async (userInput) => {
    if (!userInput.query.trim()) return;

    try {
      const currentQuery = userInput.query.trim();
      const { chatMode, selectedProduct } = getCurrentState();

      // Benutzernachricht hinzufügen
      const userMessage = {
        id: Date.now(),
        type: "user",
        content: currentQuery,
      };

      // Prüfen, ob es die erste Benutzernachricht ist und Chat-Namen setzen
      const isFirstUserMessage = getCurrentState().messages.every(
        (msg) => msg.type !== "user"
      );

      if (isFirstUserMessage) {
        // Chat-Namen aus dem ersten Benutzer-Prompt generieren
        const chatName = generateChatName(currentQuery);
        // Chat-Namen aktualisieren
        handleRenameChat(activeChat, chatName);
      }

      // Benutzernachricht zum Zustand hinzufügen
      setChatStates((prevChatStates) => {
        const activeMessages = prevChatStates[activeChat]?.messages || [];
        return {
          ...prevChatStates,
          [activeChat]: {
            ...prevChatStates[activeChat],
            messages: [...activeMessages, userMessage],
          },
        };
      });

      // Ladeanimation starten
      setLoading(true);

      // Zum Ende scrollen, um den Tippindikator anzuzeigen
      setTimeout(scrollToBottom, 50);

      // Antwort basierend auf Chat-Modus verarbeiten
      let assistantMessage;

      try {
        switch (chatMode) {
          case CHAT_MODES.GENERAL: {
            const data = await sendChatMessage(currentQuery);
            assistantMessage = {
              id: Date.now() + 1,
              type: "assistant",
              content: data.response,
            };
            break;
          }
          case CHAT_MODES.PRODUCT_SEARCH: {
            // Explizit ein einzelnes Produkt anfordern
            const result = await fetchProductRecommendation(currentQuery);

            // Sicherstellen, dass die Antwort die Produktdaten enthält, die zur LLM-Antwort passen
            assistantMessage = {
              id: Date.now() + 1,
              type: "assistant",
              content: result.llm_response,
              products: result.recommended_products, // Sollte auf 1 Produkt beschränkt sein
              showProducts: false, // Auf true setzen, um die Produktkarte sofort anzuzeigen
            };
            break;
          }
          case CHAT_MODES.PRODUCT_SPECIFIC: {
            if (!selectedProduct)
              throw new Error("Please select a product first");
            const context = { product: selectedProduct };
            const data = await sendChatMessage(
              currentQuery,
              "product_specific",
              context
            );
            assistantMessage = {
              id: Date.now() + 1,
              type: "assistant",
              content: data.response,
            };
            break;
          }
          default:
            throw new Error("Invalid chat mode");
        }

        // Eine kleine Verzögerung hinzufügen, um die Animation besser sichtbar zu machen
        await new Promise((resolve) => setTimeout(resolve, 500));

        // Assistenten-Nachricht hinzufügen
        setChatStates((prevChatStates) => {
          const activeMessages = prevChatStates[activeChat]?.messages || [];
          return {
            ...prevChatStates,
            [activeChat]: {
              ...prevChatStates[activeChat],
              messages: [...activeMessages, assistantMessage],
            },
          };
        });
      } catch (error) {
        const errorMessage = {
          id: Date.now() + 1,
          type: "error",
          content: `Error: ${error.message}. Please try again.`,
        };

        // Fehlermeldung mit Funktionsform hinzufügen
        setChatStates((prevChatStates) => {
          const activeMessages = prevChatStates[activeChat]?.messages || [];
          return {
            ...prevChatStates,
            [activeChat]: {
              ...prevChatStates[activeChat],
              messages: [...activeMessages, errorMessage],
            },
          };
        });
      } finally {
        // Ladeanimation beenden
        setLoading(false);
      }
    } catch (error) {
      console.error("Chat-Fehler:", error);
    }
  };

  // Beispielnachricht verarbeiten
  const handleExampleClick = (example) => handleChat({ query: example });

  // Platzhaltertext basierend auf Modus und ausgewähltem Produkt
  const getPlaceholder = (mode, selectedProduct) => {
    switch (mode) {
      case CHAT_MODES.PRODUCT_SEARCH:
        return "Search for products...";
      case CHAT_MODES.PRODUCT_SPECIFIC:
        return selectedProduct
          ? `Ask about ${selectedProduct.manufacturer} ${selectedProduct.model}...`
          : "Select a product first...";
      default:
        return "Type your message...";
    }
  };

  // Aktuellen Chat-Zustand abrufen
  const currentState = getCurrentState();
  const { messages, selectedProduct, chatMode } = currentState;

  // === RENDER-KOMPONENTE ===
  return (
    <div className="app-container">
      <div ref={sidebarRef}>
        <ChatSidebar
          chats={chats}
          activeChat={activeChat}
          onSelectChat={handleSelectChat}
          onCreateChat={handleCreateChat}
          onRenameChat={handleRenameChat}
          onDeleteChat={handleDeleteChat}
          isOpen={sidebarOpen}
          onToggleSidebar={handleToggleSidebar}
        />
      </div>

      <div
        className={`chat-container ${
          sidebarOpen ? "with-sidebar" : "without-sidebar"
        }`}
      >
        <div className="chat-header">
          <h1 className="chat-title">Laboratory IT Hardware Assistant</h1>
          <div className="mode-selector">
            {Object.values(CHAT_MODES).map((mode) => (
              <button
                key={mode}
                className={`mode-button ${chatMode === mode ? "active" : ""}`}
                onClick={() => switchMode(mode)}
                disabled={
                  mode === CHAT_MODES.PRODUCT_SPECIFIC && !selectedProduct
                }
                title={MODE_TOOLTIPS[mode]}
              >
                {mode
                  .split("_")
                  .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
                  .join(" ")}
              </button>
            ))}
          </div>
        </div>

        <div className="chat-content">
          <MessageList
            messages={messages}
            loading={loading}
            messagesEndRef={messagesEndRef}
            onProductSelect={handleProductSelect}
            onProductDeselect={handleProductDeselect}
            selectedProduct={selectedProduct}
            chatMode={chatMode}
            onExampleClick={handleExampleClick}
            onToggleProducts={handleToggleProducts}
          />
        </div>

        <ProductSearch
          onSubmit={handleChat}
          disabled={loading}
          mode={chatMode}
          selectedProduct={selectedProduct}
          placeholder={getPlaceholder(chatMode, selectedProduct)}
        />
      </div>
    </div>
  );
};

export default Chat;