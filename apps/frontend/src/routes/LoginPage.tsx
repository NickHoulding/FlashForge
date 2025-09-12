import { useNavigate } from "react-router-dom";
import { useState } from "react";

const LoginPage = () => {
    const navigate = useNavigate();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const handleSignIn = async () => {
        try {
            const response = await fetch('http://localhost:3001/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });
            if (!response.ok) { throw new Error('Login failed'); }

            const data = await response.json();
            localStorage.setItem('token', data.token);
            navigate('/');
        } catch {
            setError('Login failed');
        }
    };

    const handleAccountCreate = async () => {
        try {
            const response = await fetch('http://localhost:3001/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password }),
            });

            if (!response.ok) { throw new Error('Acount creation failed'); }
            navigate('/');
        } catch {
            setError('Account creation failed');
        }
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
            <div className="w-[300px] text-[1.05rem] font-[Satoshi-Regular] text-center text-red-400 mt-[10px]">{error}</div>
        </main>
    );
};

export default LoginPage;
