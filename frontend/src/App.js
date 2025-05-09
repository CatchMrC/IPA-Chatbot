import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Chat from './pages/chat';
import 'bootstrap/dist/css/bootstrap.min.css';
import './styles/branding.css';




const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Chat />} />
            </Routes>
        </Router>
    );
};

export default App;