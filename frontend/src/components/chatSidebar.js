import React, { useState } from "react";
import "../styles/components.css";

// Komponente für die Chat-Seitenleiste zur Verwaltung von Chats
const ChatSidebar = ({
  chats,
  activeChat,
  onSelectChat,
  onCreateChat,
  onRenameChat,
  onDeleteChat,
  isOpen,
  onToggleSidebar,
}) => {
  // Lokale Zustände für die Umbenennung von Chats
  const [editingId, setEditingId] = useState(null); // ID des aktuell editierten Chats
  const [newName, setNewName] = useState(""); // Neuer Name für den Chat
  const [showValidationError, setShowValidationError] = useState(false); // Validierungsfehler anzeigen?

  // Chat-Umbenennung starten
  const handleRenameClick = (chatId, currentName) => {
    setEditingId(chatId);
    setNewName(currentName);
    setShowValidationError(false);
  };

  // Änderungen am Chatnamen verarbeiten und validieren
  const handleNameChange = (e) => {
    const value = e.target.value;
    setNewName(value);

    // Prüfe, ob der Wert Sonderzeichen enthält
    if (value && /[^\w\s]/.test(value)) {
      setShowValidationError(true);
    } else {
      setShowValidationError(false);
    }
  };

  // Umbenennung bestätigen und speichern
  const handleRenameSubmit = (chatId) => {
    if (newName.trim()) {
      // Prüfe, ob der Name Sonderzeichen enthält
      if (/[^\w\s]/.test(newName)) {
        alert(
          "Special characters are not allowed in chat titles. Please remove them and try again."
        );
        return; // Abbrechen bis behoben
      }

      // Sonderzeichen vor dem Speichern entfernen
      const sanitizedName = newName.replace(/[^\w\s]/g, "").trim();
      onRenameChat(chatId, sanitizedName);
    }
    setEditingId(null);
    setNewName("");
    setShowValidationError(false);
  };

  return (
    <>
      {/* Separater Toggle-Button für geschlossene Sidebar */}
      {!isOpen && (
        <div className="sidebar-toggle-container">
          <button
            className="toggle-sidebar-button closed-sidebar-button"
            onClick={onToggleSidebar}
            aria-label="Open chat sidebar"
            title="Open sidebar"
          >
            <img 
              src="/menu-icon.svg" 
              alt="Menu" 
              className="menu-icon" 
            />
          </button>
          <img 
            src="/logo.svg" 
            alt="Logo" 
            className="sidebar-logo closed-sidebar-logo" 
            style={{ 
              height: '64px', // Kleinere Grösse
              marginLeft: '32px' // Weniger Abstand
            }} 
          />
        </div>
      )}

      <div className={`chat-sidebar ${isOpen ? "open" : "closed"}`}>
        <div className="sidebar-header">
          <div className="sidebar-header-left">
            <button
              className="toggle-sidebar-button"
              onClick={onToggleSidebar}
              aria-label="Close chat sidebar"
              title="Close sidebar"
            >
              <img 
                src="/menu-icon.svg" 
                alt="Menu" 
                className="menu-icon" 
              />
            </button>
            <h2>Chats</h2>
          </div>
        </div>
        
        {/* Rest des Sidebar-Inhalts bleibt unverändert */}
        {/* Button zum Erstellen eines neuen Chats */}
        <button
          className="create-chat-button"
          onClick={onCreateChat}
          title="Start new conversation"
        >
          + New Chat
        </button>

        {/* Liste aller vorhandenen Chats */}
        <div className="chat-list">
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${activeChat === chat.id ? "active" : ""}`}
            >
              {/* Eingabefeld für die Umbenennung anzeigen, wenn dieser Chat bearbeitet wird */}
              {editingId === chat.id ? (
                <div
                  className={`chat-rename-form ${
                    showValidationError ? "has-error" : ""
                  }`}
                >
                  <input
                    type="text"
                    value={newName}
                    onChange={handleNameChange}
                    autoFocus
                    onBlur={() => handleRenameSubmit(chat.id)}
                    onKeyPress={(e) => {
                      if (e.key === "Enter") handleRenameSubmit(chat.id);
                    }}
                    placeholder="Enter chat title..."
                    className={showValidationError ? "validation-error" : ""}
                  />
                  {!showValidationError && (
                    <span className="input-helper-text">
                      Letters, numbers and spaces only
                    </span>
                  )}
                  {showValidationError && (
                    <div className="validation-message">
                      Special characters are not allowed
                    </div>
                  )}
                </div>
              ) : (
                // Chat-Eintrag mit Aktionsbuttons anzeigen
                <div
                  className="chat-item-content"
                  onClick={() => onSelectChat(chat.id)}
                >
                  <span className="chat-name">{chat.name}</span>
                  <div className="chat-actions">
                    <button
                      className="rename-button"
                      onClick={(e) => {
                        e.stopPropagation();
                        handleRenameClick(chat.id, chat.name);
                      }}
                      aria-label="Rename chat"
                      title="Change conversation title"
                    >
                      ✏️
                    </button>
                    <button
                      className="delete-button"
                      onClick={(e) => {
                        e.stopPropagation();
                        if (window.confirm(`Delete chat "${chat.name}"?`)) {
                          onDeleteChat(chat.id);
                        }
                      }}
                      aria-label="Delete chat"
                      title="Delete conversation"
                    >
                      🗑️
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Füge das Logo in einer festen Position ausserhalb der Sidebar hinzu */}
      {isOpen && (
        <div className="fixed-logo-container">
          <img 
            src="/logo.svg" 
            alt="Logo" 
            className="sidebar-logo fixed-logo" 
          />
        </div>
      )}
    </>
  );
};

export default ChatSidebar;