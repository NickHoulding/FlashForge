import type { HeaderProps } from '../types';
import Nav from "./Nav";

const Header = ({ onToggleTheme }: HeaderProps) => {
    return <header>
        <p id="logo">FlashForge</p>
        <Nav onToggleTheme={onToggleTheme}/>
    </header>;
};

export default Header;
