import axios from "axios";

const API_URL = "http://localhost:8000";

// Chat-Endpunkt für allgemeine Konversationen und produktspezifische Anfragen
export const sendChatMessage = async (
  message,
  role_type = "general",
  context = null
) => {
  try {
    const response = await axios.post(`${API_URL}/api/chat`, {
      message,
      role_type,
      context,
    });
    return response.data;
  } catch (error) {
    console.error("Chat-Fehler:", error);
    throw error;
  }
};

// Einfache Produktsuche über ChromaDB-Vektorabfragen
export const searchProducts = async (query) => {
  const response = await fetch(`${API_URL}/api/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ query }),
  });

  if (!response.ok) {
    throw new Error("Produkte konnten nicht abgerufen werden");
  }

  return response.json();
};

// Produktempfehlung mit LLM-Unterstützung
export const fetchProductRecommendation = async (query) => {
  const response = await fetch(`${API_URL}/api/recommendation`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
      single_product: true, // Immer nur ein Produkt anzeigen
    }),
  });

  if (!response.ok) {
    throw new Error("Empfehlung konnte nicht abgerufen werden");
  }

  return response.json(); // Gibt zurück: { recommended_products, llm_response }
};

// Chat-Speicherfunktionen für lokale Persistenz
export const saveChats = async (chats) => {
  try {
    localStorage.setItem("it-hardware-chats", JSON.stringify(chats));
    return true;
  } catch (error) {
    console.error("Fehler beim Speichern der Chats:", error);
    throw error;
  }
};

export const loadChats = async () => {
  try {
    const savedChats = localStorage.getItem("it-hardware-chats");
    return savedChats ? JSON.parse(savedChats) : [];
  } catch (error) {
    console.error("Fehler beim Laden der Chats:", error);
    throw error;
  }
};