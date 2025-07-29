interface SidebarProps {
    isOpen: boolean
    onToggleSidebar: () => void
}

export function Sidebar({ isOpen, onToggleSidebar }: SidebarProps) {
    return (
        <aside className={`sidebar ${isOpen ? 'open' : 'closed'}`}>
            <div className="top-controls">
                <button className="toggle-sidebar" onClick={onToggleSidebar}>
                    <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M4.75 4C3.23122 4 2 5.23122 2 6.75V17.25C2 18.7688 3.23122 20 4.75 20H19.25C20.7688 20 22 18.7688 22 17.25V6.75C22 5.23122 20.7688 4 19.25 4H4.75ZM9 18.5V5.5H19.25C19.9404 5.5 20.5 6.05964 20.5 6.75V17.25C20.5 17.9404 19.9404 18.5 19.25 18.5H9Z"/></svg>
                </button>
            </div>
            <div id="chats"></div>
            <div className="bottom-controls">
                <button className="profile-button">
                    <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM17 13.5C17 12.6716 16.3284 12 15.5 12H8.5C7.67157 12 7 12.6716 7 13.5V14C7 15.9714 8.85951 18 12 18C15.1405 18 17 15.9714 17 14V13.5ZM14.75 8.25C14.75 6.73122 13.5188 5.5 12 5.5C10.4812 5.5 9.25 6.73122 9.25 8.25C9.25 9.76878 10.4812 11 12 11C13.5188 11 14.75 9.76878 14.75 8.25Z"/>
                    </svg>
                </button>
            </div>
        </aside>
    )
}
