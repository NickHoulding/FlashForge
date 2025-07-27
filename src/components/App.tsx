import { Sidebar } from './Sidebar'
import { Header } from './Header'
import { useState } from "react";
import '../css/sidebar.css'
import '../css/app.css'

function App() {
  const [isOpen, setIsOpen] = useState(false)

  const toggleSidebar = () => {
    setIsOpen(!isOpen)
  }

  return (
    <main>
      <Sidebar isOpen={isOpen} onToggleSidebar={toggleSidebar} />
      <Header />
    </main>
  )
}

export default App
