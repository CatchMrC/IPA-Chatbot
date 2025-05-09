import axios from "axios";

const API_URL = "http://localhost:8000/api";

// Chat-Endpunkt für allgemeine Konversationen und produktspezifische Anfragen
export const sendChatMessage = async (message, role_type = "general", context = null) => {
  try {
    const response = await axios.post(`${API_URL}/chat`, {
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

// Produktsuche über ChromaDB
export const searchProducts = async (query) => {
  try {
    const response = await axios.post(`${API_URL}/search`, {
      query,
    });
    return response.data;
  } catch (error) {
    console.error("Produktsuche-Fehler:", error);
    throw error;
  }
};

// Produktempfehlung mit LLM-Unterstützung
export const fetchProductRecommendation = async (query, single_product = true) => {
  try {
    const response = await axios.post(`${API_URL}/recommendation`, {
      query,
      single_product,
    });
    return response.data;
  } catch (error) {
    console.error("Empfehlungs-Fehler:", error);
    throw error;
  }
};