import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from './pages/Home';
import Flashcards from './pages/Flashcards';
import ChatRoom from './pages/ChatRoom';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-blue-500 p-4 text-white">
          <a href="/" className="mr-4 hover:underline">Home</a>
          <a href="/flashcards" className="mr-4 hover:underline">Flashcards</a>
          <a href="/chat" className="hover:underline">Chat</a>
        </nav>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/flashcards" element={<Flashcards />} />
        <Route path="/chat" element={<ChatRoom />} />
      </Routes>
      </div>
    </BrowserRouter>
  )
}