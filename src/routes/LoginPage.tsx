import { useState } from "react";

const LoginPage = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const PlaceholderErrorMessage = "Incorrect password";

    // TODO: Implement this to handle sign-ins
    const handleSignIn = async () => {
        return null;
    };

    // TODO: Implement this to handle new account creation
    const handleAccountCreate = async () => {
        return null;
    };

    return (
        <main className="flex flex-col gap-[20px] items-center justify-center absolute bg-[var(--neutral)] w-screen h-screen z-20000">
            <h1 className="font-[Satoshi-Bold] text-[2.10rem]">FlashForge</h1>
            <input 
                placeholder="Enter username" 
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-[300px] bg-[var(--accent)] text-[var(--primary)] border border-[var(--secondary)] p-[10px] rounded-[10px] resize-none text-[1.05rem]" 
                id="">
            </input>
            <input 
                placeholder="Enter password" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-[300px] bg-[var(--accent)] text-[var(--primary)] border border-[var(--secondary)] p-[10px] rounded-[10px] resize-none text-[1.05rem]" id=""></input>
            <div className="w-[300px] flex gap-[20px]">
                <button 
                    onClick={handleAccountCreate}
                    className="flex-1 text-[1.05rem] py-[10px] font-[Satoshi-Regular] bg-[var(--secondary)] hover:bg-[var(--primary)] hover:text-[var(--neutral)] rounded-[10px] cursor-pointer">Create</button>
                <button 
                    onClick={handleSignIn}
                    className="flex-1 text-[1.05rem] py-[10px] font-[Satoshi-Regular] bg-[var(--secondary)] hover:bg-[var(--primary)] hover:text-[var(--neutral)] rounded-[10px] cursor-pointer">Sign in</button>
            </div>
            <div className="w-[300px] text-[1.05rem] font-[Satoshi-Regular] text-center text-red-400 mt-[10px]">{PlaceholderErrorMessage}</div>
        </main>
    );
};

export default LoginPage;
