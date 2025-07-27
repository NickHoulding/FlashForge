import { Sidebar } from './Sidebar'
import { Header } from './Header'
import { useState, useEffect } from "react";
import '../css/sidebar.css'
import '../css/app.css'

function App() {
  const [isOpen, setIsOpen] = useState(false)
  const [isDarkTheme, setIsDarkTheme] = useState(true)

  const toggleSidebar = () => {
    setIsOpen(!isOpen)
  }

  const toggleTheme = () => {
    setIsDarkTheme(!isDarkTheme)
  }

  useEffect(() => {
    document.documentElement.className = isDarkTheme ? 'dark-theme' : 'light-theme'
  }, [isDarkTheme])

  return (
    <main>
      <Sidebar isOpen={isOpen} onToggleSidebar={toggleSidebar} onToggleTheme={toggleTheme} />
      <div className='content'>
        <Header />
        <div className='chat'></div>
      </div>
    </main>
  )
}

export default App
