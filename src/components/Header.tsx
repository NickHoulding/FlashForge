import { Nav } from "./Nav";

interface HeaderProps {
    onToggleTheme: () => void
}

export function Header({ onToggleTheme }: HeaderProps) {
    return (
        <header>
            <p id="logo">FlashForge</p>
            <Nav onToggleTheme={onToggleTheme}/>
        </header>
    )
}
