import { Sidebar } from './components/Sidebar'
import { Header } from './components/Header'
import { useState } from "react";
import './css/sidebar.css'
import './css/app.css'

function App() {
  const [isOpen, setIsOpen] = useState(false)

  const openSidebar = () => {
      setIsOpen(true)
  }

  const closeSidebar = () => {
      setIsOpen(false)
  }

  return (
    <main>
      <Sidebar isOpen={isOpen} onCloseSidebar={closeSidebar} />
      <Header onOpenSidebar={openSidebar} />
    </main>
  )
}

export default App
