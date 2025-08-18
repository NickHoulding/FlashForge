import type { HeaderProps } from '../types';
import Nav from "./Nav";

const Header = (props: HeaderProps) => {
    const { onToggleTheme } = props;
    
    return <header>
        <p id="logo">FlashForge</p>
        <Nav onToggleTheme={onToggleTheme}/>
    </header>;
};

export default Header;
