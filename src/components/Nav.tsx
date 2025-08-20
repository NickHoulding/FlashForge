import type { NavProps } from '../types';

const Nav = ({ onToggleTheme }: NavProps) => {
    return <nav className="flex items-center">
        <ul className="font-[Satoshi-Medium] text-[1.05rem] flex items-center list-none">
            <li className="text-[var(--primary)] mr-10">Home</li>
            <li className="text-[var(--primary)] mr-10">About</li>
        </ul>
        <button
            className="w-10 h-min flex items-center justify-center text-[var(--primary)] bg-transparent p-[5px] rounded hover:bg-[var(--accent)] cursor-pointer"
            onClick={onToggleTheme}>
            <svg fill="currentColor" height="24" viewBox="0 0 24 24" width="24" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22ZM12 20V4C16.4183 4 20 7.58172 20 12C20 16.4183 16.4183 20 12 20Z"/></svg>
        </button>
    </nav>;
};

export default Nav;
