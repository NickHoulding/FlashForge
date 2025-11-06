import type { SidebarProps } from '../types';
import ChatEntry from "./ChatEntry";

const Sidebar = ({ isOpen, onToggleSidebar }: SidebarProps) => {
    const baseAside = 'sidebar-transition flex flex-col gap-[10px] box-border h-full p-[10px_2px_10px_10px] text-[var(--primary)] border-r border-[var(--secondary)] shrink-0 overflow-hidden';
    const closedAside = 'w-[60px] bg-[var(--neutral)]';
    const openAside = 'w-[250px] bg-[var(--accent)]';

    return <aside className={`${baseAside} ${isOpen ? openAside : closedAside}`}>
        <div className={`h-min w-auto bg-transparent flex mr-2 justify-end pb-[10px] border-b transition-colors ${isOpen ? 'border-[var(--secondary)]' : 'border-transparent'}`}>
            <button
                className={`w-10 h-min flex items-center justify-center text-[var(--primary)] bg-transparent p-[5px] rounded ${isOpen ? 'hover:bg-[var(--neutral)]' : 'hover:bg-[var(--accent)]'} ${isOpen ? 'hover:cursor-w-resize' : 'hover:cursor-e-resize'}`}
                onClick={onToggleSidebar}>
                <svg 
                    fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M4.75 4C3.23122 4 2 5.23122 2 6.75V17.25C2 18.7688 3.23122 20 4.75 20H19.25C20.7688 20 22 18.7688 22 17.25V6.75C22 5.23122 20.7688 4 19.25 4H4.75ZM9 18.5V5.5H19.25C19.9404 5.5 20.5 6.05964 20.5 6.75V17.25C20.5 17.9404 19.9404 18.5 19.25 18.5H9Z"/>
                </svg>
            </button>
        </div>
        <div id="chats" className={`chat-transition ${isOpen ? 'opening' : 'closing'} flex flex-col flex-1 overflow-y-auto pr-[10px] pl-[2px] ${isOpen ? 'opacity-100' : 'opacity-0'} ${!isOpen ? 'select-none pointer-events-none' : ''}`}>
            <ChatEntry />
        </div>

    </aside>;
};

export default Sidebar;
