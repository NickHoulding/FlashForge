import type { HeaderProps } from '../types';
import Nav from "./Nav";

const Header = ({ onToggleTheme }: HeaderProps) => {
    return <header 
        className={`z-10000 h-[55px] absolute top-0 right-0 left-0 flex justify-between items-center px-[10px] pl-[20px] bg-[var(--neutral)] transition-all duration-300 ease-in-out border-b border-[var(--secondary)]`}>
        <p className="font-[Satoshi-Bold] text-[1.25rem] text-[var(--primary)] leading-[0.5] p-0">FlashForge</p>
        <Nav onToggleTheme={onToggleTheme}/>
    </header>;
};

export default Header;
