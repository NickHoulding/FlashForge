interface SidebarProps {
    isOpen: boolean
    onToggleSidebar: () => void
    onToggleTheme: () => void
}

export function Sidebar({ isOpen, onToggleSidebar, onToggleTheme }: SidebarProps) {
    return (
        <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
            <div className="top-controls">
                <button className="toggle-sidebar" onClick={onToggleSidebar}>
                    <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M4.75 4C3.23122 4 2 5.23122 2 6.75V17.25C2 18.7688 3.23122 20 4.75 20H19.25C20.7688 20 22 18.7688 22 17.25V6.75C22 5.23122 20.7688 4 19.25 4H4.75ZM9 18.5V5.5H19.25C19.9404 5.5 20.5 6.05964 20.5 6.75V17.25C20.5 17.9404 19.9404 18.5 19.25 18.5H9Z"/></svg>
                </button>
            </div>
            <div id="chats"></div>
            <div className="bottom-controls">
                <button className="toggle-theme" onClick={onToggleTheme}>
                    <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22ZM12 20V4C16.4183 4 20 7.58172 20 12C20 16.4183 16.4183 20 12 20Z"/></svg>
                </button>
            </div>
        </aside>
    )
}
