import { Nav } from "./Nav";

export function Header() {
    return (
        <header>
            <button className="sidebar-button">
                <svg height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg">
                    <path fill="currentColor" d="M8,5 L3,5 L3,19 L8,19 L8,5 Z M10,5 L10,19 L21,19 L21,5 L10,5 Z M2.81818182,3 L21.1818182,3 C22.1859723,3 23,3.8954305 23,5 L23,19 C23,20.1045695 22.1859723,21 21.1818182,21 L2.81818182,21 C1.81402773,21 1,20.1045695 1,19 L1,5 C1,3.8954305 1.81402773,3 2.81818182,3 Z"/>
                </svg>
            </button>
            <Nav />
        </header>
    )
}