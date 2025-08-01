import type { HeaderProps } from '../types';
import { Nav } from "./Nav";

export function Header({ onToggleTheme }: HeaderProps) {
    return (
        <header>
            <p id="logo">FlashForge</p>
            <Nav onToggleTheme={onToggleTheme}/>
        </header>
    )
}
