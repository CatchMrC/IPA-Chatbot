import React, { useEffect, useState } from 'react';
import { fetchMessages } from '../services/api';

const MessageList = () => {
    const [messages, setMessages] = useState([]);
    const [error, setError] = useState(null);

    useEffect(() => {
        const loadMessages = async () => {
            try {
                const data = await fetchMessages();
                setMessages(data);
            } catch (err) {
                setError('Fehler beim Laden der Nachrichten.');
            }
        };

        loadMessages();
    }, []);

    if (error) {
        return <p>{error}</p>;
    }

    return (
        <ul>
            {messages.map((message) => (
                <li key={message.id}>{message.text}</li>
            ))}
        </ul>
    );
};

export default MessageList;