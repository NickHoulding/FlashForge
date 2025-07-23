import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Home from './pages/Home';
import Flashcards from './pages/Flashcards';
import ChatRoom from './pages/ChatRoom';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-blue-500 p-4 text-white">
          <Link to="/" className="mr-4 hover:underline">Home</Link>
          <Link to="/flashcards" className="mr-4 hover:underline">Flashcards</Link>
          <Link to="/chat" className="hover:underline">Chat</Link>
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